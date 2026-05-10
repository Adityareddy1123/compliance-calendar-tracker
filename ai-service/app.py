from flask import Flask, request, jsonify
import os
import json
import time
from collections import deque
from dotenv import load_dotenv
from groq import Groq
from services.response_builder import build_meta
from routes.generate_report import generate_report_bp

# Chroma
from services.chroma_service import ChromaService

# Fake Redis (no Docker needed)
import fakeredis
import hashlib

# -----------------------------
# INIT
# -----------------------------
app = Flask(__name__)
app.register_blueprint(generate_report_bp)

load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        '.env'
    )
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma = ChromaService()

# Fake Redis
redis_client = fakeredis.FakeRedis(decode_responses=True)

CACHE_TTL = 900  # 15 minutes
MODEL_NAME = "llama-3.1-8b-instant"

# -----------------------------
# METRICS
# -----------------------------
response_times = deque(maxlen=10)
start_time = time.time()

cache_hits = 0
cache_misses = 0

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "AI Chatbot Running"
    })


# -----------------------------
# QUERY (Day 5 + Day 8 + Day 9)
# -----------------------------
@app.route("/query", methods=["POST"])
def query():

    global cache_hits, cache_misses

    start = time.time()

    data = request.get_json()

    question = data.get("question")
    use_cache = data.get("use_cache", True)

    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400

    # -----------------------------
    # CACHE KEY
    # -----------------------------
    cache_key = hashlib.sha256(
        question.encode()
    ).hexdigest()

    # -----------------------------
    # CACHE CHECK
    # -----------------------------
    if use_cache:

        cached = redis_client.get(cache_key)

        if cached:

            cache_hits += 1

            result = json.loads(cached)

            end = time.time()

            response_time_ms = round(
                (end - start) * 1000,
                2
            )

            response_times.append(end - start)

            meta = build_meta(
                confidence=0.95,
                model_used=MODEL_NAME,
                tokens_used=0,
                response_time_ms=response_time_ms,
                cached=True
            )

            return jsonify({
                "answer": result["answer"],
                "sources": result["sources"],
                "meta": meta
            })

    # -----------------------------
    # CACHE MISS
    # -----------------------------
    cache_misses += 1

    docs = chroma.query(question, top_k=3)

    if not docs:

        meta = build_meta(
            confidence=0.60,
            model_used=MODEL_NAME,
            tokens_used=0,
            response_time_ms=0,
            cached=False
        )

        return jsonify({
            "answer": "No relevant data found",
            "sources": [],
            "meta": meta
        })

    context = "\n".join(docs)

    prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{question}
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content

        result = {
            "answer": answer,
            "sources": docs
        }

        # -----------------------------
        # STORE CACHE
        # -----------------------------
        if use_cache:
            redis_client.setex(
                cache_key,
                CACHE_TTL,
                json.dumps(result)
            )

        end = time.time()

        response_time_ms = round(
            (end - start) * 1000,
            2
        )

        response_times.append(end - start)

        meta = build_meta(
            confidence=0.95,
            model_used=MODEL_NAME,
            tokens_used=150,
            response_time_ms=response_time_ms,
            cached=False
        )

        return jsonify({
            "answer": answer,
            "sources": docs,
            "meta": meta
        })

    except Exception as e:
        fallback_answer = """
The AI service is currently unavailable.
Using fallback response.

Compliance management helps organizations follow regulations,
track deadlines, manage audits, and maintain policy compliance.
"""

    meta = build_meta(
        confidence=0.50,
        model_used=MODEL_NAME,
        tokens_used=0,
        response_time_ms=0,
        cached=False,
        is_fallback=True
    )

    return jsonify({
        "answer": fallback_answer,
        "fallback_reason": str(e),
        "meta": meta
    }), 200


# -----------------------------
# HEALTH (Day 7)
# -----------------------------
@app.route("/health", methods=["GET"])
def health():

    avg_response_time = (
        sum(response_times) / len(response_times)
        if response_times else 0
    )

    uptime = time.time() - start_time

    try:
        doc_count = chroma.collection.count()

    except:
        doc_count = 0

    return jsonify({
        "status": "healthy",
        "model": MODEL_NAME,
        "avg_response_time": round(avg_response_time, 4),
        "uptime_seconds": int(uptime),
        "chroma_doc_count": doc_count,
        "cache": {
            "hits": cache_hits,
            "misses": cache_misses
        }
    })


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=False)
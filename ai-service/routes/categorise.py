from flask import Blueprint, request, jsonify
from services.response_builder import build_meta
import time

categorise_bp = Blueprint("categorise", __name__)

@categorise_bp.route("/categorise", methods=["POST"])
def categorise():

    start = time.time()

    data = request.json
    text = data.get("text")

    result = {
        "category": "Finance",
        "reasoning": "Detected finance keywords"
    }

    response_time = round((time.time() - start) * 1000, 2)

    meta = build_meta(
        confidence=0.95,
        tokens_used=120,
        response_time_ms=response_time,
        cached=False
    )

    return jsonify({
        "data": result,
        "meta": meta
    })
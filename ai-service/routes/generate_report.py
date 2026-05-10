from flask import Blueprint, request, jsonify
from threading import Thread
import uuid
import time

from services.job_store import jobs

generate_report_bp = Blueprint("generate_report", __name__)

# ---------------------------------
# Background Processing
# ---------------------------------
def process_report(job_id, data):

    time.sleep(5)

    report = {
        "title": "Compliance Report",
        "summary": "AI-generated report completed successfully.",
        "generated_for": data.get("topic", "General Compliance")
    }

    jobs[job_id] = {
        "status": "completed",
        "report": report
    }

# ---------------------------------
# Generate Report API
# ---------------------------------
@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    data = request.get_json()

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "processing"
    }

    thread = Thread(
        target=process_report,
        args=(job_id, data)
    )

    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })

# ---------------------------------
# Check Job Status API
# ---------------------------------
@generate_report_bp.route("/report-status/<job_id>", methods=["GET"])
def report_status(job_id):

    job = jobs.get(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    return jsonify(job)
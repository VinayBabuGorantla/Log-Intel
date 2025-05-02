from flask import Flask, render_template, request, flash, redirect, url_for
import os
import tempfile

from src.config.logger import setup_logger
from src.utils.file_utils import is_supported_file
from src.ingestion.log_loader import extract_from_zip, load_and_aggregate_text
from src.indexing.vector_store import create_vector_store, load_vector_store
from src.qa.qa_chain import ask_question
from src.analysis.log_analyzer import extract_warnings_errors, summarize_performance, get_advanced_insights
from src.exception.custom_exception import AppException

app = Flask(__name__)
app.secret_key = "loggenie-secret"
logger = setup_logger(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/upload-log/", methods=["POST"])
def upload_log():
    try:
        uploaded_file = request.files.get("file")
        if not uploaded_file or uploaded_file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("index"))

        file_name = uploaded_file.filename.lower()
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file_name)
        uploaded_file.save(file_path)
        logger.info(f"Uploaded file saved to: {file_path}")

        # Process ZIP or single log file
        if file_name.endswith(".zip"):
            extracted_files = extract_from_zip(file_path, temp_dir)
            if not extracted_files:
                flash("No valid log files found in ZIP.", "error")
                return redirect(url_for("index"))
            text = load_and_aggregate_text(extracted_files)
        elif is_supported_file(file_path):
            text = load_and_aggregate_text([file_path])
        else:
            flash("Unsupported file type.", "error")
            return redirect(url_for("index"))

        # Vector DB
        create_vector_store(text)
        flash("Log(s) uploaded and processed successfully.", "success")
        return redirect(url_for("home"))

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        flash(f"Upload failed: {str(e)}", "error")
        return redirect(url_for("index"))

@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.form.get("question")
        if not question:
            flash("Please enter a question.", "error")
            return redirect(url_for("home"))

        vector_store = load_vector_store()
        if vector_store is None:
            flash("No logs uploaded yet.", "error")
            return redirect(url_for("index"))

        answer = ask_question(vector_store, question)
        return render_template("home.html", question=question, answer=answer)

    except Exception as e:
        logger.error(f"Question failed: {e}")
        flash(f"Failed to process question: {str(e)}", "error")
        return redirect(url_for("home"))

@app.route("/analyze", methods=["GET"])
def analyze():
    try:
        vector_store = load_vector_store()
        if vector_store is None:
            flash("No logs uploaded yet.", "error")
            return redirect(url_for("index"))

        # Load all texts (assuming they're stored)
        docs = vector_store._collection.get()["documents"]
        combined_text = "\n".join(docs)

        warnings, errors = extract_warnings_errors(combined_text)
        performance = summarize_performance(combined_text)
        insights = get_advanced_insights(combined_text)

        return render_template("home.html", warnings=warnings, errors=errors,
                               performance=performance, insights=insights)

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        flash("Failed to analyze logs.", "error")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

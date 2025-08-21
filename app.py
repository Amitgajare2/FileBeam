from flask import Flask, request, send_from_directory, render_template, url_for
from werkzeug.utils import secure_filename
import os
import json
from urllib.parse import unquote



app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
META_FILE = "file_meta.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load or create metadata (to store original filename ↔ safe filename)
if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        file_meta = json.load(f)
else:
    file_meta = {}

@app.route('/')
def index():
    # Build files list from actual folder contents and metadata
    existing_safe_names = set(os.listdir(UPLOAD_FOLDER))
    files = []

    # Add entries that have metadata and exist on disk
    for original_name, safe_name in file_meta.items():
        if safe_name in existing_safe_names:
            files.append({"original": original_name, "safe": safe_name})

    # Add any files on disk that are not in metadata
    known_safes = {entry["safe"] for entry in files}
    for safe_name in existing_safe_names - known_safes:
        files.append({"original": safe_name, "safe": safe_name})

    # Sort by original name for consistent display
    files.sort(key=lambda f: f["original"].lower())

    return render_template("index.html", files=files)

@app.route('/uploads', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    original_name = file.filename
    safe_name = secure_filename(original_name)

    # Save file under safe name
    file.save(os.path.join(UPLOAD_FOLDER, safe_name))

    # Store mapping (original → safe)
    file_meta[original_name] = safe_name
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(file_meta, f, indent=2)

    return "✅ File uploaded successfully! <a href='/'>Go back</a>"

@app.route('/files/<path:filename>')
def download(filename):
    # Decode %20 etc. into real characters
    decoded_name = unquote(filename)

    # Try to find mapping in metadata
    safe_name = file_meta.get(decoded_name)

    # If not found, check if file exists directly
    if not safe_name:
        if os.path.exists(os.path.join(UPLOAD_FOLDER, decoded_name)):
            safe_name = decoded_name
        else:
            return f"❌ File not found: {decoded_name}", 404

    return send_from_directory(UPLOAD_FOLDER, safe_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

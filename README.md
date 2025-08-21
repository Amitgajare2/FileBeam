## File Share Server (Flask)

A minimal file sharing server built with Flask. Upload files via a web UI or API, list available files, and download them. Files are stored safely in the `uploads/` folder, and original filenames are preserved for downloads.

### Features
- Simple web UI for uploading and downloading files
- Stores files under a safe name while keeping the original name for download links
- Shows "No data" when no files are present
- Works on Windows, macOS, and Linux

### Requirements
- Python 3.8+
- Pip

Dependencies are listed in `requirements.txt` and installed via pip.

### Project Structure
```
file-share-server/
  app.py
  requirements.txt
  templates/
    index.html
  uploads/            # auto-created on first run
  file_meta.json      # auto-created; maps original -> safe filename
```

### Setup (Windows)
```bat
cd C:\Users\Sainath\Desktop\New folder\file-share-server

:: Create and activate virtual environment
py -3 -m venv .venv
.venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Run the server
python app.py
```
Then open `http://localhost:8000/` in your browser.

### Setup (macOS/Linux)
```bash
cd /path/to/file-share-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Usage
- Open `http://localhost:8000/` and use the upload form.
- The files list shows all available files. If none exist, it shows "No data".
- Click the download button to download a file using its original filename.

### API Endpoints
- `GET /` – Web UI and list of files
- `POST /uploads` – Upload a file
  - Content-Type: `multipart/form-data`
  - Field name: `file`
  - Example (cross-platform):
    ```bash
    curl -F "file=@/path/to/example.txt" http://localhost:8000/uploads
    ```
- `GET /files/<filename>` – Download by original filename
  - URL-encode the filename (e.g., spaces as `%20`).
  - Example:
    ```bash
    curl -OJ "http://localhost:8000/files/my%20report.pdf"
    ```

### Configuration
- Upload directory: set by `UPLOAD_FOLDER` in `app.py` (default: `uploads`). The folder is auto-created.
- Port/host: set at the bottom of `app.py` in `app.run(host="0.0.0.0", port=8000, debug=True)`.

### How it works
- On upload, the app saves the file using `werkzeug.utils.secure_filename` into `uploads/`.
- It stores a mapping of `original -> safe` filename in `file_meta.json`.
- The index page builds the file list from actual files present in `uploads/` and the metadata, and displays an empty state when none are found.
- Downloads are served by original filename; the app looks up the safe filename from the metadata, or serves directly if it matches.

### Troubleshooting
- "No file uploaded" or "No selected file": ensure you chose a file and submitted the form.
- Uploads not saving:
  - Confirm the form uses `enctype="multipart/form-data"` and the file field name is `file`.
  - Ensure the process has write permissions to the `uploads/` folder.
- File list always shows "No data": check that files actually exist in `uploads/` and there are no permission issues.
- Download returns 404:
  - Verify the exact original filename and ensure it’s URL-encoded (spaces → `%20`).
  - Confirm the file exists on disk in `uploads/` and/or mapping exists in `file_meta.json`.
- Reset state: stop the server, delete all files in `uploads/` and remove `file_meta.json`, then restart the server.

### Notes
- This is a minimal demo; there is no authentication, authorization, or file size validation.
- Do not expose this server to the public internet without adding proper security and limits. 
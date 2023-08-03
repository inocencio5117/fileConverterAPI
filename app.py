from flask import Flask, request, jsonify
import pandas as pd
import os
import pdfkit
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"messge": "API is healthy!"})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['sample']
    if file and allowed_file(file.filename):
        # Save the file to a temporary location
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully.", "file_path": file_path})
    else:
        return jsonify({"error": "Invalid file format."}), 400

@app.route('/check_file', methods=['POST'])
def check_file():
    file = request.files['sample']
    if file and allowed_file(file.filename):
        return jsonify({"message": "the file sent is valid to convertion"})
    else:
        return jsonify({"error": "Invalid file path"}), 400

@app.route('/convert/csv', methods=['POST'])
def convert_to_csv():
    file_path = request.json.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid file path."}), 400

    # Read Excel data
    df = pd.read_excel(file_path)

    # Convert to CSV
    csv_path = os.path.splitext(file_path)[0] + '.csv'
    df.to_csv(csv_path, index=False)

    return jsonify({"message": "File converted to CSV.", "converted_file": csv_path})

@app.route('/convert/json', methods=['POST'])
def convert_to_json():
    file_path = request.json.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid file path."}), 400

    # Read Excel data
    df = pd.read_excel(file_path)

    # Convert to JSON
    json_path = os.path.splitext(file_path)[0] + '.json'
    df.to_json(json_path, orient='records')

    return jsonify({"message": "File converted to JSON.", "converted_file": json_path})

@app.route('/convert/pdf', methods=['POST'])
def convert_to_pdf():
    file_path = request.json.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid file path."}), 400

    # Read Excel data
    df = pd.read_excel(file_path)

    # Convert to PDF
    pdf_path = os.path.splitext(file_path)[0] + '.pdf'
    pdfkit.from_file(file_path, pdf_path)

    return jsonify({"message": "File converted to PDF.", "converted_file ": pdf_path})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS and \
           secure_filename(filename) == filename

if __name__ == '__main__':
    app.run()
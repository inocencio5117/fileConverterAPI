from flask import Flask, request, jsonify, Response
import pandas as pd
import pdfkit
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"messge": "API is healthy!"})

@app.route('/check_file', methods=['POST'])
def check_file():
    file = request.files['file']
    format_type = request.form.get('format_type', 'csv').lower()
    if file and allowed_file(file.filename):
        return jsonify({"message": "The file sent is valid to convertion", "format_type": format_type})
    else:
        return jsonify({"error": "Invalid file path"}), 400

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if file and allowed_file(file.filename):
        format_type = request.form.get('format_type', 'csv').lower()
        file.seek(0)
        converted_data, contetent_type = convert_and_respond(file, format_type)
        return Response(response=converted_data, status=200, mimetype=contetent_type)
    else:
        return jsonify({"error": "Invalid file format."}), 400

def convert_and_respond(file, format_type):
    df = pd.read_excel(file)

    if format_type == 'csv':
        converted_data = df.to_csv(index=False)
        content_type = 'text/csv'
    elif format_type == 'json':
        converted_data = df.to_json(orient='records')
        content_type = 'application/json'
    elif format_type == 'pdf':
        converted_data = pdfkit.from_string(df.to_html(index=False), False)
        content_type = 'application/pdf'
    else:
        return jsonify({"error": "Invalid format_type. Supported types: csv, json, pdf"}), 400

    return converted_data, content_type

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS and \
           secure_filename(filename) == filename

if __name__ == '__main__':
    app.run()
import os
from flask import Flask, send_from_directory, request, url_for, after_this_request
from flask import render_template
from excel_perser import ExcelParser
from file_reader import FileReader
import uuid


app = Flask(__name__)
UPLOAD_FOLDER = 'reports'
MAX_FILE_SIZE = 1024 * 1024 + 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def calculate(file_path, file_out_path):
    file_name = uuid.uuid4().hex
    with open(file_path) as file:
        text = file.readlines()
    calculating_data = FileReader(text, os.path.join(BASE_DIR, 'columns.json'))
    excel_parser = ExcelParser(calculating_data, file_out_path)
    excel_parser.export_document(file_name, calculating_data.columns)
    return file_name


@app.route('/', methods=['GET'])
def index():
    mydir = os.path.join(BASE_DIR, UPLOAD_FOLDER)
    filelist = [f for f in os.listdir(mydir) if f.endswith(".xlsx")]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

    return render_template("index.html")


@app.route('/save', methods=['POST'])
def report_save():
    file = request.files["file"]
    if bool(file.filename):

        # Вычисление путей.
        path_reports = os.path.join(BASE_DIR, UPLOAD_FOLDER)
        path_file = os.path.join(BASE_DIR, UPLOAD_FOLDER, file.filename)

        # Генерация Xlsx.
        file.save(path_file)
        report = calculate(path_file, path_reports)

        @after_this_request
        def remove_file(response):
            os.remove(path_file)
            return response

        return render_template("index.html", resp={"response": True, "message": "Файл успешно загружен !", "filename": report})


@app.route('/uploads/<filename>', methods=['GET'])
def report_down(filename):
    uploads = os.path.join(app.root_path, UPLOAD_FOLDER)
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000)
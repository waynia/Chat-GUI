from flask import Flask, render_template, request, make_response, redirect, url_for
import os
import re
import csv
from flask import jsonify
import openai

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"epub"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def parse_book(file_path):
    csv_file = file_path.rsplit(".", 1)[0] + ".csv"
    with open(csv_file, "w", newline="") as csvfile:
        csv.writer(csvfile)
    return csv_file


def check_api_key(api_key):
    openai.api_key = api_key

    try:
        openai.Model.list()
        return True
    except openai.error.AuthenticationError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def custom_secure_filename(filename):
    # 允许字母、数字、下划线、汉字、点和短横线，同时将其他字符替换为短横线（-）
    filename = re.sub(r'[^.\w\u4e00-\u9fa5-]', '-', filename)

    # 移除连续的短横线
    filename = re.sub(r'-+', '-', filename)

    # 移除文件名开始和结束处的短横线
    filename = filename.strip('-')

    # 限制文件名长度
    max_length = 255
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        name = name[:max_length - len(ext)]
        filename = name + ext

    return filename


@app.route("/check_api_key", methods=["POST"])
def check_api_key_route():
    api_key = request.form.get("api_key")
    is_valid = check_api_key(api_key)
    return jsonify({"is_valid": is_valid})


@app.route("/check_csv_file", methods=["GET"])
def check_csv_file():
    uploads_folder = os.path.join(os.getcwd(), 'uploads')
    csv_files = [f for f in os.listdir(uploads_folder) if f.endswith('.csv')]

    if csv_files:
        return jsonify({"csv_exists": True})
    else:
        return jsonify({"csv_exists": False})


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = custom_secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                csv_file = parse_book(file_path)
                resp = make_response(redirect(url_for("index")))
                resp.set_cookie("csv_file", csv_file)
                return resp
        else:
            openai_key = request.form["input1"]
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("openai_key", openai_key)
            return resp

    openai_key = request.cookies.get("openai_key")
    csv_file = request.cookies.get("csv_file")
    button_text = "Upload book" if openai_key else "OpenAI Key"
    placeholder_text = "Drop your epub book here" if openai_key else "Enter your OpenAI Key"
    return render_template("index.html", button_text=button_text, csv_file=csv_file, placeholder_text=placeholder_text)


@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    response = user_input * 3
    # 遍历 uploads 文件夹中的所有 CSV 文件
    uploads_folder = os.path.join(app.root_path, 'uploads')
    for filename in os.listdir(uploads_folder):
        if filename.endswith('.csv'):
            csv_path = os.path.join(uploads_folder, filename)
            with open(csv_path, newline='', encoding='utf-8') as csvfile:  # 读取CSV文件内容
                csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in csv_reader:
                    # 在这里处理 CSV 文件的每一行数据
                    print(', '.join(row))
    return jsonify({"response": "your_response_here"})


if __name__ == "__main__":
    app.run(debug=True)

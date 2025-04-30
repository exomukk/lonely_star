from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)



@app.route('/')
def dashboard():
    # Đọc dữ liệu JSON từ file
    with open('snyk_results.json', 'r') as f:
        snyk_data = json.load(f)

    # Truyền dữ liệu vào templates HTML
    return render_template('dashboard.html', vulnerabilities=snyk_data['vulnerabilities'])


if __name__ == '__main__':
    app.run(debug=True)
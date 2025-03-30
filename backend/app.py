from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Use CORS temporary for development

CORS(app, origins=["http:/localhost:3000"])

# Future configuration for production

@app.route('/')
@app.route('/index')
@app.route('/home')
def entrypoint():
    return "../main.html"



if __name__ == '__main__':
    app.run()

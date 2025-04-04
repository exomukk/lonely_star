from flask import Flask, request, jsonify
from flask_cors import CORS
import user.userController as userControllerInterface
app = Flask(__name__)

# Use CORS temporary for development

CORS(app, origins=["http://localhost:3000"])

# Future configuration for production

# Services importation
userController = userControllerInterface.userController()
@app.route('/')
@app.route('/index')
@app.route('/home')
def entrypoint():
    return "../main.html"

@app.route('/register', methods=['POST'])
def register():
    inputs = request.data.decode('utf-8')
    return jsonify(userController.register(inputs))

@app.route('/login', methods=['POST'])
def login():
    inputs = request.data.decode('utf-8')
    return jsonify(userController.login(inputs))



if __name__ == '__main__':
    app.run()

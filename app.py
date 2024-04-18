from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@projeficaz.fsc9tus.mongodb.net/biblioteca"
mongo = PyMongo(app)

@app.route('/usuarios', methods=['GET'])
def user_get():
    pass

@app.route('/usuarios', methods=['POST'])
def user_post():
    pass

@app.route('/usuarios', methods=['PUT'])
def user_put():
    pass

@app.route('/usuarios', methods=['DELETE'])
def user_delete():
    pass

@app.route('/bikes', methods=['GET'])
def bike_get():
    pass

@app.route('/bikes', methods=['POST'])
def bike_post():
    pass

@app.route('/bikes', methods=['PUT'])
def bike_put():
    pass

@app.route('/bikes', methods=['DELETE'])
def bike_delete():
    pass

@app.route('/emprestimos', methods=['GET'])
def emprestimo_get():
    pass

@app.route('/emprestimos', methods=['POST'])
def emprestimo_post():
    pass

@app.route('/emprestimos', methods=['DELETE'])
def emprestimo_delete():
    pass

if __name__ == '__main__':
    app.run(debug=True)
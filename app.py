from flask import Flask, request
from datetime import datetime
from bson import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@projeficaz.fsc9tus.mongodb.net/ap5"
mongo = PyMongo(app)

@app.route('/usuarios', methods=['GET'])
def user_get():
    filtro = {}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find(filtro, projecao)
    lista_user = list(dados_user)
    return {'usuarios': lista_user}, 200

@app.route('/usuarios/<string:id>', methods=['GET'])
def user_get_id(id):
    filtro = {"_id": ObjectId(id)}
    projecao = {'_id': 0}
    dados_user = mongo.db.usuarios.find_one(filtro, projecao)
    if dados_user is None:
        return {"erro": "usuário não encontrado"}, 404
    return {'usuarios': dados_user}, 200

@app.route('/usuarios', methods=['POST'])
def user_post():
    filtro = {}
    projecao = {'_id': 0}
    data = request.json
    dados_user = mongo.db.usuarios.find(filtro, projecao)
    lista_user = list(dados_user)
    for user in lista_user:
        if data['cpf'] == user['cpf']:
            return {"erro": "cpf já cadastrado"}, 400
    if data['cpf'] == " " or data['cpf'] == "":
        return {"erro": "cpf é obrigatório"}, 400
    
    result = mongo.db.usuarios.insert_one(data)
    return {"id": str(result.inserted_id)}, 201

@app.route('/usuarios/<string:id>', methods=['PUT'])
def user_put(id):
    filtro = {"_id": ObjectId(id)}
    projecao = {"_id": 0}
    data = request.json
    usuario_existente = mongo.db.usuarios.find_one(filtro, projecao)
    if usuario_existente is None:
        return {"erro": "usuário não encontrado"}, 404
    mongo.db.usuarios.update_one(filtro, {"$set": data})
    return {"mensagem": "alteração realizada com sucesso"}, 200

@app.route('/usuarios/<string:id>', methods=['DELETE'])
def user_delete(id):
    filtro ={"_id": ObjectId(id)}
    projecao = {'_id': 0}
    usuario_existente = mongo.db.usuarios.find_one(filtro, projecao)
    if usuario_existente is None:
        return {"erro": "usuário não encontrado"}, 404
    else:
        delete = mongo.db.usuarios.delete_one(filtro)
    
    return {"mensagem": "usuário deletado com sucesso"}, 200

@app.route('/bikes', methods=['GET'])
def bike_get():
    filtro = {}
    projecao = {'_id': 0}
    dados_bike = mongo.db.bikes.find(filtro, projecao)
    lista_bike = list(dados_bike)
    return {'bike': lista_bike}, 200

@app.route('/bikes/<string:id>', methods=['GET'])
def bike_get_id():
    filtro = {"_id": ObjectId(id)}
    projecao = {'_id': 0}
    dados_bike = mongo.db.bikes.find_one(filtro, projecao)
    return {'bike': dados_bike}, 200

@app.route('/bikes', methods=['POST'])
def bike_post():
    filtro = {}
    projecao = {'_id': 0}
    data = request.json
    dados_bike = mongo.db.bikes.find_one(filtro, projecao)
    result = mongo.db.bikes.insert_one(data)
    return {"id": str(result.inserted_id)}, 201

@app.route('/bikes/<string:id>', methods=['PUT'])
def bike_put():
    filtro = {"_id": ObjectId(id)}
    projecao = {"_id": 0}
    data = request.json
    bike_existente = mongo.db.bikes.find_one(filtro, projecao)
    if bike_existente is None:
        return {"erro": "bike não encontrada"}, 404
    mongo.db.bikes.update_one(filtro, {"$set": data})
    return {"mensagem": "alteração realizada com sucesso"}, 200

@app.route('/bikes<string:id>', methods=['DELETE'])
def bike_delete(id):
    filtro = {"_id": ObjectId(id)}
    projecao = {'_id': 0}
    bike_existente = mongo.db.bikes.find_one(filtro, projecao)
    if bike_existente is None:
        return {"erro": "bike não encontrada"}, 404
    else:
        delete = mongo.db.bikes.delete_one(filtro)
    
    return {"mensagem": "bike deletada com sucesso"}, 200

#-------------------------------------------------------------------------------------
@app.route('/emprestimos', methods=['GET'])
def emprestimo_get_all():
    filtro = {"_id": ObjectId(id)}
    projecao = {'_id': 0}
    emprestimos = mongo.db.emprestimos.find(filtro, projecao)
    lista_emprestimos = list(emprestimos)
    return {'emprestimos': lista_emprestimos}, 200

@app.route('/emprestimos/<string:id>', methods=['GET'])
def emprestimo_get_by_id(id):
    filtro = {"_id": ObjectId(id)}
    projecao = {'_id': 0}
    emprestimo = mongo.db.emprestimos.find_one(filtro, projecao)
    if emprestimo is None:
        return {'erro': 'emprestimo não encontrado'}, 404
    return {'emprestimo': emprestimo}

@app.route('/emprestimos/usuarios/<string:id_usuario>/bikes/<string:id_bike>', methods=['POST'])
def emprestimo_post(id_usuario, id_bike):
    filtro_bike = {"_id": ObjectId(id_bike)}
    bike = mongo.db.bikes.find_one(filtro_bike)
    data = request.json
    if bike is None:
        return {'erro': 'bicicleta não encontrada'}, 404
    if 'emprestimo' in bike:
        return {'erro': 'bicicleta já está alugada'}, 400
    filtro_usuario = {"_id": ObjectId(id_usuario)}
    user = mongo.db.usuarios.find_one(filtro_usuario)
    if user is None:
        return {'erro': 'usuário não encontrado'}, 404
    emprestimo = {
        'bike_id': id_bike,
        'user_id': id_usuario,
        'data_aluguel': datetime.now()
    }
    mongo.db.emprestimos.insert_one(emprestimo)
    mongo.db.bikes.update_one({"_id": ObjectId(id_usuario)}, {'$set': {'emprestimo': emprestimo}})
    return {'mensagem': 'emprestimo registrado com sucesso'}, 201

@app.route('/emprestimos/<string:id>', methods=['DELETE'])
def emprestimo_delete(id):
    filtro = {"_id": ObjectId(id)}
    emprestimo = mongo.db.emprestimos.find_one(filtro)
    if emprestimo is None:
        return {'erro': 'emprestimo não encontrado'}, 404
    bike_id = emprestimo['bike_id']
    mongo.db.bikes.update_one({"_id": ObjectId(bike_id)}, {'$unset': {'emprestimo': ''}})
    mongo.db.emprestimos.delete_one(filtro)
    return {'mensagem': 'emprestimo deletado com sucesso'}, 200

if __name__ == '__main__':
    app.run(debug=True)
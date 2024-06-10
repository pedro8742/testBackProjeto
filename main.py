import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('carros.db')
cursor = conn.cursor()

# Criar tabela para carros
cursor.execute('''
CREATE TABLE IF NOT EXISTS carros (
    id INTEGER PRIMARY KEY,
    marca TEXT,
    modelo TEXT,
    ano INTEGER
)
''')
conn.commit()

# Adicionar alguns carros iniciais
cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Toyota', 'Corolla', 2020))
cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Honda', 'Civic', 2019))
cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Ford', 'Fiesta', 2022))
cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Ford', 'Focus', 2023))
conn.commit()

# Função para adicionar um carro
@app.route('/adicionar', methods=['POST'])
def adicionar_carro():
    data = request.get_json()
    marca = data['marca']
    modelo = data['modelo']
    ano = data['ano']
    cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', (marca, modelo, ano))
    conn.commit()
    return jsonify({'message': 'Carro adicionado com sucesso!'})

# Função para listar todos os carros
@app.route('/listar', methods=['GET'])
def listar_carros():
    cursor.execute('SELECT * FROM carros')
    carros = cursor.fetchall()
    return jsonify(carros)

# Função para atualizar um carro
@app.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_carro(id):
    data = request.get_json()
    marca = data['marca']
    modelo = data['modelo']
    ano = data['ano']
    cursor.execute('UPDATE carros SET marca=?, modelo=?, ano=? WHERE id=?', (marca, modelo, ano, id))
    conn.commit()
    return jsonify({'message': 'Carro atualizado com sucesso!'})

# Função para excluir um carro
@app.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_carro(id):
    cursor.execute('DELETE FROM carros WHERE id=?', (id,))
    conn.commit()
    return jsonify({'message': 'Carro excluído com sucesso!'})

if __name__ == '__main__':
    app.run()
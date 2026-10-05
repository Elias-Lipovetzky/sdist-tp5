from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

#CORS(app, origins="http://localhost:3000")

@app.get("/api/usuarios")
def usuarios():
    return jsonify([
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Juan"}
    ])

@app.post("/api/usuarios")
def crear():
    return jsonify(request.json)

app.run(port=5000)

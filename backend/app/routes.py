from flask import Flask, url_for, redirect, Blueprint, render_template, request,jsonify


routes = Blueprint('routes', __name__)

@routes.route('/')
def inicio():
    return render_template('inicio.html')

#metodo que maneja la carga de archivos desde la pagina
@routes.route('/upload', methods = ['POST'])
def upload():
    #verificacion de que el archivo exista y se haya seleccionado
    if 'file' not in request.files:
        return jsonify({"error" : "no file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error" : "no selected file"}), 400
    
    #leemos el contenido del archivo
    content = file.read().decode('utf-8')

    #devolvemos el contenido dentro del JSON
    return jsonify({"content" : content})
    
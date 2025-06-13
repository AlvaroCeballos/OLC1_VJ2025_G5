from flask import Flask, url_for, redirect, Blueprint, render_template, request

routes = Blueprint('routes', __name__)

@routes.route('/')
def inicio():
    return render_template('inicio.html')


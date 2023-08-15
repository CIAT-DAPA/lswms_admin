from flask import Blueprint, render_template, redirect, request
from ormWP import Adm1
from datetime import datetime
adm1_bp = Blueprint('adm1', __name__)

@adm1_bp.route('/')
def mostrar_usuarios():
    adm1 = Adm1.objects()
    return render_template('adm1.html', adm1=adm1)

@adm1_bp.route('/adm1/add', methods=['POST'])
def agregar_usuario():
    nombre = request.form['name']
    ext_id = request.form['ext_id']
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    nuevo_usuario = Adm1(name=nombre, ext_id=ext_id,trace=traced)
    nuevo_usuario.save()
    
    return redirect('/')

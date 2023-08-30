from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Wscontent
from ormWP import Watershed
from ormWP import Typecontent
from datetime import datetime
wscontent_bp = Blueprint('wscontent', __name__)

@wscontent_bp.route('/wscontent')
def show_wscontent():
    wscontent = Wscontent.objects()
    watershed= Watershed.objects()
    typecontent= Typecontent.objects()
    options = ['icon-x', 'icon-y', 'list', 'text']
    positions=['left','right']

    

    

    return render_template('wscontent.html', wscontent=wscontent,watershed=watershed,typecontent=typecontent,options=options,positions=positions)
@wscontent_bp.route('/wscontent/add', methods=['GET', 'POST'])
def add_wpcontent():
    if request.method == 'POST':
        # Obtener los datos del formulario
        title = request.form['title']
        typecontent = request.form['typecontent']
        type = request.form['type']
        selectedtype=Typecontent.objects.get(id=typecontent)
        position = request.form['position']
        watershed = request.form['watershed']
        selected_watershed= Watershed.objects.get(id=watershed)
        keys = request.form.getlist('keys[]') 
        traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
         # Obtener una lista de keys
        values = request.form.getlist('values[]')  # Obtener una lista de values
        content={
            'title': title,
            'type': type,
            'position': position,
            'values': [{k:v} for k, v in zip(keys, values)],
            'trace':traced
        }
        # Crear un objeto que contenga title, type, position y los pares key-value
        wscontent_obj = Wscontent(type=selectedtype,watershed=selected_watershed,content=content) 

        # Agregar el objeto a la lista
        wscontent_obj.save()

        flash("ws content added successfully")
    return redirect('/wscontent')


@wscontent_bp.route('/editwscontent/<string:id_wscontent>', methods=['GET', 'POST'])
def edit_wscontent(id_wscontent):
    wscontent = Wscontent.objects(id=id_wscontent).first()
    print(wscontent.content)
    watershed= Watershed.objects()
    typecontent= Typecontent.objects()
    options = ['icon-x', 'icon-y', 'list', 'text']
    positions=['left','right']


    if request.method == 'POST':
        # Obtener los datos del formulario editado
        title = request.form['title']
        typecontent = request.form['typecontent']
        type = request.form['type']
        selectedtype=Typecontent.objects.get(id=typecontent)
        position = request.form['position']
        watershed = request.form['watershed']
        selected_watershed= Watershed.objects.get(id=watershed)
        keys = request.form.getlist('keys[]')
        values = request.form.getlist('values[]')
        content={
            'title': title,
            'type': type,
            'position': position,
            'values': [{k:v} for k, v in zip(keys, values)]
        }
        wscontent.update(content=content,type=selectedtype,watershed=selected_watershed)
        # Actualizar el documento en la base de datos
        flash("ws Content updated successfully")
        

        # Redirigir a una página de éxito o mostrar un mensaje de éxito
        return redirect('/wscontent')
    return render_template('edit_ws_content.html', wscontent=wscontent,watershed=watershed,typecontent=typecontent,options=options,positions=positions)
    

    # Obtener el documento con el ID proporcionado
    

@wscontent_bp.route('/deletewscontent/<string:wscontent_id>')
def delete_wpcontent(wscontent_id):
    wscontent = Wscontent.objects(id=wscontent_id).first()

    if wscontent:
        wscontent.delete()
        flash("wscontent deleted successfully")
    else:
        flash("wscontent not found")

    return redirect('/wscontent')
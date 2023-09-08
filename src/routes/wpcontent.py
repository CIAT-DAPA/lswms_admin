from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Wpcontent
from ormWP import Waterpoint
from ormWP import Typecontent
from datetime import datetime
wpcontent_bp = Blueprint('wpcontent', __name__)

@wpcontent_bp.route('/wpcontent')
def show_wpcontent():
    wpcontent = Wpcontent.objects()
    waterpoint= Waterpoint.objects()
    typecontent= Typecontent.objects()
    options = ['icon-x', 'icon-y', 'list', 'text']
    positions=['left','right']
    languages = [
        {'label': 'Amharic', 'value': 'am'},
        {'label': 'Afaan Oromo', 'value': 'or'},
        {'label': 'English', 'value': 'en'},
    ]

    
    return render_template('wpcontent.html', wpcontent=wpcontent,waterpoint=waterpoint,typecontent=typecontent,options=options,positions=positions,languages=languages)
@wpcontent_bp.route('/wpcontent/add', methods=['GET', 'POST'])
def add_wpcontent():
    if request.method == 'POST':
        # Obtener los datos del formulario
        title = request.form['title']
        typecontent = request.form['typecontent']
        type = request.form['type']
        selectedtype=Typecontent.objects.get(id=typecontent)
        position = request.form['position']
        waterpoint = request.form['waterpoint']
        language = request.form['language']
        selected_waterpoint= Waterpoint.objects.get(id=waterpoint)
        keys = request.form.getlist('keys[]') 
        traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
         # Obtener una lista de keys
        values = request.form.getlist('values[]')  # Obtener una lista de values
        content={
            'title': title,
            'type': type,
            'position': position,
            'language':language,
            'values': [{k:v} for k, v in zip(keys, values)],
            'trace':traced
        }
        # Crear un objeto que contenga title, type, position y los pares key-value
        wpcontent_obj = Wpcontent(type=selectedtype,waterpoint=selected_waterpoint,content=content) 

        # Agregar el objeto a la lista
        wpcontent_obj.save()

        flash("wp content added successfully")
    return redirect('/wpcontent')


@wpcontent_bp.route('/editwpcontent/<string:id_wpcontent>', methods=['GET', 'POST'])
def edit_wpcontent(id_wpcontent):
    wpcontent = Wpcontent.objects(id=id_wpcontent).first()
    waterpoint= Waterpoint.objects()
    typecontent= Typecontent.objects()
    

    options = ['icon-x', 'icon-y', 'list', 'text']
    positions=['left','right']
    languages = [
        {'label': 'Amharic', 'value': 'am'},
        {'label': 'Afaan Oromo', 'value': 'or'},
        {'label': 'English', 'value': 'en'},
    ]

    if request.method == 'POST':
        # Obtener los datos del formulario editado
        
        title = request.form['title']
        typecontent = request.form['typecontent']
        type = request.form['type']
        selectedtype=Typecontent.objects.get(id=typecontent)
        position = request.form['position']
        language=request.form['language']
        waterpoint = request.form['waterpoint']
        selected_waterpoint= Waterpoint.objects.get(id=waterpoint)
        keys = request.form.getlist('keys[]')
        values = request.form.getlist('values[]')
        wpcontent.content['trace']['updated'] = datetime.now()
        content={
            'title': title,
            'type': type,
            'position': position,
            'language':language,
            'trace':wpcontent.content['trace'],
            'values': [{k:v} for k, v in zip(keys, values)]
        }
        wpcontent.update(content=content,type=selectedtype,waterpoint=selected_waterpoint)
        
        flash("Content updated successfully")
        

       
        return redirect('/wpcontent')
    return render_template('edit_wp_content.html', wpcontent=wpcontent,waterpoint=waterpoint,typecontent=typecontent,options=options,positions=positions,languages=languages)
    

  
    

@wpcontent_bp.route('/deletewpcontent/<string:wpcontent_id>')
def delete_wpcontent(wpcontent_id):
    wpcontent = Wpcontent.objects(id=wpcontent_id).first()

    if wpcontent:
        wpcontent.delete()
        flash("wpcontent deleted successfully")
    else:
        flash("wpcontent not found")

    return redirect('/wpcontent')

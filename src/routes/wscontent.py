from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Wscontent
from ormWP import Watershed
from ormWP import Typecontent
from datetime import datetime
wscontent_bp = Blueprint('wscontent', __name__)

@wscontent_bp.route('/wscontent')
def show_wscontent():
    wscontent = Wscontent.objects()
    watershed= Watershed.objects(trace__enabled=True)
    typecontent= Typecontent.objects(trace__enabled=True)
    options = ['icon-x', 'icon-y', 'simple-list','complex-list', 'text','table']

    positions=['left','right']
    languages = [
        {'label': 'Amharic', 'value': 'am'},
        {'label': 'Afaan Oromo', 'value': 'or'},
        {'label': 'English', 'value': 'en'},
    ]

    

    return render_template('wscontent.html', wscontent=wscontent,watershed=watershed,typecontent=typecontent,options=options,positions=positions,languages=languages)

@wscontent_bp.route('/addwscontent')
def addd_wscontent():
    wscontent = Wscontent.objects(content__trace__enabled=True)
    watershed= Watershed.objects(trace__enabled=True)
    typecontent= Typecontent.objects(trace__enabled=True)
    options = ['icon-x', 'icon-y', 'simple-list','complex-list', 'text','table']

    positions=['left','right']
    languages = [
        {'label': 'Amharic', 'value': 'am'},
        {'label': 'Afaan Oromo', 'value': 'or'},
        {'label': 'English', 'value': 'en'},
    ]

    

    return render_template('addWscontent.html', wscontent=wscontent,watershed=watershed,typecontent=typecontent,options=options,positions=positions,languages=languages)

@wscontent_bp.route('/wscontent/add', methods=['GET', 'POST'])
def add_wscontent():
    if request.method == 'POST':
        # Obtener los datos del formulario
        title = request.form['title']
        typecontent = request.form['typecontent']
        type = request.form['type']
        selectedtype=Typecontent.objects.get(id=typecontent)
        position = request.form['position']
        watershed = request.form['watershed']
        language = request.form['language']
        selected_watershed= Watershed.objects.get(id=watershed)
        keys = request.form.getlist('keys[]') 
        traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
         # Obtener una lista de keys
        values = request.form.getlist('values[]') 
        position_type_weights = {
            ('left', 'table'): 0,
            ('left', 'simple-list'): 1,
            ('left', 'complex-list'): 2,
            ('left', 'icon-x'): 3,
            ('left', 'icon-y'): 4,
            ('left', 'text'): 5,
            ('right', 'table'): 5,
            ('right', 'complex-list'): 4,
            ('right', 'simple-list'): 3,
            ('right', 'icon-x'): 2,
            ('right', 'icon-y'): 1,
            ('right', 'text'): 0,
        }
        weight = position_type_weights.get((position, type), None) # Obtener una lista de values
        if weight is not None:
            content={
                'title': title,
                'type': type,
                'position': position,
                'language':language,
                'values': [{k:v} for k, v in zip(keys, values)],
                'weight':weight,
                'trace':traced
            }
        # Crear un objeto que contenga title, type, position y los pares key-value
            wscontent_obj = Wscontent(type=selectedtype,watershed=selected_watershed,content=content) 

        # Agregar el objeto a la lista
            wscontent_obj.save()

            flash("ws content added successfully")
        else:
    # En caso de que no se encuentre un peso válido, manejarlo según corresponda
            flash("Invalid position or type")
    return redirect('/wscontent')


@wscontent_bp.route('/editwscontent/<string:id_wscontent>', methods=['GET', 'POST'])
def edit_wscontent(id_wscontent):
    wscontent = Wscontent.objects(id=id_wscontent).first()
    print(wscontent.content)
    watershed= Watershed.objects()
    typecontent= Typecontent.objects()
    options = ['icon-x', 'icon-y', 'simple-list','complex-list', 'text']
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
        language = request.form['language']

        selectedtype=Typecontent.objects.get(id=typecontent)
        position = request.form['position']
        watershed = request.form['watershed']
        selected_watershed= Watershed.objects.get(id=watershed)
        keys = request.form.getlist('keys[]')
        values = request.form.getlist('values[]')
        wscontent.content['trace']['updated'] = datetime.now()
        position_type_weights = {
            ('left', 'table'): 0,
            ('left', 'simple-list'): 1,
            ('left', 'complex-list'): 2,
            ('left', 'icon-x'): 3,
            ('left', 'icon-y'): 4,
            ('left', 'text'): 5,
            ('right', 'table'): 5,
            ('right', 'complex-list'): 4,
            ('right', 'simple-list'): 3,
            ('right', 'icon-x'): 2,
            ('right', 'icon-y'): 1,
            ('right', 'text'): 0,
        }
        weight = position_type_weights.get((position, type), None)
        if weight is not None:
            content={
                'title': title,
                'type': type,
                'position': position,
                'language':language,
                'trace':wscontent.content['trace'],
                'weight':weight,
                'values': [{k:v} for k, v in zip(keys, values)]
            }
            wscontent.update(content=content,type=selectedtype,watershed=selected_watershed)
            # Actualizar el documento en la base de datos
            flash("ws Content updated successfully")
        else:
    # En caso de que no se encuentre un peso válido, manejarlo según corresponda
            flash("Invalid position or type")

        # Redirigir a una página de éxito o mostrar un mensaje de éxito
        return redirect('/wscontent')
    return render_template('edit_ws_content.html', wscontent=wscontent,watershed=watershed,typecontent=typecontent,options=options,positions=positions,languages=languages)
    

    # Obtener el documento con el ID proporcionado
    

@wscontent_bp.route('/deletewscontent/<string:wscontent_id>')
def delete_wpcontent(wscontent_id):
    wscontent = Wscontent.objects(id=wscontent_id).first()

    if wscontent:
        if 'content' in wscontent and 'trace' in wscontent.content:
            # Utiliza update para modificar el documento en lugar de cargarlo completo
            Wscontent.objects(id=wscontent_id).update(set__content__trace__enabled=False)

            flash("wscontent deleted successfully")
        else:
            flash("Content or Trace not found in wscontent")
    else:
        flash("wscontent not found")

    return redirect('/wscontent')
@wscontent_bp.route('/resetwscontent/<string:wscontent_id>')
def recover_wscontent(wscontent_id):
    wscontent = Wscontent.objects(id=wscontent_id).first()

    if wscontent:
        if 'content' in wscontent and 'trace' in wscontent.content:
            # Utiliza update para modificar el documento en lugar de cargarlo completo
            Wscontent.objects(id=wscontent_id).update(set__content__trace__enabled=True)

            flash("wscontent recover successfully")
        else:
            flash("Content or Trace not found in wscontent")
    else:
        flash("wpcontent not found")

    return redirect('/wscontent')

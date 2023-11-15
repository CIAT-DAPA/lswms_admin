from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Wpcontent
from ormWP import Waterpoint
from ormWP import Typecontent
from datetime import datetime
from flask_login import login_required  
wpcontent_bp = Blueprint('wpcontent', __name__)

@wpcontent_bp.route('/wpcontent')
@login_required
def show_wpcontent():
    wpcontent = Wpcontent.objects()
    waterpoint= Waterpoint.objects(trace__enabled=True)
    typecontent= Typecontent.objects(trace__enabled=True)
    options = ['icon-x', 'icon-y', 'simple-list','complex-list', 'text','table']
    positions=['left','right']
    languages = [
        {'label': 'Amharic', 'value': 'am'},
        {'label': 'Afaan Oromo', 'value': 'or'},
        {'label': 'English', 'value': 'en'},
    ]

    
    return render_template('wpcontent.html', wpcontent=wpcontent,waterpoint=waterpoint,typecontent=typecontent,options=options,positions=positions,languages=languages)
@wpcontent_bp.route('/addwpcontent')
@login_required
def addd_wpcontent():
    wpcontent = Wpcontent.objects(content__trace__enabled=True)
    waterpoint= Waterpoint.objects(trace__enabled=True)
    typecontent= Typecontent.objects(trace__enabled=True)
    options = ['icon-x', 'icon-y', 'simple-list','complex-list', 'text','table']
    positions=['left','right']
    languages = [
        {'label': 'Amharic', 'value': 'am'},
        {'label': 'Afaan Oromo', 'value': 'or'},
        {'label': 'English', 'value': 'en'},
    ]

    
    return render_template('addWpcontent.html', wpcontent=wpcontent,waterpoint=waterpoint,typecontent=typecontent,options=options,positions=positions,languages=languages)


@wpcontent_bp.route('/wpcontent/add', methods=['GET', 'POST'])
@login_required
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
        weight = position_type_weights.get((position, type), None)

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
            wpcontent_obj = Wpcontent(type=selectedtype,waterpoint=selected_waterpoint,content=content) 

            # Agregar el objeto a la lista
            wpcontent_obj.save()

            flash("wp content added successfully")
        else:
    # En caso de que no se encuentre un peso válido, manejarlo según corresponda
            flash("Invalid position or type")
    return redirect('/wpcontent')


@wpcontent_bp.route('/editwpcontent/<string:id_wpcontent>', methods=['GET', 'POST'])
@login_required
def edit_wpcontent(id_wpcontent):
    wpcontent = Wpcontent.objects(id=id_wpcontent).first()
    waterpoint= Waterpoint.objects()
    typecontent= Typecontent.objects()
    

    options = ['icon-x', 'icon-y', 'simple-list','complex-list', 'text','table']

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
            
            content = {
                'title': title,
                'type': type,
                'position': position,
                'language': language,
                'values': [{k: v} for k, v in zip(keys, values)],
                'weight': weight,
                'trace': wpcontent.content['trace'],
            }
            wpcontent.update(content=content,type=selectedtype,waterpoint=selected_waterpoint)
        
            flash("Content updated successfully")
        else:
   
            flash("Invalid position or type")

        

       
        return redirect('/wpcontent')
    return render_template('edit_wp_content.html', wpcontent=wpcontent,waterpoint=waterpoint,typecontent=typecontent,options=options,positions=positions,languages=languages)
    

  
    

@wpcontent_bp.route('/deletewpcontent/<string:wpcontent_id>')
@login_required
def delete_wpcontent(wpcontent_id):
    wpcontent = Wpcontent.objects(id=wpcontent_id).first()

    if wpcontent:
        if 'content' in wpcontent and 'trace' in wpcontent.content:
           
            Wpcontent.objects(id=wpcontent_id).update(set__content__trace__enabled=False)

            flash("wpcontent deleted successfully")
        else:
            flash("Content or Trace not found in wpcontent")
    else:
        flash("wpcontent not found")

    return redirect('/wpcontent')

@wpcontent_bp.route('/resetwpcontent/<string:wpcontent_id>')
@login_required
def recover_wpcontent(wpcontent_id):
    wpcontent = Wpcontent.objects(id=wpcontent_id).first()

    if wpcontent:
        if 'content' in wpcontent and 'trace' in wpcontent.content:
            
            Wpcontent.objects(id=wpcontent_id).update(set__content__trace__enabled=True)

            flash("wpcontent recover successfully")
        else:
            flash("Content or Trace not found in wpcontent")
    else:
        flash("wpcontent not found")

    return redirect('/wpcontent')

@wpcontent_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401
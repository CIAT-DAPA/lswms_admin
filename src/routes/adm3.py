from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Adm1
from ormWP import Adm2
from ormWP import Adm3
from datetime import datetime
adm3_bp = Blueprint('adm3', __name__)

@adm3_bp.route('/adm3')
def show_adm3():
    adm3 = Adm3.objects()
    adm2 = Adm2.objects(trace__enabled=True)
    return render_template('adm3.html', adm3=adm3, adm2=adm2)

@adm3_bp.route('/addadm3')
def addd_adm3():
    adm3 = Adm3.objects(trace__enabled=True)
    adm2 = Adm2.objects(trace__enabled=True)
    return render_template('addAdm3.html', adm3=adm3, adm2=adm2)

@adm3_bp.route('/adm3/add', methods=['POST'])
def add_adm3():
    name = request.form['name']
    ext_id = request.form['ext_id']
    adm2_id = request.form['adm2'] 
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    adm3 = Adm3(name=name, ext_id=ext_id,trace=traced,adm2=adm2_id)
    adm3.save()
    flash("Adm3 added succesfully")
    return redirect('/adm3')

@adm3_bp.route('/editadm3/<string:adm3_id>', methods=['GET', 'POST'])
def edit_adm3(adm3_id):
    adm3 = Adm3.objects(id=adm3_id).first()
    adm2=Adm2.objects()
    
    
    if request.method == 'POST':
        nombre = request.form['name']
        ext_id = request.form['ext_id']
        trace = adm3.trace
        adm2_id = request.form['adm2'] 
        selected_adm2 = Adm2.objects.get(id=adm2_id)
        trace['updated'] = datetime.now()
        adm3.update(name=nombre, ext_id=ext_id, trace=trace,adm2=selected_adm2)

        flash("Adm3 updated successfully")
        return redirect('/adm3')

    return render_template('edit_adm3.html', adm3=adm3,adm2=adm2)

@adm3_bp.route('/deleteadm3/<string:adm3_id>')
def delete_adm3(adm3_id):
    adm3 = Adm3.objects(id=adm3_id).first()

    if adm3:
        trace = adm3.trace

        trace['enabled'] = False
        adm3.update(trace=trace)
        flash("Adm3 deleted successfully")
    else:
        flash("Adm3 not found")

    return redirect('/adm3')

@adm3_bp.route('/resetadm3/<string:adm3_id>')
def reset_adm2(adm3_id):
    adm3 = Adm3.objects(id=adm3_id).first()

    if adm3:
        trace = adm3.trace

        trace['enabled'] = True
        adm3.update(trace=trace)
        flash("Adm3 recover successfully")
    else:
        flash("Adm3 not found")

    return redirect('/adm3')



from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Adm1
from ormWP import Adm2
from datetime import datetime
adm2_bp = Blueprint('adm2', __name__)

@adm2_bp.route('/adm2')
def show_adm2():
    adm2 = Adm2.objects(trace__enabled=True)
    adm1 = Adm1.objects(trace__enabled=True)

    return render_template('adm2.html', adm2=adm2, adm1=adm1)

@adm2_bp.route('/addadm2')
def addd_adm2():
    adm2 = Adm2.objects(trace__enabled=True)
    adm1 = Adm1.objects(trace__enabled=True)

    return render_template('addAdm2.html', adm2=adm2, adm1=adm1)
@adm2_bp.route('/adm2/add', methods=['POST'])
def add_adm2():
    name = request.form['name']
    ext_id = request.form['ext_id']
    adm1_id = request.form['adm1'] 
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    adm2 = Adm2(name=name, ext_id=ext_id,trace=traced,adm1=adm1_id)
    adm2.save()
    flash("Adm2 added succesfully")
    return redirect('/adm2')

@adm2_bp.route('/editadm2/<string:adm2_id>', methods=['GET', 'POST'])
def edit_adm2(adm2_id):
    adm2 = Adm2.objects(id=adm2_id).first()
    adm1=Adm1.objects()
    
    
    if request.method == 'POST':
        nombre = request.form['name']
        ext_id = request.form['ext_id']
        trace = adm2.trace
        adm1_id = request.form['adm1'] 
        selected_adm1 = Adm1.objects.get(id=adm1_id)
        trace['updated'] = datetime.now()
        adm2.update(name=nombre, ext_id=ext_id, trace=trace,adm1=selected_adm1)

        flash("Adm2 updated successfully")
        return redirect('/adm2')

    return render_template('edit_adm2.html', adm2=adm2,adm1=adm1)

@adm2_bp.route('/deleteadm2/<string:adm2_id>')
def delete_adm2(adm2_id):
    adm2 = Adm2.objects(id=adm2_id).first()
    

    if adm2:
        trace = adm2.trace

        trace['enabled'] = False
        adm2.update(trace=trace)
        flash("Adm2 deleted successfully")
    else:
        flash("Adm2 not found")

    return redirect('/adm2')



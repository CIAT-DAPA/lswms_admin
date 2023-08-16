from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Adm1
from datetime import datetime
adm1_bp = Blueprint('adm1', __name__)

@adm1_bp.route('/')
def show_adm1():
    adm1 = Adm1.objects()
    return render_template('adm1.html', adm1=adm1)

@adm1_bp.route('/adm1/add', methods=['POST'])
def add_adm1():
    name = request.form['name']
    ext_id = request.form['ext_id']
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    adm1 = Adm1(name=name, ext_id=ext_id,trace=traced)
    adm1.save()
    flash("Adm1 added succesfully")
    return redirect('/')

@adm1_bp.route('/edit/<string:adm1_id>', methods=['GET', 'POST'])
def edit_adm1(adm1_id):
    adm1 = Adm1.objects(id=adm1_id).first()
    """ json_data = [{"id":str(x.id),"name":x.name,"ext_id":x.ext_id} for x in adm1] """
    
    if request.method == 'POST':
        nombre = request.form['name']
        ext_id = request.form['ext_id']
        trace = adm1.trace
        trace['updated'] = datetime.now()
        adm1.update(name=nombre, ext_id=ext_id, trace=trace)

        flash("Adm1 updated successfully")
        return redirect('/')

    return render_template('edit_adm1.html', adm1=adm1)

@adm1_bp.route('/delete/<string:adm1_id>')
def delete_adm1(adm1_id):
    adm1 = Adm1.objects(id=adm1_id).first()

    if adm1:
        adm1.delete()
        flash("Adm1 deleted successfully")
    else:
        flash("Adm1 not found")

    return redirect('/')



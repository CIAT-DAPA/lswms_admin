from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from ormWP import Adm1
from datetime import datetime

adm1_bp = Blueprint('adm1', __name__)

@adm1_bp.route('/adm1')
@login_required 
def show_adm1():
    adm1 = Adm1.objects()
    return render_template('adm1.html', adm1=adm1)
@login_required
@adm1_bp.route('/addadm1')
def addd_adm1():
    adm1 = Adm1.objects(trace__enabled=True)
    return render_template('addAdm1.html', adm1=adm1)

@adm1_bp.route('/adm1/add', methods=['POST'])
@login_required
def add_adm1():
    name = request.form['name']
    ext_id = request.form['ext_id']
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    adm1 = Adm1(name=name, ext_id=ext_id,trace=traced)
    adm1.save()
    flash("Adm1 added succesfully")
    return redirect('/adm1')

@adm1_bp.route('/edit/<string:adm1_id>', methods=['GET', 'POST'])
@login_required
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
        return redirect('/adm1')

    return render_template('edit_adm1.html', adm1=adm1)

@adm1_bp.route('/delete/<string:adm1_id>')
@login_required
def delete_adm1(adm1_id):
    adm1 = Adm1.objects(id=adm1_id).first()

    if adm1:
        trace = adm1.trace

        trace['enabled'] = False
        adm1.update(trace=trace)
        flash("Adm1 deleted successfully")
    else:
        flash("Adm1 not found")

    return redirect('/adm1')

@adm1_bp.route('/reset/<string:adm1_id>')
@login_required
def reset_adm1(adm1_id):
    adm1 = Adm1.objects(id=adm1_id).first()

    if adm1:
        trace = adm1.trace

        trace['enabled'] = True
        adm1.update(trace=trace)
        flash("Adm1 recover successfully")
    else:
        flash("Adm1 not found")

    return redirect('/adm1')

@adm1_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401


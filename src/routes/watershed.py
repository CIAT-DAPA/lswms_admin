from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Adm1
from ormWP import Adm2
from ormWP import Adm3
from ormWP import Watershed
from datetime import datetime
from flask_login import login_required  

watershed_bp = Blueprint('watershed', __name__)

@watershed_bp.route('/watershed')
@login_required
def show_watershed():
    watershed = Watershed.objects()
    adm3 = Adm3.objects(trace__enabled=True)
    return render_template('watershed.html', watershed=watershed, adm3=adm3)

@watershed_bp.route('/addwatershed')
@login_required
def addd_watershed():
    watershed = Watershed.objects(trace__enabled=True)
    adm3 = Adm3.objects(trace__enabled=True)
    return render_template('addWatershed.html', watershed=watershed, adm3=adm3)


@watershed_bp.route('/watershed/add', methods=['POST'])
@login_required
def add_wateshed():
    name = request.form['name']
    area = request.form['area']
    adm3_id = request.form['adm3'] 
    selected_adm3 = Adm3.objects.get(id=adm3_id)

    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    watershed = Watershed(name=name, area=area,trace=traced,adm3=selected_adm3)
    watershed.save()
    flash("Watershed added succesfully")
    return redirect('/watershed')

@watershed_bp.route('/editwatershed/<string:watershed_id>', methods=['GET', 'POST'])
@login_required
def edit_watershed(watershed_id):
    watershed = Watershed.objects(id=watershed_id).first()
    adm3=Adm3.objects()
    
    
    if request.method == 'POST':
        nombre = request.form['name']
        area = request.form['area']
        trace = watershed.trace
        adm3_id = request.form['adm3'] 
        selected_adm3 = Adm3.objects.get(id=adm3_id)
        trace['updated'] = datetime.now()
        watershed.update(name=nombre, area=area, trace=trace,adm3=selected_adm3)

        flash("Watershed updated successfully")
        return redirect('/watershed')

    return render_template('edit_watershed.html', watershed=watershed,adm3=adm3)

@watershed_bp.route('/deletewatershed/<string:watershed_id>')
@login_required
def delete_watershed(watershed_id):
    watershed = Watershed.objects(id=watershed_id).first()

    if watershed:
        trace = watershed.trace

        trace['enabled'] = False
        watershed.update(trace=trace)
        flash("Watershed deleted successfully")
    else:
        flash("Watershed not found")

    return redirect('/watershed')


@watershed_bp.route('/resetwatershed/<string:watershed_id>')
@login_required
def reset_watershed(watershed_id):
    watershed = Watershed.objects(id=watershed_id).first()

    if watershed:
        trace = watershed.trace

        trace['enabled'] = True
        watershed.update(trace=trace)
        flash("Watershed recover successfully")
    else:
        flash("Watershed not found")

    return redirect('/watershed')
@watershed_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401
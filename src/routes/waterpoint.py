from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Adm1
from ormWP import Adm2
from ormWP import Adm3
from ormWP import Watershed
from ormWP import Waterpoint
from datetime import datetime
waterpoint_bp = Blueprint('waterpoint', __name__)

@waterpoint_bp.route('/waterpoint')
def show_watershed():
    waterpoint = Waterpoint.objects()
    watershed=Watershed.objects()
    return render_template('waterpoint.html', waterpoint=waterpoint, watershed=watershed)

@waterpoint_bp.route('/waterpoint/add', methods=['POST'])
def add_wateshed():
    name = request.form['name']
    lat = request.form['lat']
    lon = request.form['lon']
    area = request.form['area']
    watershed = request.form['watershed'] 
    ext_id = request.form['ext_id'] 
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    waterpoint = Waterpoint(name=name, area=area,lat=lat,lon=lon,ext_id=ext_id,trace=traced,watershed=watershed,other_attributes=[''],aclimate_id='',climatology=[''])
    waterpoint.save()
    flash("Waterpoint added succesfully")
    return redirect('/waterpoint')

@waterpoint_bp.route('/editwaterpoint/<string:waterpoint_id>', methods=['GET', 'POST'])
def edit_waterpoint(waterpoint_id):
    waterpoint = Waterpoint.objects(id=waterpoint_id).first()
    watershed=Watershed.objects()
    
    
    if request.method == 'POST':
        name = request.form['name']
        lat = request.form['lat']
        lon = request.form['lon']
        area = request.form['area']
        watershed_id = request.form['watershed'] 
        ext_id = request.form['ext_id'] 
        trace = waterpoint.trace
        selected_watershed = Watershed.objects.get(id=watershed_id)
        trace['updated'] = datetime.now()
        waterpoint.update(name=name, area=area,lat=lat,lon=lon,ext_id=ext_id, trace=trace,watershed=selected_watershed)

        flash("Waterpoint updated successfully")
        return redirect('/waterpoint')

    return render_template('edit_waterpoint.html', waterpoint=waterpoint,watershed=watershed)

@waterpoint_bp.route('/deletewaterpoint/<string:waterpoint_id>')
def delete_watershed(waterpoint_id):
    waterpoint = Waterpoint.objects(id=waterpoint_id).first()

    if waterpoint:
        waterpoint.delete()
        flash("Waterpoint deleted successfully")
    else:
        flash("Waterpoint not found")

    return redirect('/waterpoint')
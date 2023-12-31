from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Typecontent
from datetime import datetime
from flask_login import login_required  

typecontent_bp = Blueprint('typecontent', __name__)

@typecontent_bp.route('/typecontent')
@login_required
def show_typecontent():
    typecontent = Typecontent.objects()
    return render_template('typecontent.html', typecontent=typecontent)

@typecontent_bp.route('/addtypecontent')
@login_required
def addd_typecontent():
    typecontent = Typecontent.objects(trace__enabled=True)

    return render_template('addTypecontent.html', typecontent=typecontent)

@typecontent_bp.route('/typecontent/add', methods=['POST'])
@login_required
def add_typecontent():
    name = request.form['name']
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}

    typecontent = Typecontent(name=name,trace=traced)
    typecontent.save()
    flash("typecontent added succesfully")
    return redirect('/typecontent')

@typecontent_bp.route('/editypecontent/<string:typecontent_id>', methods=['GET', 'POST'])
@login_required
def edit_typecontent(typecontent_id):
    typecontent = Typecontent.objects(id=typecontent_id).first()
    
    if request.method == 'POST':
        name = request.form['name']
        trace = typecontent.trace

        trace['updated'] = datetime.now()
        typecontent.update(name=name,trace=trace)


        flash("typecontent updated successfully")
        return redirect('/typecontent')

    return render_template('edit_typecontent.html', typecontent=typecontent)

@typecontent_bp.route('/deletetypecontent/<string:typecontent_id>')
@login_required
def delete_typecontent(typecontent_id):
    typecontent = Typecontent.objects(id=typecontent_id).first()

    if typecontent:
        trace = typecontent.trace

        trace['enabled'] = False
        typecontent.update(trace=trace)
        flash("Typecontent deleted successfully")
    else:
        flash("typecontent not found")

    return redirect('/typecontent')

@typecontent_bp.route('/resetypecontent/<string:typecontent_id>')
@login_required
def reset_typecontent(typecontent_id):
    typecontent = Typecontent.objects(id=typecontent_id).first()

    if typecontent:
        trace = typecontent.trace

        trace['enabled'] = True
        typecontent.update(trace=trace)
        flash("Category recover successfully")
    else:
        flash("Category not found")

    return redirect('/typecontent')
@typecontent_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401
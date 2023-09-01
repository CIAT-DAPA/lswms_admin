from flask import Blueprint, render_template, redirect, request,flash
from ormWP import Typecontent
typecontent_bp = Blueprint('typecontent', __name__)

@typecontent_bp.route('/typecontent')
def show_typecontent():
    typecontent = Typecontent.objects()
    return render_template('typecontent.html', typecontent=typecontent)

@typecontent_bp.route('/typecontent/add', methods=['POST'])
def add_typecontent():
    name = request.form['name']
    typecontent = Typecontent(name=name)
    typecontent.save()
    flash("typecontent added succesfully")
    return redirect('/typecontent')

@typecontent_bp.route('/editypecontent/<string:typecontent_id>', methods=['GET', 'POST'])
def edit_typecontent(typecontent_id):
    typecontent = Typecontent.objects(id=typecontent_id).first()
    
    if request.method == 'POST':
        name = request.form['name']
        typecontent.update(name=name)

        flash("typecontent updated successfully")
        return redirect('/typecontent')

    return render_template('edit_typecontent.html', typecontent=typecontent)

@typecontent_bp.route('/deletetypecontnt/<string:typecontent_id>')
def delete_typecontent(typecontent_id):
    typecontent = Typecontent.objects(id=typecontent_id).first()

    if typecontent:
        typecontent.delete()
        flash("typecontent deleted successfully")
    else:
        flash("typecontent not found")

    return redirect('/typecontent')



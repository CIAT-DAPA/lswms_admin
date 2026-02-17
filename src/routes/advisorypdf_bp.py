from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required
from ormWP import AdvisoryPdf, AdvisoryTypeEnum
from werkzeug.utils import secure_filename
import os
import shutil

advisorypdf_bp = Blueprint('advisorypdf', __name__)

PDFS_PATH = os.getenv('PDFS_PATH', '/Users/cnasayo/Documents/CIAT/waterpoints2025/data/data')

TYPES = [t.value for t in AdvisoryTypeEnum]


@advisorypdf_bp.route('/advisorypdf')
@login_required
def list_advisorypdf():
    items = AdvisoryPdf.objects().order_by('name')
    return render_template('advisorypdf.html', items=items)


@advisorypdf_bp.route('/advisorypdf/add', methods=['GET', 'POST'])
@login_required
def add_advisorypdf():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        pdf_type = request.form.get('type', '').strip()
        pdf_file = request.files.get('pdf_file')

        if not name:
            flash('Name is required', 'danger')
            return redirect('/advisorypdf/add')

        if pdf_type not in TYPES:
            flash('Invalid type', 'danger')
            return redirect('/advisorypdf/add')

        if not pdf_file or not pdf_file.filename:
            flash('PDF file is required', 'danger')
            return redirect('/advisorypdf/add')

        filename = secure_filename(pdf_file.filename)

        # Save file to disk
        os.makedirs(PDFS_PATH, exist_ok=True)
        file_path = os.path.join(PDFS_PATH, filename)
        pdf_file.save(file_path)

        # Save to DB
        doc = AdvisoryPdf(
            name=name,
            description=description,
            type=AdvisoryTypeEnum(pdf_type),
            filename=filename
        )
        doc.save()
        flash('Advisory PDF created successfully', 'success')
        return redirect('/advisorypdf')

    return render_template('advisorypdf_add.html', types=TYPES)


@advisorypdf_bp.route('/advisorypdf/edit/<string:item_id>', methods=['GET', 'POST'])
@login_required
def edit_advisorypdf(item_id):
    doc = AdvisoryPdf.objects(id=item_id).first()
    if not doc:
        flash('Advisory PDF not found', 'danger')
        return redirect('/advisorypdf')

    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        new_description = request.form.get('description', '').strip()
        new_type = request.form.get('type', '').strip()
        pdf_file = request.files.get('pdf_file')

        if not new_name:
            flash('Name is required', 'danger')
            return redirect(f'/advisorypdf/edit/{item_id}')

        if new_type not in TYPES:
            flash('Invalid type', 'danger')
            return redirect(f'/advisorypdf/edit/{item_id}')

        # If a new PDF file was uploaded, replace the old one
        if pdf_file and pdf_file.filename:
            new_filename = secure_filename(pdf_file.filename)

            # Remove old file if it exists
            old_path = os.path.join(PDFS_PATH, doc.filename)
            if os.path.exists(old_path):
                os.remove(old_path)

            # Save new file
            os.makedirs(PDFS_PATH, exist_ok=True)
            new_path = os.path.join(PDFS_PATH, new_filename)
            pdf_file.save(new_path)
            doc.filename = new_filename

        doc.name = new_name
        doc.description = new_description
        doc.type = AdvisoryTypeEnum(new_type)
        doc.save()
        flash('Advisory PDF updated successfully', 'success')
        return redirect('/advisorypdf')

    return render_template('advisorypdf_edit.html', doc=doc, types=TYPES)


@advisorypdf_bp.route('/advisorypdf/delete/<string:item_id>')
@login_required
def delete_advisorypdf(item_id):
    doc = AdvisoryPdf.objects(id=item_id).first()
    if not doc:
        flash('Advisory PDF not found', 'danger')
        return redirect('/advisorypdf')

    # Remove file from disk
    file_path = os.path.join(PDFS_PATH, doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    doc.delete()
    flash('Advisory PDF deleted', 'success')
    return redirect('/advisorypdf')


@advisorypdf_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401

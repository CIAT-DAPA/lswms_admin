from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app, send_from_directory
from flask_login import login_required
import os


ALLOWED_EXTENSIONS = {'html'}
ALLOWED_NAMES = {'weekly'}
weekly_bp = Blueprint('weekly', __name__)

def allowed_file(filename):
    name, extension = os.path.splitext(filename)
    return extension.lower() == '.html' and name.lower() in ALLOWED_NAMES

@weekly_bp.route('/addweekly')
@login_required
def add_weekly():
    return render_template('addWeekly.html')

@weekly_bp.route('/weekly/add', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file provided')
        return redirect('/adm1')

    file = request.files['file']

    if file and allowed_file(file.filename):
        upload_folder_path = os.path.join('/var/www/waterpoinsAdmin', 'alerts')
        os.makedirs(upload_folder_path, exist_ok=True)

        file_path = os.path.join(upload_folder_path, file.filename)
        file.save(file_path)

        flash('File uploaded successfully!')
        return redirect('/adm1')

    else:
        flash('Invalid file format or name')
        return redirect('/adm1')
    
@weekly_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401

@weekly_bp.route('/download_weekly')
@login_required
def download_file():
    directory = '/var/www/waterpoinsAdmin/alerts'
    filename = 'weekly.html'
    return send_from_directory(directory, filename, as_attachment=True)
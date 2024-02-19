from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app, send_from_directory
from flask_login import login_required
import os

ALLOWED_EXTENSIONS = {'html'}
ALLOWED_NAMES = {'alert', 'weekly'}
alerts_bp = Blueprint('alerts', __name__)

def allowed_file(filename, alert_checked, weekly_checked):
    name, extension = os.path.splitext(filename)
    name_lower = name.lower()
    
    if not (alert_checked or weekly_checked):
        return False

    if alert_checked and 'alert' not in name_lower:
        return False

    if weekly_checked and 'weekly' not in name_lower:
        return False

    return extension.lower() == '.html' and name_lower in ALLOWED_NAMES

@alerts_bp.route('/addalert')
@login_required 
def add_alert():
    directory = '/var/www/waterpoinsAdmin/alerts'
    files = [file for file in os.listdir(directory) if file.endswith('.html') and ('alert' in file or 'weekly' in file)]
    return render_template('addAlert.html', files=files)

@alerts_bp.route('/alert/add', methods=['POST'])
@login_required 
def upload_file():
    if 'file' not in request.files:
        flash('No file provided', 'error')
        return redirect('/addalert')

    file = request.files['file']
    type_selected = request.form.get('type', None)

    if type_selected not in {'alert', 'weekly'}:
        flash('Please select at least one option (Alert or Weekly)', 'error')
        return redirect('/addalert')

    if not file:  
        flash('Please select a file to upload', 'error')
        return redirect('/addalert')

    if (type_selected == 'alert' and 'alert' not in file.filename.lower()) or \
       (type_selected == 'weekly' and 'weekly' not in file.filename.lower()):
        flash('Selected type does not match the file name', 'error')
        return redirect('/addalert')

    if file and allowed_file(file.filename, type_selected == 'alert', type_selected == 'weekly'):
        upload_folder_path = os.path.join('/var/www/waterpoinsAdmin', 'alerts')
        os.makedirs(upload_folder_path, exist_ok=True)

        file_path = os.path.join(upload_folder_path, file.filename)
        file.save(file_path)

        flash('File uploaded successfully!', 'success')
        return redirect('/addalert')

    else:
        flash('Invalid file format or name', 'error')
        return redirect('/addalert')



        
    
@alerts_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401

@alerts_bp.route('/download/<filename>')
def download_specific_file(filename):
    directory = '/var/www/waterpoinsAdmin/alerts'
    return send_from_directory(directory, filename, as_attachment=True)

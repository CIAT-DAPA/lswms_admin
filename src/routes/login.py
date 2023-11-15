from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, logout_user, current_user,login_manager
from models.models import User  
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get(username)  

        if user and user.check_password(password):
            login_user(user)
            flash('Success', 'success')
            print(current_user.username)
            return redirect('/adm1')
        else:
            flash('Incorrect credentials', 'error')


   
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect('/login') 


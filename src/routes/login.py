from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, current_user,login_required, logout_user
from models.models import User  

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect('/adm1')  
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_user_by_username(username)

        if user:
            print(user.user_obj["id"])
            realm_id=User.get_realm_id()
            id_role = User.get_role_id_by_name(realm_id)

            roles=User.get_user_role_mapping_by_role_id(id_role)

            credentials = User.get_credentials(user.user_obj['id'])
            print(credentials)
            if User.verify_password(password, credentials):
                print("password correcto")
            else:
                print("password incorrecto")
            if User.check_user_has_role(user.user_obj['id'],roles) and User.verify_password(password, credentials):
                print("tiene el rol")
                login_user(user)
                flash('Success', 'success')
                return redirect('/adm1')
            else:
                print("no tiene el rol")
                flash('sorry you are not admin', 'error')
        else:
            flash('Incorrect credentials', 'error')

    return render_template('login.html')


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect('/')
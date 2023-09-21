from flask import Blueprint, render_template, redirect, request,flash

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def show_adm1():
    
    return render_template('home.html')
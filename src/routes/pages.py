from flask import Blueprint, render_template, session, redirect, url_for
from src.utils.validacoes import verifica_gestor

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@pages_bp.route('/painel-morador')
def painel_morador():
    if 'user_id' not in session:
        return redirect('/unauthorized')
    return render_template('painelMorador.html')

@pages_bp.route('/painel-gestor')
def painel_gestor():
    if 'user_id' not in session:
        return redirect('/unauthorized')
    return render_template('painelGestor.html')

@pages_bp.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')


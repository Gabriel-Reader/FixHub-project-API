from flask import Blueprint, render_template
from src.utils.auth_decorators import token_required

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@pages_bp.route("/painel-morador")
def painel_morador():
    # As informações do usuário autenticado estarão em request.user
    return render_template("painelMorador.html")

@pages_bp.route("/painel-gestor")
def painel_gestor():
    # As informações do usuário autenticado estarão em request.user
    return render_template("painelGestor.html")

@pages_bp.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")

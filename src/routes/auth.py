from flask import Blueprint, request, jsonify, session
from src.services.manipular_database import verificar_login, criar_usuario
from src.utils.validacoes import validar_email, validar_password, validar_username, verifica_gestor

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario_form = data.get('usuario')
    senha_form = data.get('senha')
    
    dados_usuario_db = verificar_login(usuario_form, senha_form)
    
    if dados_usuario_db:
        id_morador_db, nome_db, senha_db, ceu_casa_db = dados_usuario_db
        
        session.clear()
        session['user_id'] = id_morador_db
        session['username'] = nome_db
        session['ceu'] = ceu_casa_db
        
        is_gestor = verifica_gestor(nome_db)
        
        return jsonify({
            'success': True,
            'user': {
                'id': id_morador_db,
                'username': nome_db,
                'ceu_casa': ceu_casa_db,
                'is_gestor': is_gestor
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Usuário ou senha incorretos.'
        }), 401

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    c_usuario = data.get('usuario')
    c_email = data.get('email')
    c_senha = data.get('senha')
    c_quarto = data.get('quarto')
    c_casa = data.get('casa')
    
    user = (c_usuario, c_senha, c_email, c_quarto, c_casa)
    
    errors = []
    
    if not validar_username(c_usuario):
        errors.append('O usuário deve ter apenas letras e números (3-20 caracteres).')
    
    if not validar_password(c_senha):
        errors.append('A senha deve ter pelo menos 6 caracteres, incluindo letras e números.')
    
    if not validar_email(c_email):
        errors.append('Insira um E-mail válido.')
    
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    else:
        criar_usuario(user)
        return jsonify({
            'success': True,
            'message': 'Usuário cadastrado com sucesso!'
        })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'ceu_casa': session.get('ceu'),
                'is_gestor': verifica_gestor(session.get('username'))
            }
        })
    else:
        return jsonify({'authenticated': False})


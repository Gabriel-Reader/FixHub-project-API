from flask import Blueprint, request, jsonify
from src.services.manipular_database import verificar_login, criar_usuario
from src.utils.validacoes import validar_email, validar_password, validar_username, verifica_gestor
import jwt
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

# Chave secreta para assinar e verificar os tokens JWT
SECRET_KEY = 'd2ccd1731dc1cc9e3352a9db9698cc4ba'

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario_form = data.get("usuario")
    senha_form = data.get("senha")
    
    dados_usuario_db = verificar_login(usuario_form, senha_form)
    
    if dados_usuario_db:
        id_morador_db, nome_db, senha_db, ceu_casa_db = dados_usuario_db
        
        is_gestor = verifica_gestor(nome_db)
        
        # Gerar token JWT
        token_payload = {
            'user_id': id_morador_db,
            'username': nome_db,
            'ceu_casa': ceu_casa_db,
            'is_gestor': is_gestor,
            'exp': datetime.utcnow() + timedelta(hours=24) # Token expira em 24 horas
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
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

@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    c_usuario = data.get("usuario")
    c_email = data.get("email")
    c_senha = data.get("senha")
    c_quarto = data.get("quarto")
    c_casa = data.get("casa")
    
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

@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Com JWT, o logout é geralmente tratado no lado do cliente (descartando o token).
    # Se uma lista negra de tokens for implementada, a lógica seria adicionada aqui.
    return jsonify({'success': True, 'message': 'Sessão encerrada no cliente.'})

@auth_bp.route("/check-session", methods=["GET"])
def check_session():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'authenticated': False}), 401

    try:
        token = token.split(" ")[1] # Remover "Bearer "
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # O token é válido, retornar as informações do usuário
        return jsonify({
            'authenticated': True,
            'user': {
                'id': payload.get('user_id'),
                'username': payload.get('username'),
                'ceu_casa': payload.get('ceu_casa'),
                'is_gestor': payload.get('is_gestor')
            }
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'authenticated': False, 'message': 'Token expirado.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'authenticated': False, 'message': 'Token inválido.'}), 401



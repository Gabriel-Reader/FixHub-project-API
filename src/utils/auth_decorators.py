from flask import request, jsonify
import jwt
from functools import wraps

# A chave secreta deve ser a mesma usada para assinar o token no auth.py
SECRET_KEY = 'd2ccd1731dc1cc9e3352a9db9698cc4ba'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWTs são geralmente enviados no cabeçalho Authorization como Bearer Token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token é necessário!'}), 401

        try:
            # Decodifica o token usando a chave secreta e o algoritmo
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # Anexa os dados do usuário decodificados ao objeto request
            # para que as rotas protegidas possam acessá-los
            request.user = data 
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido.'}), 401

        return f(*args, **kwargs)
    return decorated



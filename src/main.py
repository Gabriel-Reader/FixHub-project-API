import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template
from flask_cors import CORS

from src.routes.pedidos import pedidos_bp
from src.routes.pages import pages_bp
from src.routes.auth import auth_bp

app = Flask(__name__, 
           static_folder=os.path.join(os.path.dirname(__file__), 'static'),
           template_folder=os.path.join(os.path.dirname(__file__), 'static', 'templates'))
app.config['SECRET_KEY'] = 'd2ccd1731dc1cca262d6c889e3352a921f973db9698cc4ba'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos')
app.register_blueprint(pages_bp)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

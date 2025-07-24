from flask import Blueprint, request, jsonify, session
from src.services.manipular_database import (
    criar_pedido, mostrar_pedidos_morador, mostrar_pedidos_gestor,
    alterar_status_pedido, comentario_gestor, deletar_pedido, obter_filtros_disponiveis
)
from src.utils.utilitarios import converter_pedidos_para_dicionario


pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/criar', methods=['POST'])
def criar_pedido_api():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    data = request.get_json()
    id_morador = session.get('user_id')
    casa = data.get('casa')
    local_manuntencao = data.get('local_manuntencao')
    categoria = data.get('categoria')
    quarto = data.get('quarto')
    ala = data.get('ala')
    descricao = data.get('descricao')
    comentario_gestor = ""
    status = "Pendente"
    
    pedido = (id_morador, casa, local_manuntencao, categoria, quarto, ala, descricao, comentario_gestor, status)
    
    criar_pedido(pedido)
    
    return jsonify({
        'success': True
    })

@pedidos_bp.route('/morador', methods=['GET'])
def listar_pedidos_morador():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    id_morador = session.get('user_id')
    pedidos_tuplas = mostrar_pedidos_morador(id_morador)
    pedidos = converter_pedidos_para_dicionario(pedidos_tuplas)
    
    return jsonify({
        'success': True,
        'pedidos': pedidos,
        'user': {
            'username': session.get('username'),
            'ceu_casa': session.get('ceu')
        }
    })

@pedidos_bp.route('/gestor', methods=['GET'])
def listar_pedidos_gestor():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    # Obter parâmetros de filtro da URL
    filtro_casa = request.args.get('casa', '')
    filtro_categoria = request.args.get('categoria', '')
    filtro_status = request.args.get('status', '')
    ordenar_por = request.args.get('ordenar_por', 'recentes')
    
    # Chamar mostrar_pedidos_gestor com os filtros
    pedidos_tuplas = mostrar_pedidos_gestor(
        filtro_casa=filtro_casa if filtro_casa else None,
        filtro_categoria=filtro_categoria if filtro_categoria else None,
        filtro_status=filtro_status if filtro_status else None,
        ordenar_por=ordenar_por
    )
    pedidos = converter_pedidos_para_dicionario(pedidos_tuplas)
    
    # Obter casas e categorias disponíveis para preencher os selects de filtro
    casas_disponiveis, categorias_disponiveis = obter_filtros_disponiveis()
    
    return jsonify({
        'success': True,
        'pedidos': pedidos,
        'filtros': {
            'casas_disponiveis': casas_disponiveis,
            'categorias_disponiveis': categorias_disponiveis,
            'filtro_casa': filtro_casa,
            'filtro_categoria': filtro_categoria,
            'filtro_status': filtro_status,
            'ordenar_por': ordenar_por
        },
        'user': {
            'username': session.get('username')
        }
    })

@pedidos_bp.route('/atualizar', methods=['POST'])
def atualizar_pedido_api():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    data = request.get_json()
    pedido_id = data.get('pedido_id')
    novo_status = data.get('status')
    novo_comentario = data.get('comentario')
    
    alterar_status_pedido(pedido_id, novo_status)
    if novo_comentario:
        comentario_gestor(pedido_id, novo_comentario)
    
    return jsonify({
        'success': True
    })

@pedidos_bp.route('/deletar/<int:id_pedido>', methods=['DELETE'])
def deletar_pedido_api(id_pedido):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    id_morador = session.get('user_id')
    deletar_pedido(id_pedido, id_morador)
    
    return jsonify({
        'success': True
    })


from flask import Blueprint, request, jsonify
from src.services.manipular_database import (
    criar_pedido, mostrar_pedidos_morador, mostrar_pedidos_gestor,
    alterar_status_pedido, comentario_gestor, deletar_pedido, obter_filtros_disponiveis
)
from src.utils.utilitarios import converter_pedidos_para_dicionario
from src.utils.auth_decorators import token_required


pedidos_bp = Blueprint("pedidos", __name__)

@pedidos_bp.route("/criar", methods=["POST"])
@token_required
def criar_pedido_api():
    # As informações do usuário estão em request.user
    user_id = request.user.get("user_id")
    username = request.user.get("username")
    
    data = request.get_json()
    casa = data.get("casa")
    local_manuntencao = data.get("local_manuntencao")
    categoria = data.get("categoria")
    quarto = data.get("quarto")
    ala = data.get("ala")
    descricao = data.get("descricao")
    comentario_gestor = ""
    status = "Pendente"
    
    pedido = (user_id, casa, local_manuntencao, categoria, quarto, ala, descricao, comentario_gestor, status)
    
    criar_pedido(pedido)
    
    return jsonify({
        "success": True,
        "message": f"Pedido criado por {username} (ID: {user_id})"
    })


@pedidos_bp.route("/morador", methods=["GET"])
@token_required # Aplicar o decorador
def listar_pedidos_morador():
    
    id_morador = request.user.get("user_id") # Usar request.user
    pedidos_tuplas = mostrar_pedidos_morador(id_morador)
    pedidos = converter_pedidos_para_dicionario(pedidos_tuplas)
    
    return jsonify({
        "success": True,
        "pedidos": pedidos,
        "user": {
            "username": request.user.get("username"), # Usar request.user
            "ceu_casa": request.user.get("ceu_casa") # Usar request.user
        }
    })


@pedidos_bp.route("/gestor", methods=["GET"])
@token_required # Aplicar o decorador
def listar_pedidos_gestor():

    # Obter parâmetros de filtro da URL
    filtro_casa = request.args.get("casa", "")
    filtro_categoria = request.args.get("categoria", "")
    filtro_status = request.args.get("status", "")
    ordenar_por = request.args.get("ordenar_por", "recentes")
    
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
        "success": True,
        "pedidos": pedidos,
        "filtros": {
            "casas_disponiveis": casas_disponiveis,
            "categorias_disponiveis": categorias_disponiveis,
            "filtro_casa": filtro_casa,
            "filtro_categoria": filtro_categoria,
            "filtro_status": filtro_status,
            "ordenar_por": ordenar_por
        },
        "user": {
            "username": request.user.get("username")
        }
    })

@pedidos_bp.route("/atualizar", methods=["POST"])
@token_required
def atualizar_pedido_api():
    
    data = request.get_json()
    pedido_id = data.get("pedido_id")
    novo_status = data.get("status")
    novo_comentario = data.get("comentario")
    
    alterar_status_pedido(pedido_id, novo_status)
    if novo_comentario:
        comentario_gestor(pedido_id, novo_comentario)
    
    return jsonify({
        "success": True
    })

@pedidos_bp.route("/deletar/<int:id_pedido>", methods=["DELETE"])
@token_required
def deletar_pedido_api(id_pedido):
    
    id_morador = request.user.get("user_id") # Usar request.user
    deletar_pedido(id_pedido, id_morador)
    
    return jsonify({
        "success": True
    })



from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Tema, Item
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Tema & Itens API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Documentação Swagger")
tema_tag = Tag(name="Tema", description="Adição, visualização, atualização e remoção de temas à base")
item_tag = Tag(name="Item", description="Adição, visualização, atualização e remoção de um item a um tema cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, tela que permite ver a documentação em Swagger.
    """
    return redirect('/openapi/swagger')


@app.post('/tema', tags=[tema_tag],
          responses={"200": TemaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tema(form: TemaSchema):
    """Adiciona um novo Tema à base de dados

    Retorna uma representação do tema e itens associados.
    """
    nome = form.nome
    tema = Tema(nome)
    logger.debug(f"Adicionando tema de nome: '{tema.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando tema
        session.add(tema)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado tema de nome: '{tema.nome}'")
        return apresenta_tema(tema), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Tema de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar tema '{tema.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tema '{tema.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.put('/tema', tags=[tema_tag],
          responses={"200": TemaViewSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def update_tema(form: TemaUpdSchema):
    """Atualiza o nome de um Tema à base de dados

    Retorna uma representação do tema e itens associados.
    """
    nome_velho = form.nome_velho
    nome_novo = form.nome_novo

    logger.debug(f"Atualizando tema de nome: de '{nome_velho}' para '{nome_novo}'")
    try:
        # criando conexão com a base
        session = Session()
        # buscando tema
        tema = session.query(Tema).filter(Tema.nome == nome_velho).first()
        tema_renomeado = session.query(Tema).filter(Tema.nome == nome_novo).first()

        if not tema:
            # se o tema não foi encontrado
            error_msg = "Tema não encontrado na base :/"
            logger.warning(f"Erro ao buscar tema '{nome_velho}', {error_msg}")
            return {"message": error_msg}, 404
        elif tema_renomeado:
            # erro de duplicidade do nome
            error_msg = "Tema de mesmo nome já salvo na base :/"
            logger.warning(f"Erro ao atualizar tema '{tema.nome}', {error_msg}")
            return {"message": error_msg}, 409
        else:
            # atualiza o nome do tema
            tema.atualiza_nome_tema(nome_novo)
            
            # efetivando o camando de atualização do tema na tabela
            session.commit()
            logger.debug(f"Atualizado tema de nome: de '{nome_velho}' para '{nome_novo}'")
            return apresenta_tema(tema), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tema '{tema.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/temas', tags=[tema_tag],
         responses={"200": ListagemTemasSchema, "404": ErrorSchema})
def get_temas():
    """Faz a busca por todos os Temas cadastrados

    Retorna uma representação da listagem de temas.
    """
    logger.debug(f"Coletando temas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    temas = session.query(Tema).all()

    if not temas:
        # se não há temas cadastrados
        return {"temas": []}, 200
    else:
        logger.debug(f"%d temas econtrados" % len(temas))
        # retorna a representação de tema
        return apresenta_temas(temas), 200


@app.get('/tema', tags=[tema_tag],
         responses={"200": TemaViewSchema, "404": ErrorSchema})
def get_tema(query: TemaBuscaSchema):
    """Faz a busca por um Tema a partir do nome do tema

    Retorna uma representação do tema e itens associados.
    """
    nome_tema = unquote(unquote(query.nome))
    logger.debug(f"Coletando dados sobre tema #{nome_tema}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

    if not tema:
        # se o tema não foi encontrado
        error_msg = "Tema não encontrado na base :/"
        logger.warning(f"Erro ao buscar tema '{nome_tema}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Tema econtrado: '{tema.nome}'")
        # retorna a representação de tema
        return apresenta_tema(tema), 200


@app.delete('/tema', tags=[tema_tag],
            responses={"200": TemaDelSchema, "404": ErrorSchema})
def del_tema(form: TemaBuscaSchema):
    """Deleta um Tema a partir do nome de tema informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome_tema = form.nome
    logger.debug(f"Deletando dados sobre tema #{nome_tema}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Tema).filter(Tema.nome == nome_tema).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado tema #{nome_tema}")
        return {"message": "Tema removido", "nome": nome_tema}, 200
    else:
        # se o tema não foi encontrado
        error_msg = "Tema não encontrado na base :/"
        logger.warning(f"Erro ao deletar tema #'{nome_tema}', {error_msg}")
        return {"message": error_msg}, 404
    

@app.delete('/temas', tags=[tema_tag],
            responses={"200": TemasDelSchema, "404": ErrorSchema})
def del_temas():
    """Deleta todos os Temas cadastrados

    Retorna uma mensagem de confirmação da remoção.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Tema).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado todos os temas")
        return {"message": "Temas removidos", "quantidade": count}, 200
    else:
        # se o tema não foi encontrado
        error_msg = "Não há temas para deletar :/"
        logger.warning(f"Erro ao deletar temas', {error_msg}")
        return {"message": error_msg}, 404




@app.post('/item', tags=[item_tag],
          responses={"200": TemaViewSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def add_item(form: ItemSchema):
    """Adiciona um novo Item à base de dados

    Retorna uma representação do tema com seus itens.
    """
    nome_tema = form.nome_tema
    nome_item = form.nome_item
    
    logger.debug(f"Adicionando tema de nome: '{nome_item}'")
    try:
        # criando conexão com a base
        session = Session()
        # buscando tema
        tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

        if not tema:
            # se o tema não foi encontrado
            error_msg = "Tema não encontrado na base :/"
            logger.warning(f"Erro ao adicionar item no tema #'{nome_tema}', {error_msg}")
            return {"message": error_msg}, 404
        
        item = Item(nome_item)
        count = tema.adiciona_item(item)
        if not count:
            # duplicidade de nome de item no tema
            error_msg = "Item de mesmo nome já salvo na base :/"
            logger.warning(f"Erro ao adicionar item '{nome_item}', {error_msg}")
            return {"message": error_msg}, 409
        
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado item '{nome_item}' no tema '{nome_tema}'")
        return apresenta_tema(tema), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar item '{nome_item}', {error_msg}")
        return {"message": error_msg}, 400


@app.put('/item', tags=[item_tag],
          responses={"200": TemaViewSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def update_item(form: ItemUpdSchema):
    """Atualiza o nome de um item à base de dados

    Retorna uma representação do tema e itens associados.
    """
    nome_item_velho = form.nome_item_velho
    nome_item_novo = form.nome_item_novo
    nome_tema = form.nome_tema

    logger.debug(f"Atualizado item de nome: de '{nome_item_velho}' para '{nome_item_novo}' no tema '{nome_tema}'")
    try:
        # criando conexão com a base
        session = Session()
        # buscando tema
        tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

        if not tema:
            # se o tema não foi encontrado
            error_msg = "Tema não encontrado na base :/"
            logger.warning(f"Erro ao buscar tema '{nome_tema}', {error_msg}")
            return {"message": error_msg}, 404
        
        # buscando item
        item = session.query(Item).filter(Item.nome == nome_item_velho, Item.tema == tema.id).first()
        
        if not item:
            # se o item não foi encontrado
            error_msg = "Item não encontrado na base :/"
            logger.warning(f"Erro ao buscar item '{nome_item_velho}', {error_msg}")
            return {"message": error_msg}, 404
        
        # atualiza o nome do tema
        count = tema.atualiza_nome_item(nome_item_velho, nome_item_novo)
        session.commit()

        if count:
            logger.debug(f"Atualizado item de nome: de '{nome_item_velho}' para '{nome_item_novo}' no tema '{nome_tema}'")
            return apresenta_tema(tema), 200
        else:
            # erro de duplicidade do nome
            error_msg = "Item de mesmo nome já salvo na base :/"
            logger.warning(f"Erro ao atualizar item '{nome_item_velho}', {error_msg}")
            return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tema '{tema.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/itens', tags=[item_tag],
         responses={"200": TemaViewSchema, "404": ErrorSchema})
def get_itens(query: ItensBuscaSchema):
    """Faz a busca por todos os Itens cadastrados em um tema

    Retorna uma representação do tema e itens associados.
    """
    logger.debug(f"Coletando itens ")

    nome_tema = unquote(unquote(query.nome_tema))

    # criando conexão com a base
    session = Session()
    # fazendo a busca do tema
    tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

    if not tema:
         # se o tema não foi encontrado
        error_msg = "Tema não encontrado na base :/"
        logger.warning(f"Erro ao buscar tema '{nome_tema}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"%d itens econtrados" % len(tema.itens))
        # retorna a representação de tema
        return apresenta_tema(tema), 200


@app.get('/item', tags=[item_tag],
         responses={"200": ItemViewSchema, "404": ErrorSchema})
def get_item(query: ItemBuscaSchema):
    """Faz a busca por um Item a partir do nome do tema + item

    Retorna uma representação do item.
    """
    nome_tema = unquote(unquote(query.nome_tema))
    nome_item = unquote(unquote(query.nome_item))

    logger.debug(f"Coletando dados sobre item #{nome_item} no tema #{nome_tema}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

    if not tema:
        # se o tema não foi encontrado
        error_msg = "Tema não encontrado na base :/"
        logger.warning(f"Erro ao buscar tema '{nome_tema}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        item = session.query(Item).filter(Item.nome == nome_item, Item.tema == tema.id).first()

        if not item:
            # se o tema não foi encontrado
            error_msg = "Item não encontrado na base :/"
            logger.warning(f"Erro ao buscar item '{nome_item}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Item econtrado: '{nome_item}'")
            # retorna a representação de item
            return apresenta_item(item, tema), 200


@app.delete('/item', tags=[item_tag],
            responses={"200": ItemDelSchema, "404": ErrorSchema})
def del_item(form: ItemBuscaSchema):
    """Deleta um Item a partir do nome de tema + item informados

    Retorna uma mensagem de confirmação da remoção.
    """
    nome_tema = form.nome_tema
    nome_item = form.nome_item
    logger.debug(f"Deletando dados sobre item #{nome_item} no tema #{nome_tema}")
    # criando conexão com a base
    session = Session()

    tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

    if not tema:
        # se o tema não foi encontrado
        error_msg = "Tema não encontrado na base :/"
        logger.warning(f"Erro ao buscar tema '{nome_tema}', {error_msg}")
        return {"message": error_msg}, 404
    
    count = session.query(Item).filter(Item.nome == nome_item, Item.tema == tema.id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado item #{nome_item}")
        return {"message": "Item removido", "nome": nome_item}, 200
    else:
        # se o tema não foi encontrado
        error_msg = "Item não encontrado na base :/"
        logger.warning(f"Erro ao deletar item #'{nome_item}', {error_msg}")
        return {"message": error_msg}, 404
    

@app.delete('/itens', tags=[item_tag],
            responses={"200": ItensDelSchema, "404": ErrorSchema})
def del_itens(form: ItensBuscaSchema):
    """Deleta todos os Itens cadastrados em um tema

    Retorna uma mensagem de confirmação da remoção.
    """
    nome_tema = form.nome_tema

    # criando conexão com a base
    session = Session()

    tema = session.query(Tema).filter(Tema.nome == nome_tema).first()

    if not tema:
        # se o tema não foi encontrado
        error_msg = "Tema não encontrado na base :/"
        logger.warning(f"Erro ao buscar tema '{nome_tema}', {error_msg}")
        return {"message": error_msg}, 404
    
    # fazendo a remoção
    count = session.query(Item).filter(Item.tema == tema.id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado todos os itens")
        return {"message": "Itens removidos", "quantidade": count}, 200
    else:
        # se o tema não foi encontrado
        error_msg = "Não há itens para deletar :/"
        logger.warning(f"Erro ao deletar itens', {error_msg}")
        return {"message": error_msg}, 404

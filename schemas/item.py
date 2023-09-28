from pydantic import BaseModel
from model.item import Item
from model.tema import Tema


class ItemSchema(BaseModel):
    """ Define como um item deve ser representado sozinho
    """
    nome_tema: str = "animais"
    nome_item: str = "cachorro"

class ItemShortSchema(BaseModel):
    """ Define como um item deve ser representado dentro do tema
    """
    nome: str = "cachorro"

    
class ItemUpdSchema(BaseModel):
    """ Define como a atualização de um item deve ser representado
    """
    nome_tema: str = "animais"
    nome_item_velho: str = "cachorro"
    nome_item_novo: str = "gato"


class ItensBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca pelo nome do tema
    """
    nome_tema: str = "animais"


class ItemBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca pelo nome do item
    """
    nome_tema: str = "animais"
    nome_item: str = "cachorro"


class ItemViewSchema(BaseModel):
    """ Define como um item será retornado: tema + item.
    """
    nome_tema: str = "animais"
    nome_item: str = "cachorro"


class ItemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

class ItensDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de todos os temas.
    """
    message: str
    quantidade: int

def apresenta_item(item: Item, tema: Tema):
    """ Retorna uma representação do item seguindo o schema definido em
        ItemViewSchema.
    """
    return {
        
        "nome_tema": tema.nome,
        "nome_item": item.nome
    }
from pydantic import BaseModel
from typing import List
from model.tema import Tema

from schemas import ItemShortSchema


class TemaSchema(BaseModel):
    """ Define como um novo tema a ser inserido deve ser representado
    """
    nome: str = "animais"

    
class TemaUpdSchema(BaseModel):
    """ Define como a atualização de um tema deve ser representado
    """
    nome_velho: str = "animais"
    nome_novo: str = "livros"


class TemaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca pelo nome do tema
    """
    nome: str = "animais"


class ListagemTemasSchema(BaseModel):
    """ Define como uma listagem de temas será retornada.
    """
    temas:List[TemaSchema]


def apresenta_temas(temas: List[Tema]):
    """ Retorna uma representação do tema seguindo o schema definido em
        TemaViewSchema.
    """
    result = []
    for tema in temas:
        result.append({
            "nome": tema.nome,
            "total_itens": len(tema.itens),
            "itens": [{"nome": c.nome} for c in tema.itens]
        })

    return {"temas": result}


class TemaViewSchema(BaseModel):
    """ Define como um tema será retornado: tema + itens.
    """
    nome: str = "animais"
    total_itens: int = 1
    itens:List[ItemShortSchema]


class TemaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

class TemasDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de todos os temas.
    """
    message: str
    quantidade: int

def apresenta_tema(tema: Tema):
    """ Retorna uma representação do tema seguindo o schema definido em
        TemaViewSchema.
    """
    return {
        "nome": tema.nome,
        "total_itens": len(tema.itens),
        "itens": [{"nome": c.nome} for c in tema.itens]
    }
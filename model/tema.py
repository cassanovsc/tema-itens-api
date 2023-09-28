from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from  model import Base, Item


class Tema(Base):
    __tablename__ = 'tema'

    id = Column("pk_tema", Integer, primary_key=True)
    nome = Column(String(140), unique=True)

    # Definição do relacionamento entre o tema e o item.
    # Essa relação é implicita, não está salva na tabela 'tema',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    itens = relationship("Item")

    def __init__(self, nome:str):
        """
        Cria um Tema

        Arguments:
            nome: nome do tema.
        """
        self.nome = nome


    def adiciona_item(self, item:Item):
        """ Adiciona um novo comentário ao Tema
        """
        for i in self.itens:
            if i.nome == item.nome:
                return 0
        self.itens.append(item)
        return 1


    def atualiza_nome_tema(self, nome_tema:str):
        """ Atualiza o nome do Tema
        """
        self.nome = nome_tema


    def atualiza_nome_item(self, nome_item_velho:str, nome_item_novo:str):
        """ Atualiza o nome de um item
        """
        for i in self.itens:
            if i.nome == nome_item_novo:
                return 0
            
        for i in self.itens:
            if i.nome == nome_item_velho:
                i.nome = nome_item_novo
                return 1

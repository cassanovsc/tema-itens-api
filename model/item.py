from sqlalchemy import Column, String, Integer, ForeignKey

from  model import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140))

    # Definição do relacionamento entre o item e um tema.
    # Aqui está sendo definido a coluna 'tema' que vai guardar
    # a referencia ao tema, a chave estrangeira que relaciona
    # um tema ao item.
    tema = Column(Integer, ForeignKey("tema.pk_tema"), nullable=False)

    def __init__(self, nome:str):
        """
        Cria um Item

        Arguments:
            nome: o nome de um item.
        """
        self.nome = nome

    def atualiza_nome(self, nome:str):
        """ Atualiza o nome do Item
        """
        self.nome = nome

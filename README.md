# API - Tema & Itens

Neste projeto foi desenvolvida uma API para a realização de CRUD para Chave - Valores, onde um Tema (chave) pode possuir vários Itens (valores).
As tecnologias utilizadas foram:
 - BackEnd: Python e [Flask](https://flask.palletsprojects.com/en/2.3.x/)
 - Banco de dados: [SQLAlchemy](https://www.sqlalchemy.org/) e [SQLite](https://www.sqlite.org/index.html)
 - Documentação: [OpenAPI3](https://swagger.io/specification/)

O objetivo aqui é mostrar parte do conteúdo aprendido durante Curso de Pós Graduação em Desenvolvimento Full Stack da PUC Rio.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5010
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5010 --reload
```

Abra o [http://localhost:5010/#/](http://localhost:5010/#/) no navegador para verificar o status da API em execução.

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t temas-itens-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5010:5010 temas-itens-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5010/#/](http://localhost:5010/#/) no navegador.


# Tarefa: Desenvolvimento de Endpoints para CRUD de Cadastro de Empresas

Este é o envio para a Tarefa: Desenvolvimento de Endpoints para CRUD de Cadastro de Empresas.

## Iniciando o Backend

Para iniciar o backend, você pode usar o Docker Compose (recomendado) seguindo estes passos:

1. Clone este repositório.
2. Entre no diretório:

`cd eStracta`

3. No terminal, insira o seguinte comando:

`docker compose up -d`

A documentação Swagger estará disponível em http://localhost:5000/docs.

## Populando a Base de Dados

Para popular a base de dados com dados mock para serem usados pelo frontend, siga estes passos:

1. Certifique-se de que a API e o banco de dados PostgreSQL estão em execução.
2. No terminal, execute o seguinte comando para tornar o script executável:

`chmod +x generate_mock.sh`

3. Em seguida, execute o script:

`./generate_mock.sh`

Os dados mock devem agora estar na base de dados e prontos para serem visualizados pelo frontend.

Para mais informações sobre o frontend, acesse [link para frontend](https://github.com/gbilton/estracta-react)

## Rodando o Aplicativo sem Docker

Se preferir rodar o aplicativo sem Docker, siga estes passos:

1. Configure um banco Postgresql com os dados:
   user: postgres
   password: eStractaPassword
   db: eStracta

- usuário: postgres
- senha: eStractaPassword
- banco de dados: eStracta

2. Clone este repositório.
3. Entre no diretório:
   `cd eStracta`
4. Crie um virtual environment:
   `python -m venv .venv`
5. Ative o virtual environment:
   `. .venv/bin/activate`
6. Instale as dependencias:
   `pip install -r requirements.txt`
7. Digite no terminal:
   `flask --app app.main run`

Obs: A senha está visível apenas para facilitar o processo, pois este é um envio de projeto temporário.

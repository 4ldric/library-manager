from flask import Flask, request
from models.books import Book  # importando a classe book armazenada no arquivo books

app = Flask(__name__)


# Criação do CRUD (Create, Read, Update, Delete)
books = []

# CREATE
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    print(data)
    return "teste"


if __name__ == "__main__":
    app.run(debug=True)
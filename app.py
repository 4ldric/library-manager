from flask import Flask, request, jsonify
from models.books import Book  # importando a classe book armazenada no arquivo books

app = Flask(__name__)


# Criação do CRUD (Create, Read, Update, Delete)
books = []
book_id_control = 1

# CREATE
@app.route('/books', methods=['POST'])
def create_book():
    global book_id_control  # recuperando acesso a variavel global para que possamos interar com a mesma
    data = request.get_json()  # Contem o acesso a informações que foi passada pelo usuario
    new_book = Book(id=book_id_control, title=data["title"], author=data.get("author", ""))  # criação do livro utilizando as informações retornadas e definindo o author como vazio caso o usuario não responda.
    book_id_control += 1
    books.append(new_book)
    return jsonify({"message": "Livro adicionado com sucesso"})  #  retorna nosso feedback em formato JSON para mais facilidade de leitura para API

# READ 
@app.route('/books', methods=['GET'])
def get_books():
    books_list =[book.get_dict() for book in books]  # retorna todos os livros na lista books em forma de dicionario para lista de livros
    output = {  #  O que sera mostrado ao usuario apos fazer a requisição
        "books": books_list,
        "total_books": len(books_list)
    }  
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
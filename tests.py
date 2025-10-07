import pytest
import requests

# CRUD
BASE_URL = 'http://127.0.0.1:5000'  # url base da aplicação

books = []

def test_create_book():
    new_book_data = {
        "title": "iracema",
        "author": "jose de alencar"
    }
    response = requests.post(f"{BASE_URL}/books", json=new_book_data)  # enviando requisição para aplicação
    assert response.status_code == 200  # validando se a resposta do teste e positiva
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    books.append(response_json["id"])

def test_get_books():
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    response_json = response.json()
    assert "books" in response_json
    assert "total_books" in response_json

def test_get_book():
    if books:
        book_id = books[0]  # pegando o primeiro livro caso exista na lista
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert book_id == response_json['id']

def test_update_book():
    # atualização do livro
    if books:
        book_id = books[0]
        payload = {
            "title": "novo titulo",
            "author": "novo autor",
            "availabre": False
        }
        response = requests.put(f"{BASE_URL}/books/{book_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        # verificação da modificação do livro
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['title'] == payload['title']
        assert response_json['author'] == payload['author']
        assert response_json['availabre'] == payload['availabre']

def test_delete_book():
    if books:
        book_id = books[0]
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 200

        # verifica se o livro foi realmente apagado
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 404

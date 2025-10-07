
📌 **Descrição:**  
CRUD para uma Biblioteca de livros, criada utilizando conceitos básicos do framework flask  

---
## 🔹 Funcionalidades

- ✅ Adicionar um novo livro
- 📋 Listar todos os livros
- ✏️ Editar informações de um livro existente
- 🔍 Visualizar apenas um livro especifico
- ❌ Remover um livro

GitHub: https://github.com/4ldric/library-manager.git

---

## 🔍 Implementação Inicial

### 📌 Criando nossa classe para importação

```python
Class Book:
	def __init__(self, id, title, author, availabre=True)  # 1
	self.id = id
	self.title = title
	self.author = author
	self.availabre = available
	
	def get_dict(self):  # 2
		return {
			"id": self.id,
			"title": self.title,
			"author": self.author,
			"availabre": self.availabre
		}
```

📌 **Explicação:**

- 1. Recebe os parâmetros do livro 
- 2.  Retorna as informações em forma de dicionario

---

### 📌 Importando requerimentos e criando nosso app

```python
# pip3 install -r requiriments.txt
from flask import Flask, request, jsonify
from models.books import Book  # 1

app = flask(__name__)  # 2
books = []  # 3
book_id_control = 1  # 4
if __name__ == "__main__":  # 5
	app.run(debug=True)
```

📌 **Explicação:**

- 1. Importamos nossa classe utilizando o caminho que ela esta localizada `pasta.arquivo`
- 2. Cria nossa variável de iniciação
- 3. Cria nossa lista de livros
- 4. Criamos nosso controlador de id dos livros
- 5. Sobe o serviço apenas se for chamado manualmente

---
## 🔍 Criando nosso CRUD
### 📌 Rota CREATE

```python
@app.route('/books', methods=['POST'])  # 1
def create_book():
	global book_id_control  # 2
	data = request.get_json()  # 3
	new_book = Book(title=data['title'], author=data.get("author", ""))  # 4
	book_id_control += 1
	books.append(new_book)
	return jsonify({"message": "Livro adicionado com sucesso"})  # 5
	
``` 

📌 **Explicação:**

- 1. Criamos nossa rota e definindo o método de requisição como `POST`
- 2. Para podermos ter acesso para modificar uma variável fora do escopo da função, temos que chama-la como global
- 3. Armazenamos as respostas do usuário através do método request
- 4. Chamando nossa classe e definindo um valor padrão caso o usuário não preencha o author
- 5. Retornando nossa mensagem de sucesso em formato `JSON`

---
### 📌 Rota READ: todos os livros

```python
@app.route('/books', methods=['GET'])
def get_books():
	book_list = [book.get_dict() for book in books]  # 1
	output = {  # 2
		"books":books_list,
		"total_books": len(books)   # 3
	}
	return jsonify(output)  
```

📌 **Explicação:**

- 1. Faz com que cada livro seja adicionado a lista em forma de dicionário
- 2. Estrutura de dicionário que será retornada 
- 3. Informa o total de livros adicionados 

---

### 📌 Rota READ: livro especifico

```python
@app.route('/books/<int:id>', methods=['GET'])  # 1
def get_book(id):
	for book in books:  # 2
		if book.id == id:
		return jsonify(book.get_dict())
	return jsonify({"message": "Livro não encontrado"}), 404  # 3
```

📌 **Explicação:**

- 1. Definindo um parâmetro de rota como inteiro para receber o id do livro
- 2. Ira percorrer cada livro da lista e verificar se o id existe e retorna o livro do id
- 3. Caso não encontre o livro e retornado feedback e também um Status Code 

---

### 📌 Rota PUT

```python
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
	data = request.get_json()  # 1
	bk = None  # 2
	for book in books:
		if book.id == id:
			bk = book
			break
	if bk is None:
		return jsonify({"message": "Livro não encontrado"}), 404
		
	bk.title = data['title']  # 3
	bk.author = data.get('author', '')
	bk.availabre = data['availabre']
	return jsonify({"message": "livro atualizado com sucesso!"})
```

📌 **Explicação:**

- 1. Pegamos novamente a resposta do usuário para atualizar o livro especificado
- 2. Criamos uma variável para armazenar o livro caso id especificado seja encontrado
- 3. Alteramos as informações do livro com as respostas novas do usuário

---

### 📌 Rota DELETE

```python
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
bk = None
for book in books:  # 1
	if book.id == id:
		bk = book
		break
if bk is None:  
	return jsonify({"message": "Livro não encontrado"}), 404
books.remove(bk)  # 2
return jsonify({"message": "Livro deletado com sucesso!"})
```

📌 **Explicação:**

- 1. Faz a verificação para ver se a o livro com id especificado, caso não haja ele da um retorno negativo
- 2. Remove o livro especificado da lista de livros

---

## 🤖 Testes automatizados
### 📌 Rota CREATE

```python
import pytest, requests

BASE_URL = 'http://127.0.0.1:5000'  # 1
books = []  # 2

def test_book_create():
	new_book_data = {  # 3
		"title": "Iracema",
		"author": "Jose de alencar"
	} 
	response = requests.post(f'{BASE_URL}/books', json=new_book_data)  # 4
	assert response.status_code == 200  # 5
	response_json = response.json()
	assert "message" in response_json
	assert "id" in response_json
	books.append(response_json['id'])
``` 

📌 **Explicação:**

- 1. Definimos nossa `BASE_URL` de teste
- 2. Criamos uma lista para armazenar ids dos livros
- 3. Criamos um pala de informações necessárias para adicionar um livro
- 4. Estamos armazenando a requisição `POST` para nosso servidor e repassando os parâmetros necessários para a adição do livro
- 5. Passando a validação do nosso teste de acordo com os requisitos

---
### 📌 Rota READ: todos os livres

```python
def test_get_books():
	response = requests.get(f'{BASE_URL}/books')
	assert response.status_code == 200
	response_json = response.json()
	assert "books" in response_json
	assert "total_books" in response_json
``` 

📌 **Explicação:**

---
### 📌 Rota READ: livro especifico

```python
def test_get_book():
	if books:  # 1
		book_id = books[0] 
		response = requests.get(f'{BASE_URL}/books/{book_id}')
		assert response.status_code == 200
		response_json = response.json()
		assert book_id == response_json["id"]
``` 

📌 **Explicação:**

- 1. Ira verificar se existe algum livro adicionado e ira realizar o teste

---

### 📌 Rota UPDATE

```python
def test_update_book():
	if books:
		book_id = books[0]
		payload = {  
			"title": "novo titulo",
			"author": "novo autor",
			"availabre": False
		}
		
		response = requests.put(f'{BASE_URL}/books/{book_id}', json= payload)
		assert response.status_code == 200
		
		response = requests.get(f'{BASE_URL}/books/{book_id}') # 1
		assert response.status_code == 200
		response_json = response.json()
		assert response_json['title'] == payload['title']  
		assert response_json['author'] == payload['author']
		assert response_json['availabre'] == payload['availabre']
	
``` 

📌 **Explicação:**

- 1. Faz uma nova requisição para verificar se as informações foram atualizadas

---
### 📌 Rota DELETE

```python
def test_delete_book():
	if books:
		book_id = books[0]
		response = requests.delete(f'{BASE_URL}/books{book_id}')
		assert response.status_code == 200
		
		response = requests.get(f'{BASE_URL}/books/{book_id}')  # 1
		assert response.status_code == 404
``` 

📌 **Explicação:**

- 1. Realiza uma nova requisição e verifica se o livro foi excluído retornando o status Code 404


---







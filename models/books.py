class Book:
    def __init__(self, id, title, author, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.availabre = available

    def get_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "availabre": self.availabre
        }

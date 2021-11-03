import uuid
from flask import session

from src.commom.database import Database
from src.models.users import Users
Database.initialize()


class Books(object):
    def __init__(self, title, author, isbn, lang, pages, genre, publisher, price, edition, quantity, description,  _id=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.lang = lang
        self.pages = pages
        self.genre = genre
        self.publisher = publisher
        self.price= price
        self.edition= edition
        self.quantity= quantity
        self.description = description
        self.id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def book_add(cls, title, author, isbn, lang, pages, genre, publisher, price, edition, description, quantity, email):
        new_book = cls(title, author, isbn, lang, pages, genre, publisher, price, edition, quantity, description)
        new_book.book_add_to_db()
        user1 = Users.get_by_email(f'u_email= \'{email}\'')
        bookid = {f'{new_book.id}'}
        Database.update(collection='users', data=f"u_booklist = u_booklist + {bookid}",
                        query=f"u_id=\'{user1.u_id}\'")

    def book_add_to_db(self):
        return Database.insert(collection='bookdata', data=self.format_my_data())

    def format_my_data(self):
        return f"(b_title, b_author, b_isbn, b_lang, b_pages, b_genre, b_publisher, b_price, b_edition, " \
               f"b_description, b_quantity, b_id) values(\'{self.title}\', \'{self.author}\', \'{self.isbn}\', \'{self.lang}\',  " \
               f"{self.pages}, \'{self.genre}\', \'{self.publisher}\',{self.price},\'{self.edition}\'," \
               f"\'{self.description}\',{self.quantity},\'{self.id}\') "

    @classmethod
    def find_book(cls, book_id):
        data = Database.find(collection='bookdata', query=f"b_id = \'{book_id}\'")
        return data

    @classmethod
    def get_book_by_id(cls, bookid):
        book = Database.find(collection='bookdata', query=f"b_id = \'{bookid}\'")
        if book is not None:
            return book

    @staticmethod
    def add_review(comment, rating, bookid ):
        book = Database.find(collection='bookdata', query=f"b_id = \'{bookid}\'")
        final_rating= int(rating)
        bookreview = {f'{comment}': final_rating}
        Database.update(collection='bookdata', data=f"b_review = b_review + {bookreview}",
                        query=f"b_id=\'{book.b_id}\'")
        book_column_to_update = ''
        count=0
        if final_rating == 5:
            book_column_to_update = 'b_five'
            count= book.b_five +1
        elif final_rating == 4:
            book_column_to_update = 'b_four'
            count = book.b_four + 1
        elif final_rating == 3:
            book_column_to_update = 'b_three'
            count = book.b_three + 1
        elif final_rating == 2:
            book_column_to_update = 'b_two'
            count = book.b_two + 1
        elif final_rating == 1:
            book_column_to_update = 'b_one'
            count = book.b_one + 1
        Database.update(collection='bookdata', data=f'{book_column_to_update} = {count}',
                        query=f"b_id=\'{book.b_id}\'")


    @staticmethod
    def add_filter(type, genre):
        books = Users.get_books()
        booklist = []
        for i in books:
            if type:
                if not genre:
                    if i.b_type in type:
                        booklist.append(i)
                else:
                    if i.b_type in type:
                        if i.b_genre in genre:
                            booklist.append(i)
            elif genre:
                if not type:
                    if i.b_genre in genre:
                        booklist.append(i)
            else:
                return books
        return booklist


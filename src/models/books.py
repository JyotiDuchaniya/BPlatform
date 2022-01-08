import uuid
import os
from src.application_logging.logger import App_Logger
from src.commom.database import Database
from src.models.users import Users
Database.initialize()

file_path = '../Blogs_logs/Book_Log.txt'
os.makedirs(os.path.dirname(file_path), exist_ok=True)

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
        user1 = Users.get_by_email(f"u_email= '{email}'")
        bookid = {f'{new_book.id}'}
        Database.update(collection='users', data=f"u_booklist = u_booklist + {bookid}",
                        query=f"u_id='{user1.u_id}'")
        App_Logger.log(file_path, "New book i.e. %s uploaded by %s " % (new_book.title, user1.u_name))

    def book_add_to_db(self):
        App_Logger.log(file_path, "New book i.e. %s uploaded by database " % self.title)
        return Database.insert(collection='bookdata', data=self.format_my_data())

    def format_my_data(self):
        return f"(b_title, b_author, b_isbn, b_lang, b_pages, b_genre, b_publisher, b_price, b_edition, " \
               f"b_description, b_quantity, b_id) values(\'{self.title}\', \'{self.author}\', \'{self.isbn}\', \'{self.lang}\',  " \
               f"{self.pages}, \'{self.genre}\', \'{self.publisher}\',{self.price},\'{self.edition}\'," \
               f"\'{self.description}\',{self.quantity},\'{self.id}\') "

    @classmethod
    def find_book(cls, book_id):
        data = Database.find(collection='bookdata', query=f"b_id = '{book_id}'")
        App_Logger.log(file_path, "Book i.e. %s found as per query " % data.b_title)
        return data

    @classmethod
    def get_book_by_id(cls, bookid):
        book = Database.find(collection='bookdata', query=f"b_id ='{bookid}'")
        App_Logger.log(file_path, "Book i.e. %s found as per book_id given " % book.b_title)
        if book is not None:
            return book

    @staticmethod
    def add_review(comment, rating, bookid ):
        try:
            book = Database.find(collection='bookdata', query=f"b_id = '{bookid}'")
            final_rating= int(rating)
            bookreview = {f'{comment}': final_rating}
            Database.update(collection='bookdata', data=f"b_review = b_review + {bookreview}",
                            query=f"b_id='{book.b_id}'")
            App_Logger.log(file_path, "Review added for book: %s" % book.b_title)
            book_column_to_update = ''
            count=0
            if final_rating == 5:
                book_column_to_update = 'b_five'
                if book.b_five:
                    count= book.b_five +1
                else:
                    count= 1
            elif final_rating == 4:
                book_column_to_update = 'b_four'
                if book.b_four:
                    count = book.b_four + 1
                else:
                    count = 1
            elif final_rating == 3:
                book_column_to_update = 'b_three'
                if book.b_three:
                    count = book.b_three + 1
                else:
                    count = 1
            elif final_rating == 2:
                book_column_to_update = 'b_two'
                if book.b_two:
                    count = book.b_two + 1
                else:
                    count = 1
            elif final_rating == 1:
                book_column_to_update = 'b_one'
                if book.b_one:
                    count = book.b_one + 1
                else:
                    count = 1
            Database.update(collection='bookdata', data=f'{book_column_to_update} = {count}',
                            query=f"b_id='{book.b_id}'")
        except Exception as e:
            App_Logger.log(file_path, "error:: %s" % e)

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
                App_Logger.log(file_path, "All the books loaded")
                return books
        App_Logger.log(file_path, "The books based on genre as %s and type as %s loaded." % (genre, type))
        return booklist

    @staticmethod
    def search_book(keyword):
        all_books= Users.get_books()
        booklist=[]
        for i in all_books:
            if str.lower(keyword) in str.lower(i.b_title):
                booklist.append(i)
        App_Logger.log(file_path, "The books matching keyword : %s loaded." % keyword)
        return booklist


import uuid
from flask import session

from src.commom.database import Database
Database.initialize()


class Users(object):
    def __init__(self, email, password, username, _id=None):
        self.email = email
        self.password = password
        self.username = username
        self.id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, query):
        users = Database.find(collection='users', query=query)
        if users is not None:
            return users
        else:
            return None

    @classmethod
    def get_by_id(cls, _id):
        users = Database.find(collection='users', query=f"u_id = \'{_id}\'")
        if users is not None:
            return users

    @staticmethod
    def login_valid(email, password):
        user_valid = Users.get_by_email(f'u_email= \'{email}\'')
        if user_valid is not None:
            print(user_valid)
            print(user_valid.u_pwd)
            return user_valid.u_pwd == password
        else:
            return False

    @classmethod
    def register(cls, email, password, username):
        user = cls.get_by_email(f'u_email= \'{email}\'')
        if user is None:
            new_user = cls(email, password, username)
            print(new_user.email)
            session['email'] = email
            new_user.save_to_db()

    @staticmethod
    def login(email):
        session['email'] = email

    @staticmethod
    def logout():
        session['email'] = None

    @staticmethod
    def get_books():
        data = Database.find('bookdata')
        return data

    def format_my_data_insert(self):
        return f"(u_email, u_pwd, u_username, u_id) values(\'{self.email}\', \'{self.password}\', \'{self.username}\',\'{self.id}\')"

    def save_to_db(self):
        return Database.insert(collection='users', data=self.format_my_data_insert())

    @staticmethod
    def update_profile(name, username, phone, email):
        user_profile = Users.get_by_email(f'u_email= \'{email}\'')
        Database.update(collection='users', data=Users.format_my_data_update_profile(name, username, phone),
                        query=f"u_id=\'{user_profile.u_id}\'")

    @staticmethod
    def format_my_data_update_profile(name, username, phone):
        return f"u_name=\'{name}\', u_username=\'{username}\',u_phone=\'{phone}\'"

    @staticmethod
    def update_address(street, pin, city, state, country, email):
        user_profile1 = Users.get_by_email(f'u_email= \'{email}\'')
        Database.update(collection='users', data=Users.format_my_data_update_address(street, pin, city, state, country),
                        query=f"u_id=\'{user_profile1.u_id}\'")

    @staticmethod
    def format_my_data_update_address(street, pin, city, state, country):
        return f"u_street=\'{street}\', u_pin=\'{pin}\',u_city=\'{city}\',u_state=\'{state}\',u_country=\'{country}\'"

    @staticmethod
    def add_book_to_cart(bookid, email):
        user1= Users.get_by_email(f'u_email= \'{email}\'')
        check= f'\'{bookid}\''
        print(check)

        if user1.u_cart is not None:
            flag = False
            for i in user1.u_cart:
                if i == check:
                    flag = True
            if flag:
                Users.add_book_quantity(bookid,email)
            else:
                book_id = {f'{bookid}': 1}
                Database.update(collection='users', data=f"u_cart = u_cart + {book_id}",
                            query=f"u_id=\'{user1.u_id}\'")
        else:
            book_id = {f'{bookid}': 1}
            Database.update(collection='users', data=f"u_cart = u_cart + {book_id}",
                            query=f"u_id=\'{user1.u_id}\'")

    @staticmethod
    def add_book_quantity(book_id,email):
        user1= Users.get_by_email(f'u_email= \'{email}\'')
        c= user1.u_cart[f'{book_id}']
        add_book_count = {f'{book_id}': c+1}
        Database.update(collection='users', data=f"u_cart = u_cart + {add_book_count}", query=f"u_id=\'{user1.u_id}\'")

    @staticmethod
    def delete_book_quantity(book_id, email):
        user1 = Users.get_by_email(f'u_email= \'{email}\'')
        c = user1.u_cart[f'{book_id}']
        if c>1:
            sub_book_count = {f'{book_id}': c - 1}
            Database.update(collection='users', data=f"u_cart = u_cart + {sub_book_count}",
                            query=f"u_id=\'{user1.u_id}\'")
        else:
            Database.delete(collection='users', columns=f'u_cart[\'{book_id}\']', query=f"u_id=\'{user1.u_id}\'")


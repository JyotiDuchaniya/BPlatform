import random, uuid, os
from datetime import datetime, timedelta
from flask import session

from src.application_logging.logger import App_Logger
from src.commom.database import Database
Database.initialize()

file_path = '../Blogs_logs/Users_Log.txt'
os.makedirs(os.path.dirname(file_path), exist_ok=True)

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
            App_Logger.log(file_path, "User found having email address as %s" % users.u_email)
            return users
        else:
            App_Logger.log(file_path, "No user found")
            return None

    @classmethod
    def get_by_id(cls, _id):
        users = Database.find(collection='users', query=f"u_id = '{_id}'")
        if users is not None:
            App_Logger.log(file_path, "User found having user ID as %s" % users.u_id)
            return users

    @staticmethod
    def login_valid(email, password):
        user_valid = Users.get_by_email(f"u_email= '{email}'")
        if user_valid is not None:
            App_Logger.log(file_path, "Checking the user's password")
            return user_valid.u_pwd == password
        else:
            App_Logger.log(file_path, "No user found for this email ID: %s" % email)
            return False

    @classmethod
    def register(cls, email, password, username):
        user = cls.get_by_email(f"u_email= '{email}'")
        if user is None:
            new_user = cls(email, password, username)
            session['email'] = email
            new_user.save_to_db()
            App_Logger.log(file_path, "New user added in BPlatform database having email address %s" % email)

    @staticmethod
    def login(email):
        session['email'] = email
        App_Logger.log(file_path, "Successfully logged in via email address %s" % email)

    @staticmethod
    def logout():
        session['email'] = None
        App_Logger.log(file_path, "Logged Out")

    @staticmethod
    def get_books():
        data = Database.find('bookdata')
        App_Logger.log(file_path, "All books loaded for user")
        return data

    def format_my_data_insert(self):
        return f"(u_email, u_pwd, u_username, u_id) values(\'{self.email}\', \'{self.password}\', \'{self.username}\',\'{self.id}\')"

    def save_to_db(self):
        return Database.insert(collection='users', data=self.format_my_data_insert())

    @staticmethod
    def update_profile(name, username, phone, email):
        user_profile = Users.get_by_email(f"u_email= '{email}'")
        Database.update(collection='users', data=Users.format_my_data_update_profile(name, username, phone),
                        query=f"u_id='{user_profile.u_id}'")
        App_Logger.log(file_path, "Profile Updated for user - %s" % user_profile.u_name)

    @staticmethod
    def format_my_data_update_profile(name, username, phone):
        return f"u_name='{name}', u_username='{username}',u_phone='{phone}'"

    @staticmethod
    def update_address(street, pin, city, state, country, email):
        user_profile1 = Users.get_by_email(f"u_email= '{email}'")
        Database.update(collection='users', data=Users.format_my_data_update_address(street, pin, city, state, country),
                        query=f"u_id='{user_profile1.u_id}'")
        App_Logger.log(file_path, "Address Updated for user - %s" % user_profile1.u_name)

    @staticmethod
    def change_password(old_pwd, new_pwd, confirm_pwd,  email):
        # if new_pwd == confirm_pwd:
        user_profile1 = Users.get_by_email(f"u_email= '{email}'")
        if old_pwd == user_profile1.u_pwd:
            Database.update(collection='users', data=f"u_pwd='{new_pwd}'",
                    query=f"u_id='{user_profile1.u_id}'")
        App_Logger.log(file_path, "Password Updated for user - %s" % user_profile1.u_name)

    @staticmethod
    def format_my_data_update_address(street, pin, city, state, country):
        return f"u_street='{street}', u_pin='{pin}',u_city='{city}',u_state='{state}',u_country='{country}'"

    @staticmethod
    def add_book_to_cart(bookid, email):
        user1= Users.get_by_email(f"u_email= '{email}'")
        check= f'\'{bookid}\''
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
                            query=f"u_id='{user1.u_id}'")
        else:
            book_id = {f'{bookid}': 1}
            Database.update(collection='users', data=f"u_cart = u_cart + {book_id}",
                            query=f"u_id='{user1.u_id}'")
        App_Logger.log(file_path, "Book user added in profile of %s" % user1.u_name)

    @staticmethod
    def add_book_quantity(book_id,email):
        user1= Users.get_by_email(f"u_email= '{email}'")
        c= user1.u_cart[f'{book_id}']
        add_book_count = {f'{book_id}': c+1}
        Database.update(collection='users', data=f"u_cart = u_cart + {add_book_count}", query=f"u_id=\'{user1.u_id}\'")
        App_Logger.log(file_path, "Quantity increased for book- %s in profile of %s" % (book_id, user1.u_name))

    @staticmethod
    def delete_book_quantity(book_id, email):
        user1 = Users.get_by_email(f"u_email= '{email}'")
        c = user1.u_cart[f'{book_id}']
        if c>1:
            sub_book_count = {f'{book_id}': c - 1}
            Database.update(collection='users', data=f"u_cart = u_cart + {sub_book_count}",
                            query=f"u_id='{user1.u_id}'")
            App_Logger.log(file_path, "Quantity decreased for book- %s in profile of %s" % (book_id, user1.u_name))
        else:
            Database.delete(collection='users', columns=f'u_cart['{book_id}']', query=f"u_id='{user1.u_id}'")
            App_Logger.log(file_path, "Book having bookID as %s removed from profile of %s" % (book_id, user1.u_name))

    @staticmethod
    def add_order_history(email, order_id):
        user = Users.get_by_email(f"u_email= '{email}'")
        for i in user.u_cart:
            rand_no= random.randint(1,100)
            order= {f'{rand_no}${i}':f'{user.u_cart[i]}${order_id}'}
            Database.update(collection='users', data=f"u_orderhistory= u_orderhistory + {order}",
                            query=f"u_id='{user.u_id}'")
            App_Logger.log(file_path, "New ordered books added in book history" )

    @staticmethod
    def clear_cart(email):
        user = Users.get_by_email(f"u_email= '{email}'")
        Database.delete(collection='users', columns='u_cart', query=f"u_id='{user.u_id}'")
        App_Logger.log(file_path, "card cleared for %s" % email)

    @staticmethod
    def update_book_shipping_status(bookid, status, email, orderid):
        user = Users.get_by_email(f"u_email= '{email}'")
        book_status = {f'{orderid}${bookid}': status}
        Database.update(collection='users', data=f'u_booklist2= u_booklist2 +  {book_status}',
                        query=f"u_id='{user.u_id}'")
        App_Logger.log(file_path, "Shipping status updated for order ID %s and book ID as %s" % (orderid, bookid))

    @staticmethod
    def update_book_order_date( email, orderid):
        user = Users.get_by_email(f"u_email= '{email}'")
        today = datetime.now()
        date1 = today.strftime('%b %d,%Y')
        receive_date = (today + timedelta(days=7)).strftime('%b %d,%Y')
        order_date = {f'{orderid}': f'{date1}${receive_date}'}
        Database.update(collection='users', data=f'u_ordertimestamp= u_ordertimestamp +  {order_date}',
                        query=f"u_id='{user.u_id}'")
        App_Logger.log(file_path, "Book order date added for orderID %s" % orderid)

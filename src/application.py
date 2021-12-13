from flask import *
import razorpay
from src.commom.database import Database
from src.models.users import Users
from src.models.blogs import Blogs
# from flask import Flask, render_template, request, session, url_for, redirect
from src.models.books import Books

# Database.initialize()
# Database.insert(collection='usersdata', data="(u_id , u_email) values(2,'hello')")
# Database.find(collection='usersdata', query=f'u_id = {value}')
# Database.update(collection='usersdata', data="u_name = 'Joss', u_username = 'Nathan'", query="u_id=2")
# Database.delete(collection='bookdata', columns='b_title, b_author', query='b_id=1')
# Users.login_valid("email2", "password2")
# Users.register("email2", "password2", "username2")
# Users.get_books()
# Books.find_book(23)
# Books.book_add("abc","abc","abc","abc",123,"abc","abc")
# Blogs.new_post(blog_title='post 1', blog_description='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',email= 'ab1@mailinator.com')

application = Flask(__name__)
application.secret_key = 'let'


@application.before_first_request
def database_initialize():
    Database.initialize()
    if 'email' not in session:
        session['email']= None


@application.route('/')
@application.route('/welcome')
def welcome():
    email=session['email']
    return render_template('Welcome.html', email=email, title='Welcome')


@application.route('/login')
def login():
    return render_template('login.html')


@application.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    if Users.login_valid(email, password):
        Users.login(email)
    else:
        flash('Incorrect Credentials!!', category='error')
        session['email'] = None
        return redirect(url_for('login'))
    return redirect(url_for('buy'))


@application.route('/register')
def register_get():
    return render_template('SignUp.html')


@application.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    user = Users.get_by_email(f'u_email= \'{email}\'')
    if user is not None:
        if user.u_pwd == password and user.u_email == email:
            flash('Already an user!!', category='error')
            return redirect(url_for('login'))
        elif user.u_pwd != password and user.u_email == email:
            flash('Already an user!!', category='error')
            return redirect(url_for('login'))
    else:
        Users.register(email, password, username)
        flash('User is successfully registered!!', category='success')
        session['email'] = email
        return redirect(url_for('welcome'))


# @app.route('/signup')
# def signup():
#     return render_template("SignUp.html")


@application.route('/welcome/buy/search', methods=['POST'])
def search_books():
    search_keyword = request.form['search-keyword']
    result = []
    result = Books.search_book(search_keyword)
    books = Users.get_books()
    email = session['email']
    cartbook1 = []
    genre_list1 = []
    if session['email'] is not None:
        user = Users.get_by_email(f'u_email= \'{email}\'')
        if user.u_cart is not None:
            for i in user.u_cart:
                cartbook1.append(i)
    for y in books:
        if y.b_genre not in genre_list1:
            genre_list1.append(y.b_genre)
    return render_template('Buy-Contents-Main-Page.html', data=result, genre_list=genre_list1, type='', genre='',
                           cartbook=cartbook1, email=email)


@application.route('/welcome/buy')
def buy():
    books = Users.get_books()
    email = session['email']
    cartbook = []
    genre_list = []
    if session['email'] is not None:
        user = Users.get_by_email(f'u_email= \'{email}\'')
        if user.u_cart is not None:
            for i in user.u_cart:
                cartbook.append(i)
    for y in books:
        if y.b_genre not in genre_list:
            genre_list.append(y.b_genre)
    return render_template('Buy-Contents-Main-Page.html', data=Users.get_books(), genre_list=genre_list,
                           cartbook=cartbook, email=email)


@application.route('/welcome/filter', methods=['POST'])
def buy_filter():
    book_type = request.form.getlist('type[]')
    genre = request.form.getlist('genre[]')
    books1 = Books.add_filter(type, genre)
    books = Users.get_books()
    email = session['email']
    cartbook1 = []
    genre_list1 = []
    if session['email'] is not None:
        user = Users.get_by_email(f'u_email= \'{email}\'')
        if user.u_cart is not None:
            for i in user.u_cart:
                cartbook1.append(i)
    for y in books:
        if y.b_genre not in genre_list1:
            genre_list1.append(y.b_genre)
    return render_template('Buy-Contents-Main-Page.html', data=books1, genre_list=genre_list1, type=book_type,
                           genre=genre, cartbook=cartbook1, email=email)


@application.route('/welcome/buy/<string:b_id>')
def book_specific(b_id):
    book = Books.find_book(b_id)
    email = session['email']
    user = Users.get_by_email(f'u_email= \'{email}\'')
    flag = False
    if session['email'] is not None:
        user = Users.get_by_email(f'u_email= \'{email}\'')
        if user.u_cart:
            for i in user.u_cart:
                if i == book.b_id:
                    flag = True
    book = Books.find_book(b_id)
    if book.b_review is None:
        reviewflag = False
    else:
        reviewflag = True
    return render_template("Book-Detail-Page.html", book=book, flag=flag, reviewflag=reviewflag, email=email)


@application.route('/welcome/buy/<string:b_id>/review', methods=['POST'])
def add_book_review(b_id):
    comment = request.form['rating-input-class']
    star = request.form['star']
    Books.add_review(comment, star, b_id)
    flash('Review Added.', category='success')
    return redirect(f'/welcome/buy/{b_id}')


@application.route('/welcome/buy/main/<string:b_id>')
def add_to_cart(b_id):
    email = session['email']
    Users.add_book_to_cart(b_id, email)
    return redirect(url_for('buy'))


@application.route('/welcome/buy/<string:b_id>/add-to-cart')
def add_to_cart_book_specific(b_id):
    email = session['email']
    Users.add_book_to_cart(b_id, email)
    return redirect(f'/welcome/buy/{b_id}')


@application.route('/welcome/sell', methods=['POST'])
def upload_book():
    title = request.form['book-title']
    author = request.form['book-author']
    isbn = request.form['book-isbn']
    lang = request.form['book-lang']
    pages = request.form['book-pages']
    genre = request.form['book-genre']
    publisher = request.form['book-publisher']
    price = request.form['book-price']
    edition = request.form['book-edition']
    quantity = request.form['book-quantity']
    description = request.form['book-description']
    email = session['email']
    if email:
        if title and author and isbn and lang and genre and publisher and price and edition and description and quantity:
            Books.book_add(title, author, isbn, lang, pages, genre, publisher, price, edition, description, quantity, email)
            flash('Book has been successfully uploaded', category='success')
            return redirect(url_for('booklist'))
        else:
            flash('Not all fields are filled!', category= 'error')
            return redirect(url_for('upload_book'))
    else:
        return redirect(url_for('login'))


@application.route('/welcome/forum')
def forum():
    posts= Blogs.all_posts()
    total_posts = Database.find_length(collection='forum')
    email= session['email']
    count1=0
    for i in total_posts:
        count1 = i.count
    return render_template('Forum-Main-Page.html', posts = posts, count=count1, email=email)


@application.route('/welcome/forum', methods=['POST'])
def new_post():
    email = session['email']
    title = request.form['blog-title']
    description = request.form['blog-description']
    Blogs.new_post(title, description, email)
    flash('New Blog has been added!!',category= 'success')
    return redirect('/welcome/forum')


@application.route('/welcome/forum/<string:blog_id>')
def post_specific(blog_id):
    email= session['email']
    comments= None
    post = Blogs.one_post(blog_id)
    comments = Blogs.comments(blog_id)
    if comments:
        total_comments= len(comments)
    else:
        total_comments= 0
    return render_template('Blog-Specific-Page.html', post=post, comments=comments, total_comments=total_comments, email=email)


@application.route('/welcome/forum/<string:blog_id>/comment', methods=['POST'])
def post_specific_comment(blog_id):
    email= session['email']
    user= Users.get_by_email(f'u_email= \'{email}\'')
    comment= request.form['text-area']
    Blogs.post_comment(user.u_name, comment, blog_id)
    flash('Your views has been shared!!',category= 'success')
    return redirect(f'/welcome/forum/{blog_id}')


@application.route('/welcome/sell')
def sell():
    email= session['email']
    return render_template('Sell-Section.html', email=email)


@application.route('/welcome/sell/booklist')
def booklist():
    email = session['email']
    if email:
        user = Users.get_by_email(f'u_email= \'{email}\'')
        booklist = []
        if user.u_booklist:
            for i in user.u_booklist:
                book = Books.get_book_by_id(i)
                booklist.append(book)
        return render_template('book-list-of-sellers.html', booklist=booklist)
    else:
        return render_template(url_for('login'))


@application.route('/users/<string:type>/my-account')
def account(type):
    if session['email']:
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        return render_template('My-Account.html', user=user, type=type)
    else:
        return render_template(url_for('login'))

@application.route('/users/buy/order-history')
def order_history():
    if session['email']:
        email= session['email']
        user= Users.get_by_email(f'u_email= \'{email}\'')
        orders = []
        book_order_status=[]
        book_order_date = []
        if user.u_orderhistory:
            for i in user.u_orderhistory:
                bookid= i.split('$')
                book= Books.get_book_by_id(bookid[1])
                orderdetails= user.u_orderhistory[i].split('$')
                order=[book, orderdetails[0], orderdetails[1]]
                orders.append(order)
        if user.u_ordertimestamp:
            for i in user.u_ordertimestamp:
                order_date= user.u_ordertimestamp[i].split('$')
                date= [i, order_date[0],order_date[1]]
                book_order_date.append(date)
        return render_template('My-Order-History.html', orders= orders, user=user, book_order_date=book_order_date)
    else:
        return render_template(url_for('login'))


@application.route('/users/buy/my-cart')
def cart():
    if session['email']:
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        cartbook = []
        if user.u_cart is None:
            return redirect(url_for('buy'))
        for i in user.u_cart:
            book = Books.get_book_by_id(i)
            cartbook.append(book)
        return render_template('My-Cart.html', cartbook=cartbook, user=user)
    else:
        return render_template(url_for('login'))


@application.route('/users/<string:type>/my-account', methods=['POST'])
def account_update(type):
    if session['email']:
        name = request.form['name']
        phone = request.form['phone']
        username = request.form['username']
        email = session['email']
        Users.update_profile(name, username, phone, email)
        if type == 'sell':
            return redirect('/users/sell/my-account')
        elif type == 'buy':
            return redirect('/users/sell/my-account')
    else:
        return render_template(url_for('login'))


@application.route('/users/<string:type>/my-account/update-address', methods=['POST'])
def update_address(type):
    if session['email']:
        street = request.form['street']
        pin = request.form['pin']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        email = session['email']
        Users.update_address(street, pin, city, state, country, email)
        flash('User Details updated!!',category= 'success')
        if type == 'sell':
            return redirect('/users/sell/my-account')
        elif type == 'buy':
            return redirect('/users/sell/my-account')
    else:
        return render_template(url_for('login'))


@application.route('/users/<string:type>/my-account/change-password', methods=['POST'])
def change_pwd(type):
    if session['email']:
        email= session['email']
        old_pwd = request.form['old-password']
        new_pwd = request.form['new-password']
        confirm_pwd = request.form['confirm-password']
        Users.change_password(old_pwd, new_pwd, confirm_pwd, email)
        flash('Password successfully changed!!',category= 'success')
        if type == 'sell':
            return redirect('/users/sell/my-account')
        elif type == 'buy':
            return redirect('/users/sell/my-account')
    else:
        return render_template(url_for('login'))


@application.route('/users/buy/my-cart/update-address', methods=['POST'])
def update_address_via_my_cart():
    if session['email']:
        street = request.form['street']
        pin = request.form['pin']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        email = session['email']
        Users.update_address(street, pin, city, state, country, email)
        flash('Shipping Address Updated!!',category= 'success')
        return redirect(url_for("cart"))
    else:
        return render_template(url_for('login'))


@application.route('/users/buy/my-cart/add-book/<string:b_id>')
def add_same_book_in_cart(b_id):
    if session['email']:
        email = session['email']
        Users.add_book_quantity(b_id, email)
        return redirect(url_for('cart'))
    else:
        return render_template(url_for('login'))


@application.route('/users/buy/my-cart/delete-book/<string:b_id>')
def delete_same_book_in_cart(b_id):
    if session['email']:
        email = session['email']
        Users.delete_book_quantity(b_id, email)
        return redirect(url_for('cart'))
    else:
        return render_template(url_for('login'))


@application.route('/users/logout')
def logout():
    session['email'] = None
    flash('Successfully logged out!!', category='success')
    return redirect('/')


@application.route('/users/buy/pay', methods=['GET', 'POST'])
def pay():
    if session['email']:
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        if user.u_cart is None:
            return redirect(url_for('buy'))
        total_price=0
        for i in user.u_cart:
            book = Books.get_book_by_id(i)
            total_price= total_price + book.b_price*user.u_cart[i]
        final_price= round(total_price-0.1*total_price+20)
        client= razorpay.Client(auth= ('rzp_test_kJDRaiqaU5kUyN','qsUTlyWvCWeZjGiKYLbPWu2o'))
        payment=client.order.create({'amount': int(final_price * 100), 'currency' : 'INR', 'payment_capture': '1'})
        session['order_id']= payment['id']
        return render_template('initiate-payment.html', payment=payment)
    else:
        return render_template(url_for('login'))

@application.route('/users/buy/pay/success', methods=['GET', 'POST'])
def success():
    if session['email']:
        order_id= session['order_id']
        email = session['email']
        Users.add_order_history(email, order_id)
        Users.clear_cart(email)
        user = Users.get_by_email(f'u_email= \'{email}\'')
        if user.u_orderhistory:
            for i in user.u_orderhistory:
                bookid = i.split('$')
                orderid= user.u_orderhistory[i].split('$')
                Users.update_book_shipping_status(bookid[1], 1, email, orderid[1])
                Users.update_book_order_date(email,orderid[1])
        return render_template('Sucess.html')
    else:
        return render_template(url_for('login'))


@application.route('/test', methods=['POST'])
def test():
    Database.update(collection='users', data="u_address = 'check'", query="u_id = '32403'" )
    return '', 204


if __name__ == '__main__':
    application.run(port=8000)

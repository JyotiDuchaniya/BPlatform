from src.commom.database import Database
from src.models.users import Users
from src.models.blogs import Blogs
from flask import Flask, render_template, request, session, url_for, redirect
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

app = Flask(__name__)
app.secret_key = 'let'


@app.before_first_request
def database_initialize():
    Database.initialize()
    if 'email' not in session:
        session['email']= None


@app.route('/')
@app.route('/login')
def login():

    if session['email'] is None:
        return render_template('login.html')
    else:
        print('else')
        return redirect(url_for('welcome_users'))


@app.route('/login', methods=['POST'])
def login_post():
    if session['email'] is None:
        email = request.form['email']
        password = request.form['password']
        if Users.login_valid(email, password):
            Users.login(email)
        else:
            session['email'] = None
        return redirect(url_for('welcome_users'))
    else:
        return redirect(url_for('welcome_users'))


@app.route('/welcome', methods=['GET'])
def welcome_users():
    if session['email'] is not None:
        return render_template('Welcome.html')
    else:
        return redirect('/')


@app.route('/register')
def register_get():
    if session['email'] is None:
        return render_template('SignUp.html')
    else:
        return redirect(url_for('welcome_users'))


@app.route('/register', methods=['POST'])
def register_user():
    if session['email'] is None:
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        if not Users.login_valid(email, password):
            Users.register(email, password, username)
            session['email'] = email
        else:
            return 'User exists'
        return redirect(url_for('welcome_users'))
    else:
        return redirect(url_for('welcome_users'))


# @app.route('/signup')
# def signup():
#     return render_template("SignUp.html")


@app.route('/welcome/buy/search', methods=['POST'])
def search_books():
    search_keyword = request.form('search-keyword')
    Database.find(collection='bookdata', query='b_title = \'Changeling~\'')
    return 'welcome'


@app.route('/welcome/buy')
def buy():
    if session['email'] is not None:
        books = Users.get_books()
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        cartbook = []
        genre_list = []
        if user.u_cart is not None:
            for i in user.u_cart:
                cartbook.append(i)
        for y in books:
            if y.b_genre not in genre_list:
                genre_list.append(y.b_genre)
        return render_template('Buy-Contents-Main-Page.html', data=Users.get_books(), genre_list=genre_list,
                               cartbook=cartbook)
    else:
        return redirect('/')


@app.route('/welcome/filter', methods=['POST'])
def buy_filter():
    if session['email'] is not None:
        type = request.form.getlist('type[]')
        genre= request.form.getlist('genre[]')
        books1 = Books.add_filter(type,genre)
        books= Users.get_books()
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        cartbook1 = []
        genre_list1 = []
        if user.u_cart is not None:
            for i in user.u_cart:
                cartbook1.append(i)
        for y in books:
            if y.b_genre not in genre_list1:
                genre_list1.append(y.b_genre)
        return render_template('Buy-Contents-Main-Page.html', data=books1, genre_list=genre_list1,type=type, genre=genre,
                               cartbook=cartbook1)
    else:
        return redirect('/')


@app.route('/welcome/buy/<string:b_id>')
def book_specific(b_id):
    if session['email'] is not None:
        book = Books.find_book(b_id)
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        flag = False
        if user.u_cart:
            for i in user.u_cart:
                if i == book.b_id:
                    flag = True
        book = Books.find_book(b_id)
        if book.b_review is None:
            reviewflag = False
        else:
            reviewflag = True
        return render_template("Book-Detail-Page.html", book=book, flag=flag, reviewflag=reviewflag)
    else:
        return redirect('/')


@app.route('/welcome/buy/<string:b_id>/review', methods=['POST'])
def add_book_review(b_id):
    if session['email'] is not None:
        comment = request.form['rating-input-class']
        star = request.form['star']
        Books.add_review(comment, star, b_id)
        return redirect(f'/welcome/buy/{b_id}')
    else:
        return redirect('/')


@app.route('/welcome/buy/<string:b_id>')
def add_to_cart(b_id):
    if session['email'] is not None:
        email = session['email']
        Users.add_book_to_cart(b_id, email)
        return redirect(url_for('buy'))
    else:
        return redirect('/')


@app.route('/welcome/buy/<string:b_id>/add-to-cart')
def add_to_cart_book_specific(b_id):
    if session['email'] is not None:
        email = session['email']
        Users.add_book_to_cart(b_id, email)
        return redirect(f'/welcome/buy/{b_id}')
    else:
        return redirect('/')


@app.route('/welcome/sell', methods=['POST'])
def upload_book():
    if session['email'] is not None:
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
        Books.book_add(title, author, isbn, lang, pages, genre, publisher, price, edition, description, quantity, email)
        return redirect(url_for('booklist'))
    else:
        return redirect('/')


@app.route('/welcome/forum')
def forum():
    if session['email'] is not None:
        posts= Blogs.all_posts()
        total_posts = Database.find_length(collection='forum')
        count1=0
        for i in total_posts:
            count1 = i.count
        return render_template('Forum-Main-Page.html', posts = posts, count=count1)
    else:
        return redirect('/')


@app.route('/welcome/forum', methods=['POST'])
def new_post():
    if session['email'] is not None:
        email = session['email']
        title = request.form['blog-title']
        description = request.form['blog-description']
        Blogs.new_post(title, description, email)
        return redirect('/welcome/forum')
    else:
        return redirect('/')


@app.route('/welcome/forum/<string:blog_id>')
def post_specific(blog_id):
    post = Blogs.one_post(blog_id)
    return render_template('Blog-Specific-Page.html', post=post)


@app.route('/welcome/forum/<string:blog_id>/comment', methods=['POST'])
def post_specific_comment(blog_id):
    if session['email'] is not None:
        email= session['email']
        user= Users.get_by_email(f'u_email= \'{email}\'')
        comment= request.form['text-area']
        Blogs.post_comment(user.u_name, comment, blog_id)
        return redirect(f'/welcome/forum/{blog_id}')
    else:
        return redirect('/')


@app.route('/welcome/sell')
def sell():
    if session['email'] is not None:
        return render_template('Sell-Section.html')
    else:
        return redirect('/')


@app.route('/welcome/sell/booklist')
def booklist():
    if session['email'] is not None:
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        booklist = []
        for i in user.u_booklist:
            book = Books.get_book_by_id(i)
            booklist.append(book)
        return render_template('book-list-of-sellers.html', booklist=booklist)
    else:
        return redirect('/')


@app.route('/users/<string:type>/my-account')
def account(type):
    if session['email'] is not None:
        email = session['email']
        user = Users.get_by_email(f'u_email= \'{email}\'')
        return render_template('My-Account.html', user=user, type=type)
    else:
        return redirect('/')


@app.route('/users/buy/order-history')
def order_history():
    if session['email'] is not None:
        email= session['email']
        user= Users.get_by_email(f'u_email= \'{email}\'')
        orders = []
        for i in user.u_booklist:
            book = Books.get_book_by_id(i)
            orders.append(book)
        return render_template('My-Order-History.html', orders= orders)
    else:
        return redirect('/')


@app.route('/users/buy/my-cart')
def cart():
    if session['email'] is not None:
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
        return redirect('/')


@app.route('/users/<string:type>/my-account', methods=['POST'])
def account_update(type):
    if session['email'] is not None:
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
        return redirect('/')


@app.route('/users/<string:type>/my-account/update-address', methods=['POST'])
def update_address(type):
    if session['email'] is not None:
        street = request.form['street']
        pin = request.form['pin']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        email = session['email']
        Users.update_address(street, pin, city, state, country, email)
        if type == 'sell':
            return redirect('/users/sell/my-account')
        elif type == 'buy':
            return redirect('/users/sell/my-account')
    else:
        return redirect('/')


@app.route('/users/buy/my-cart/update-address', methods=['POST'])
def update_address_via_my_cart():
    if session['email'] is not None:
        street = request.form['street']
        pin = request.form['pin']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        email = session['email']
        Users.update_address(street, pin, city, state, country, email)
        return redirect(url_for("cart"))
    else:
        return redirect('/')


@app.route('/users/buy/my-cart/add-book/<string:b_id>')
def add_same_book_in_cart(b_id):
    if session['email'] is not None:
        email = session['email']
        Users.add_book_quantity(b_id, email)
        return redirect(url_for('cart'))
    else:
        return redirect('/')


@app.route('/users/buy/my-cart/delete-book/<string:b_id>')
def delete_same_book_in_cart(b_id):
    if session['email'] is not None:
        email = session['email']
        Users.delete_book_quantity(b_id, email)
        return redirect(url_for('cart'))
    else:
        return redirect('/')


@app.route('/users/logout')
def logout():
    session['email'] = None
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8000)

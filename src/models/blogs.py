import uuid
from datetime import date, datetime

from flask import session

from src.commom.database import Database
from src.models.users import Users
Database.initialize()


class Blogs:
    def __init__(self, blog_title, blog_description, blog_author, blog_id=None):
        self.blog_title = blog_title
        self.blog_description = blog_description
        self.blog_author = blog_author
        self.blog_id = uuid.uuid4().hex if blog_id is None else blog_id

    @staticmethod
    def new_post( blog_title, blog_description, email):
        user = Users.get_by_email(f'u_email= \'{email}\'')
        date1 = datetime.now().strftime('%b %d,%Y')
        newpost= Blogs(blog_title, blog_description, user.u_name)
        newpost.save_to_db(date1)

    def save_to_db(self, date1):
        Database.insert(collection='forum', data=f"(blog_id, blog_title, blog_description, blog_author, blog_time) "
                                                 f"values('{self.blog_id}','{self.blog_title}',"
                                                 f" '{self.blog_description}','{self.blog_author}','{date1}')")

    @staticmethod
    def all_posts():
        posts= Database.find(collection='forum')
        return posts

    @staticmethod
    def one_post(blogid):
        post = Database.find(collection='forum', query=f"blog_id = \'{blogid}\'")
        return post

    @staticmethod
    def post_comment(name, comment, blogid):
        timestamp= datetime.now()
        commentpost = {timestamp: f'{name},{comment}'}
        Database.update(collection='forum', data=f"blog_comment = blog_comment + {commentpost}",
                        query=f"blog_id=\'{blogid}\'")
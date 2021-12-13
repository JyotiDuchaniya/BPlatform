import os
import uuid,time
from datetime import date, datetime, timezone
from src.application_logging.logger import App_Logger

from src.commom.database import Database
from src.models.users import Users
Database.initialize()

file_path = '../Blogs_logs/Blog_Log.txt'
os.makedirs(os.path.dirname(file_path), exist_ok=True)

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
        App_Logger.log(file_path, " %s: posted by user %s!!" % (blog_title, user.u_name))

    def save_to_db(self, date1):
        try:
            message= 'Saving to database'
            App_Logger.log(file_path, message)
            Database.insert(collection='forum', data=f"(blog_id, blog_title, blog_description, blog_author, blog_time) "
                                                 f"values('{self.blog_id}','{self.blog_title}',"
                                                 f" '{self.blog_description}','{self.blog_author}','{date1}')")
        except Exception as e:
            App_Logger.log(file_path, "error:: %s" % e)

    @staticmethod
    def all_posts():
        posts= Database.find(collection='forum')
        App_Logger.log(file_path, "All posts loaded")
        return posts

    @staticmethod
    def one_post(blogid):
        post = Database.find(collection='forum', query=f"blog_id = \'{blogid}\'")
        App_Logger.log(file_path, "Selected post %s loaded" % post.blog_title)
        return post

    @staticmethod
    def post_comment(name, comment, blogid):
        try:
            t= int(datetime.now(tz=timezone.utc).timestamp() * 1000)
            # timestamp= int(time.mktime(t.timetuple()))
            # print(timestamp)
            commentpost = {t: f'{name}${comment}'}
            Database.update(collection='forum', data=f"blog_comment = blog_comment + {commentpost}",
                            query=f"blog_id=\'{blogid}\'")
            App_Logger.log(file_path, "Comment added by %s at %d" % (name, t))
        except Exception as e:
            App_Logger.log(file_path, "error:: %s" % e)

    @staticmethod
    def comments(blogid):
        blog = Database.find(collection='forum', query=f"blog_id=\'{blogid}\'")
        comments=[]
        if blog.blog_comment is not None:
            for i in sorted(blog.blog_comment):
                x= blog.blog_comment[i].split('$')
                x.append(i.strftime("%b %d,%Y"))
                comments.append(x)
            App_Logger.log(file_path, "Comment loaded for blog: %s" % blog.blog_title)
            return comments
        else:
            App_Logger.log(file_path, "No comments found for blog: %s" % blog.blog_title)
            return None
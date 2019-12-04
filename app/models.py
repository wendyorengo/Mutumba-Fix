from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    post = db.relationship('Post',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password) 
       
    def __repr__(self):
        return f'User {self.username}'

class Post(db.Model):
    '''
    Post class to define Post Objects
    '''
    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key = True)
    post = db.Column(db.String)
    title = db.Column(db.String)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref = 'post',lazy="dynamic")

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    image_path = db.Column(db.String)
    blog_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    username = db.Column(db.String)

    def save_comments(self):
        db.session.add(self)
        db.session.commit()
        

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(post_id=id).all()
        return comments


    @classmethod
    def clear_(cls):
        Comment.all_comments.clear()
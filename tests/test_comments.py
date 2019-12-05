import unittest
from app.models import Comment,Post,User
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_kappaahmed = User(username = "kappaahmed", password = "1234", email="kappaahmed@gmail.com")
        self.new_post = Post(title="code", body = "coding rocks", user_id =self.user_kappaahmed.id )
        self.new_comment = Commentt(title="code", user_id =self.user_kappaahmed.id )

    def tearDown(self):
        Post.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_commentt()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comments(self):

        self.new_comment.save_comment()
        comments = Comment.get_comments()
        self.assertTrue(len(comments)==1)


    



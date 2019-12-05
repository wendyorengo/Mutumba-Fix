import unittest
from app.models import User
from app import db


class UserModelTest(unittest.TestCase):
    '''
    class for testing the behaviour of the User class
    '''
def setUp(self):
    '''
    function for set up method to run before each testcase
    '''
    self.new_user = User(password = 'kingkong')


def test_password_setter(self):
    '''
    test case function to if the password hash works and pass_secure contains a value
    '''
    self.assertTrue(self.new_user.pass_secure is not None)

def test_no_access_password(self):
    '''
    the function test whether the password is unreachable to the user party
    '''
    with self.assertRaises(AttributeError):

def test_password_verification(self):
    '''
    function to test whether the password can be verified
    '''
    self.assertTrue(self.new_user)
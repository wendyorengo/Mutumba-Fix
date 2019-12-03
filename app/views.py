from flask import render_template
from app import app

# Views
@app.route('/login')
def login():

    '''
    View root page function that returns the login and its data
    '''
    return render_template('login.html')

@app.route('/register')
def register():

    '''
    View root page function that returns the register page and its data
    '''
    return render_template('register.html')






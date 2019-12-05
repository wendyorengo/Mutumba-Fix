from flask import render_template,redirect,url_for, abort,request,flash
from . import main
from ..requests import get_quotes

from .forms import CommentsForm ,UpdateProfile, PostForm
from ..models import User,Post, Comment
from flask_login import login_required, current_user
# from .. import db, photos
# import markdown2
# from ..email import mail_message


   

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to Mitumba Fix Application'

    
    posts= Post.get_all_posts() 
    quotes = get_quotes() 

    return render_template('index.html', title = title, quotes = quotes, posts=posts)

@main.route('/about')
def about():
    '''
    View root page function that returns the about page and its data
    '''
    title = 'Welcome to Mitumba Fix Application'
    return render_template('about.html', title=title)

@main.route('/contact')
def contact():
    '''
    View root page function that returns the contact page and its data
    '''
    title = ''
    return render_template('contacts.html', title = title)

@main.route('/all')
def all():
    '''
    View profile page that returns all the profiles of the users"
    '''
    title = 'Welcome to Mitumba Fix Application'

    
    profile= Post.get_all_profiles() 
    

    return render_template('profile.html', title = title, profiles=profiles)



@main.route('/post')
def post():

    '''
    View post page function that returns the post details page and its data
    '''
    found_post= Post.query.get(post_id)
    title = post_id
    post_comments = Comment.get_comments(post_id)

    return render_template('post.html',title= title ,found_post= found_post, post_comments= post_comments)


@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        post.title.data = post.title
        post.content.data = post.content
    return render_template('post.html', title='Update Post', form=form)

@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.post'))



@main.route('/post/new/', methods = ['GET','POST'])
@login_required
def new_post():
    '''
    Function that creates new posts
    '''
    form = PostForm()


    if form.validate_on_submit():
        post = Post(title=form.title.data,post=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post'))

    return render_template('new_post.html', new_post_form= form)

@main.route('/blog/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    if form.validate_on_submit():
        new_comment = Comment(blog_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comments()
        return redirect(url_for('main.all'))
    
    return render_template('new_comment.html',comment_form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)

@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returns  the comments belonging to a particular blog
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comment.html',comments = comments, id=id)




from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import User
from .forms import  LoginForm,RegistrationForm
from .. import db
from ..email import mail_message


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')
    title = "login"
    return render_template('auth/login.html',login_form = login_form, title = title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
    
@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password =form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Mutumba Fix","email/welcome_user", user.email,user=user)
        
        return redirect(url_for('auth.login'))
    title = "Register Now"
    return render_template('auth/register.html',title=title, registration_form =form)

    


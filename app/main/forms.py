from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, RadioField,SelectField
from wtforms.validators import Required

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('SUBMIT')

class PostForm(FlaskForm):
    title = TextAreaField ('Name of Item')
    content = TextAreaField('Describe your item', validators=[Required()])
    submit = SubmitField('Submit') 

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Explain your dealings.',validators = [Required()])
    submit = SubmitField('Submit')




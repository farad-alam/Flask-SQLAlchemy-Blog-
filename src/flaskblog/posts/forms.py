from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=10,max=300)])
    content = TextAreaField('Content', validators=[DataRequired()])
    thumbnail = FileField("Post Thumbnail", validators=[FileAllowed(['jpg','png'])])
    publish_post = SubmitField('Publish Post')
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_ckeditor import CKEditorField
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=10,max=300)])
    content = CKEditorField('Content', validators=[DataRequired()])
    thumbnail = FileField("Post Thumbnail", validators=[FileAllowed(['jpg','png'])])
    publish_post = SubmitField('Publish Post')
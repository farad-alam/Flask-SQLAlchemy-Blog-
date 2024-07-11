from flask_ckeditor import CKEditorField
from flask_admin.contrib.sqla import ModelView
from flaskblog import admin, db
from .models import Post

class PostModelView(ModelView):
    column_list = ('id', 'title', 'content', 'thumbnail', 'user', 'created_at')
    form_columns = ('title', 'content', 'thumbnail')
    form_overrides = {
        'content': CKEditorField
    }

admin.add_view(PostModelView(Post, db.session))
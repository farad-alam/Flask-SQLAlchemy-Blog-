from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flaskblog import admin, db
from .models import User
from flask import flash


# class UserModelView(ModelView):
#     def on_model_change(self, form, model, is_created):
#         # Check if the password field has been modified
#         if form.password.data and form.password.data != model.password:
#             model.password = generate_password_hash(form.password.data)



class UserModelView(ModelView):
    def create_model(self, form):
        try:
            model = self.model(
                username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            flash('Failed to create record. %s' % str(ex), 'error')
            return False
        else:
            self.after_model_change(form, model, True)
        return model

# Add the custom model view to the admin
admin.add_view(UserModelView(User, db.session))
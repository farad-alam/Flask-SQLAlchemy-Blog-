from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = '7741226d315a481bbf828d655f58afa3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "user_bp.user_login"
login_manager.login_message_category = 'info'



from flaskblog.main.routes import main_bp
from flaskblog.users.routes import user_bp
from flaskblog.posts.routes import posts_bp

app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(posts_bp)
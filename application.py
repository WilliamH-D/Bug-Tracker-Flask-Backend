from flask import Flask
from database.models import db
from blueprints.projects import bp as projects_bp
from blueprints.bugs import bp as bugs_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.register_blueprint(projects_bp)
app.register_blueprint(bugs_bp)

db.init_app(app)


@app.route('/')
def index():
    return "Bug Tracker API root"

import os
from flask import Flask
from config import *
from database import db
from models import *
import workers
from flask_restful import Resource, Api
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from flask_login import LoginManager, login_manager
from flask_sse import sse
from flask_caching import Cache
app = None
celery=None
api=None
cache=None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no Production config is setup")
    else:
        #print("Starting local dev")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    #login_manager= LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    db.create_all()
    api = Api(app)
    app.app_context().push()
    celery= workers.celery
        # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    cache = Cache(app)
    app.app_context().push()
    return app, celery, api, cache

app, celery, api, cache = create_app()
#api = Api(app)
## Routes
from controllers import *

## APIs
from api import *

api.add_resource(User_decks, "/api/<int:user_id>")
api.add_resource(Deck, "/api/<int:user_id>/<int:deck_id>")
api.add_resource(Cards, "/api/<int:user_id>/<int:deck_id>/<int:card_id>")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
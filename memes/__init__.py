from flask import Flask
from db import mongo
from flask_cors import CORS
import vk_api
import os



def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.from_pyfile("config.py")
    mongo.init_app(app)
    CORS(app)

    from .routes import routes as auth_blueprint
    app.register_blueprint(auth_blueprint)

    session = vk_api.VkApi(login=os.getenv('LOGIN'), password=os.getenv('PASSWORD'))
    session.auth()
    access_token = session.token['access_token']
    group = '-197700721'

    albums_ids = ['284717200', '281940823', '283939598', '274262016']

    vk = session.get_api()
    memes = []

    for i in range(4):
        memes.append(vk.photos.get(album_id=albums_ids[i],
                                   owner_id=group,
                                   extended=1,
                                   access_token=access_token))


    return app
from flask import Flask
from db import mongo
from flask_cors import CORS
import vk as vka


def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.from_pyfile("config.py")
    mongo.init_app(app)
    CORS(app)
    db = mongo.db

    memes = [mem for mem in db.memes.find()]

    if len(memes) == 1:
        session = vka.Session(access_token='hehehhehehehehehehehhehehehehehe')
        vk_api = vka.API(session)
        group = '-197700721'

        albums_ids = ['274262016']

        memms = []
        memms.append(vk_api.photos.get(album_id=albums_ids[0],
                                       owner_id=group,
                                       extended=1,
                                       count=287,
                                       rev=1,
                                       v=5.131))

        # дополнительный запрос на смешных котяточек
        group_1 = '-208870661'
        kittens = vk_api.photos.get(album_id='wall',
                                    owner_id=group_1,
                                    extended=1,
                                    rev=1,
                                    count=600,
                                    v=5.131)
        print(len(kittens['items']))

        memms.append(kittens)

        for mems in memms:
            for mem in mems['items']:
                memes.append({
                    '_id': mem['id'],
                    'album_id': mem['album_id'],
                    'user_id': mem['user_id'],
                    'owner_id': mem['owner_id'],
                    'text': mem['text'],
                    'url': mem['sizes'][1]['url'],
                    'likes_count': mem['likes']['count'],
                    'date': mem['date'],
                    'inside_likes': 1,
                    'is_fav': 0
                })

                db.memes.insert_one({
                    '_id': mem['id'],
                    'album_id': mem['album_id'],
                    'user_id': mem['user_id'],
                    'owner_id': mem['owner_id'],
                    'text': mem['text'],
                    'url': mem['sizes'][1]['url'],
                    'likes_count': mem['likes']['count'],
                    'date': int(mem['date']),
                    'inside_likes': 1,
                    'is_fav': 0
                })




    from .routes import routes as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

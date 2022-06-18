from flask import Blueprint, jsonify, request, session, redirect, url_for
from db import mongo
import json

routes = Blueprint('routes', __name__)
db = mongo.db


def find_all():
    memes_find = db.memes.find({'_id': {'$ne': 0}})
    memes = [mem for mem in memes_find]
    return memes


memes = [meme for meme in find_all()]
memes.sort(key=lambda x: x['date'])


@routes.route('/get_all_memes', methods=['GET'])
def get_all_memes_for_date():
    memes.sort(key=lambda x: x['date'])
    filter_meme = []
    for meme in memes:
        mem = {
            '_id': meme['_id'],
            'user_id': meme['user_id'],
            'likes_count': meme['likes_count'],
            'url': meme['url']
        }
        filter_meme.append(mem)
    return json.dumps({'memes': filter_meme})


@routes.route('/get_memes',  methods=['POST'])
def compare_meme():
    is_doing = int(request.args.get('is_doing'))
    meme_id = int(request.args.get('_id'))

    memes_find = db.memes.find({'_id': int(meme_id)})
    memes = [mem for mem in memes_find]
    curr = memes[0]

    if int(is_doing) == 0:
        curr['inside_likes'] *= 0.7
    else:
        curr['inside_likes'] *= 1.1

    db.memes.update_one({'_id': int(meme_id)}, {"$set": {'inside_likes': curr['inside_likes']}})
    return json.dumps({'': [{'id': meme_id},
                            {'is_doing': is_doing},
                            {'curr': curr}]})


@routes.route('/get_range_memes',  methods=['POST'])
def range_meme():
    fav_meme_id = int(request.args.get('_id'))

    memes_find = db.memes.find({'_id': fav_meme_id})
    memes_for_fav = [mem for mem in memes_find]
    curr = memes_for_fav[0]
    memes.sort(key=lambda x: x['inside_likes'])

    for i in range(1, len(memes), 7):

        curr['inside_likes'] *= 1.1
        memes.append(curr)

    return json.dumps({'memes with fav': memes})



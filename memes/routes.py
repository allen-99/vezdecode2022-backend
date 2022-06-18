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
    print(memes_find)
    memes = [mem for mem in memes_find]
    print(memes)
    curr = memes[0]

    if int(is_doing) == 0:
        curr['inside_likes'] *= 0.7
    else:
        curr['inside_likes'] *= 1.1

    db.memes.update_one({'_id': int(meme_id)}, {"$set": {'inside_likes': curr['inside_likes']}})
    return json.dumps({'': [{'id': meme_id},
                            {'is_doing': is_doing},
                            {'curr': curr}]})




# @routes.route('/get_all_meme_order_by', methods=["POST", "GET"])
# def get_all_meme_order_by():
#     memes_find = []
#     try:
#         memes_find = find_all()
#     finally:
#         if len(memes_find) != 0:
#             memes_find.sort(key=lambda x: x['date'])
#             curr = memes_find[0]
#             data = json.dumps({'memes': memes_find})
#             return redirect(url_for('routes.get_rating_meme', curr_meme=curr))
#         else:
#             return redirect(url_for('routes.get_rating_meme_end'))
#
#
# @routes.route('/get_rating_meme/<curr_meme>', methods=["POST", "GET"])
# def get_rating_meme(curr_meme):
#     data = request.args.get('data')
#     curr = curr_meme
#     memes = data['memes']
#     if request.method == 'GET':
#         return json.dumps({'message': 'choose like or skip'})
#     if request.method == 'POST':
#         doing = request.args.get('doing')
#         if doing == 'like':
#             like(curr)
#         if doing == 'skip':
#             skip(curr)
#     index = memes.index(curr)+1
#     if len(memes) < index:
#         curr = memes[index]
#         return redirect(url_for('/get_rating_meme', data=memes, curr_meme=curr))
#     else:
#         return redirect(url_for('/get_rating_meme_end'))

#
# @routes.route('/choose_fav_mem', methods=["POST", "GET"])
# def choose_mem():
#     fav_mem = find_with_id(request.args.get('_id'))
#     prev_fav_mem_find = db.memes.find_one({'is_fav': 1})
#     try:
#         prev_fav_mem = [mem for mem in prev_fav_mem_find]
#         db.memes.update_one({'_id': prev_fav_mem[0]}, {"$set": {'is_fav': 0}})
#     finally:
#         fav_mem[0]['is_fav'] = 1
#         print(fav_mem)
#         db.memes.update_one({'_id': fav_mem[0]['_id']}, {"$set": {'likes_count': fav_mem[0]['likes_count']}})
#         return json.dumps({'mems': fav_mem[0]})
#
#
# @routes.route('/get_all_memes_fav', methods=["GET"])
# def get_memes_for_fav():
#     memes_find = db.memes.find({'_id': {'$ne': 0}})  #общее число
#     memes = [mem for mem in memes_find]
#     try:
#         fav_mem_find = db.memes.find_one({'is_fav': 1})
#         fav_mem = [mem for mem in fav_mem_find]
#         memes.sort(key=lambda x: x['likes_count'])
#         for i in range(6, len(memes_find), len(memes_find)//7):
#             memes.append(fav_mem[0])
#     finally:
#         return json.dumps({'mems': memes})

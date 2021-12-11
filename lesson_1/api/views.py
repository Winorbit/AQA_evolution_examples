from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker

import json

from models import engine, Post, User, DeclarativeBase
from settings import logger
from validation import check_email

DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
app = Flask(__name__)


@app.route("/users", methods = ["post"])
def create_new_user():
    content = request.get_json()
    
    email = content.get('email')
    
    if not check_email(email):
        message = f"User creation failed - invalid emai {email}"
        logger.error(message)
        return jsonify({"error_message": message}), 400

    username = content.get('username') 
    password = content.get('password')

    if username and password:
        try:
            new_user = User(**content)
            db_session = Session()
            db_session.add(new_user)
            db_session.commit()
            message = f"New user {username} created."
            logger.info(message)
            return jsonify({}), 201
        except Exception as e:
            message = f"User with params {content} not loaded with exception: {e}"
            logger.error(message)
            return jsonify({"error_message": message}), 400
    else:
        message = f"User creation failed - wrong input data {content}"
        logger.error(message)
        return jsonify({"error_message": message}), 400



@app.route("/users", methods = ["get"])
def get_users():
    try:
        db_session = Session()
        users_query = db_session.query(User).all()
        users = [user.serialize for user in users_query]
        res = jsonify(users)
        return res, 200

    except Exception as e:
        message = f"Something went wrong in loading users: {e}"
        logger.error(message)
        res = jsonify({"error_message": message})
        return res, 400


@app.route("/users/<user_id>", methods = ["get"])
def get_user_by_id(user_id): 
    try:
        db_session = Session()
        user = db_session.query(User).filter(User.id == user_id).first()
        if user:
            res = jsonify(user.serialize)
            return res, 200
        else:
            res = {"error_message": f"User with id {user_id} not found"}
            return jsonify(res), 400
    except Exception as e:
        message = f"Something went wrong in loading user {user_id} because : {e}"
        logger.error(message)
        return jsonify({"error_message":message}), 400


@app.route("/users/<user_id>", methods = ["put"])
def update_user(user_id):
    content = request.get_json()

    try:
        db_session = Session()
        new_user = db_session.query(User).filter(User.id == user_id).first()
        
        for key, value in content.items():
            setattr(new_user, key, value)
        
        db_session.add(new_user)
        db_session.commit()    

        return jsonify(new_user.serialize), 201
    except Exception as e:
        message = f"Update failed with exception: {e}"
        logger.error(message)
        return jsonify({"error_message": message}), 400


@app.route("/posts", methods = ["post"])
def create_post():
    content = request.get_json()
    
    title = content.get('title') 
    text = content.get('text') 
    author_id = int(content.get('author_id'))

    if title and text and author_id:
        try:
            new_post = Post(text=text, title=title, author_id=author_id)
            db_session = Session()
            db_session.add(new_post)
            db_session.commit()
            message = f"New post {new_post.serialize} created."
            logger.info(message)
            res = jsonify(new_post.serialize)
            print(res)
            return res, 201
        except Exception as e:
            message = f"Post {content} not created with exception: {e}"
            logger.error(message)
            return jsonify({"error_message": message}), 400
    else:
        return jsonify({"error_message": f"wrong input data: {content}"}), 400


@app.route("/posts", methods = ["get"])
def get_posts():
    try:
        db_session = Session()
        posts_query = db_session.query(Post).all()
        posts = [post.serialize for post in posts_query]
        res = jsonify(posts)
        return res, 200
    except Exception as e:
        message = f"Something went wrong in loading posts: {e}"
        return jsonify({"error_message":message}), 400


@app.route("/posts/<post_id>", methods = ["get"])
def get_post_by_id(post_id): 
    try:
        db_session = Session()
        post = db_session.query(Post).filter(Post.id == post_id).first()
        if post:
            res = jsonify(post.serialize)
            return res, 200
        else:
            res = {"error_message": f"Post with id {post_id} not found"}
            return jsonify(res),400
    except Exception as e:
        message = f"Something went wrong in loading post {post_id}: {e}"
        logger.error(message)
        return jsonify({"error_message": message}), 400


@app.route("/posts/<post_id>", methods = ["put"])
def update_post(post_id):
    content = request.get_json()
    try:
        db_session = Session()
        new_post = db_session.query(Post).filter(Post.id == post_id).first()
        
        for key, value in content.items():
            setattr(new_post, key, value)
        
        db_session.add(new_post)
        db_session.commit()    
        
        return jsonify(new_post.serialize), 201
    except Exception as e:
        message = f"Update failed with exception: {e}"
        logger.error(message)
        return jsonify({"error_message": message}), 400

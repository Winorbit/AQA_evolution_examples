import json
import sys

from flask import Flask, request, jsonify
from flask_restx import Resource, Api, fields
from sqlalchemy.orm import sessionmaker

called_from = sys.modules['__main__'].__file__
if "unittest" in called_from or "pytest" in called_from:
    from .models import engine, Post, User, DeclarativeBase
    from .settings import logger
    from .validation import check_email
else:
    from models import engine, Post, User, DeclarativeBase
    from settings import logger
    from validation import check_email

DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
app = Flask(__name__)
api = Api(app, 
          version='1.0', 
          title='Sample API',
          description='A sample API',)

user_payload = api.model('User', {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,})

post_payload = api.model('Post', {
    'title': fields.String,
    'text': fields.String,
    'author_id': fields.Integer,})

@api.route('/users')
class Users(Resource):
    @api.expect(user_payload)
    def post(self):
        content = request.get_json()
        email = content.get('email')
        
        if not email:
            message = f"User creation failed - body without email {content}"
            logger.error(message)
            res = {"error_message": message}
            return res, 400

        if not check_email(email):
            message = f"User creation failed - invalid emai {email}"
            logger.error(message)
            res = {"error_message": message}
            return res, 400

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
                return new_user.serialize, 201
            except Exception as e:
                message = f"User with params {content} not loaded with exception: {e}"
                logger.error(message)
                res = {"error_message": message}
                return res, 400
        else:
            message = f"User creation failed - wrong input data {content}"
            logger.error(message)
            res = {"error_message": message}
            return res, 400

    def get(self):
        try:
            db_session = Session()
            users_query = db_session.query(User).all()
            users = [user.serialize for user in users_query]
            return users, 200

        except Exception as e:
            message = f"Something went wrong in loading users: {e}"
            logger.error(message)
            res = {"error_message": message}
            return res, 400



@api.route("/users/<int:user_id>")
class SingleUser(Resource):
    def get(self, user_id): 
        try:
            db_session = Session()
            user = db_session.query(User).filter(User.id == user_id).first()
            if user:
                return user.serialize, 200
            else:
                res = {"error_message": f"User with id {user_id} not found"}
                return res, 400
        except Exception as e:
            message = f"Something went wrong in loading user {user_id} because : {e}"
            logger.error(message)
            res = {"error_message": message}
            return res, 400

    @api.expect(user_payload)
    def put(self, user_id):
        content = request.get_json()
        email = content.get('email')
        
        if email:
            if not check_email(email):
                message = f"User update failed - invalid emai {email}"
                logger.error(message)
                res = {"error_message": message}
                return res, 422
        try:
            db_session = Session()
            new_user = db_session.query(User).filter(User.id == user_id).first()
            
            for key, value in content.items():
                setattr(new_user, key, value)
            
            db_session.add(new_user)
            db_session.commit()    

            return new_user.serialize, 201
        except Exception as e:
            message = f"Update failed with exception: {e}"
            logger.error(message)
            res = {"error_message": message}
            return res, 400


@api.route('/posts')
class Users(Resource):
    @api.expect(post_payload)
    def post(self):
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
                return new_post.serialize, 201
            except Exception as e:
                message = f"Post {content} not created with exception: {e}"
                logger.error(message)
                res = {"error_message": message}
                return res, 400
        else:
            res = {"error_message": f"wrong input data: {content}"}
            return res, 400

    def get(self):
        try:
            db_session = Session()
            posts_query = db_session.query(Post).all()
            posts = [post.serialize for post in posts_query]
            return posts, 200
        except Exception as e:
            message = f"Something went wrong in loading posts: {e}"
            res = {"error_message":message}
            return res, 400


@api.route("/posts/<int:post_id>")
class SinglePost(Resource):
    def get(self, post_id): 
        try:
            db_session = Session()
            post = db_session.query(Post).filter(Post.id == post_id).first()
            if post:
                return post.serialize, 200
            else:
                res = {"error_message": f"Post with id {post_id} not found"}
                return jsonify(res),400
        except Exception as e:
            message = f"Something went wrong in loading post {post_id}: {e}"
            logger.error(message)
            return {"error_message": message}, 400

    @api.expect(post_payload)
    def put(self, post_id):
        content = request.get_json()
        try:
            db_session = Session()
            new_post = db_session.query(Post).filter(Post.id == post_id).first()
            
            for key, value in content.items():
                setattr(new_post, key, value)
            
            db_session.add(new_post)
            db_session.commit()    
            
            return new_post.serialize, 201
        except Exception as e:
            message = f"Update failed with exception: {e}"
            logger.error(message)
            return {"error_message": message}, 400
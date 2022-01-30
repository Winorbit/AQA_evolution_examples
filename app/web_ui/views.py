from flask import Flask, request, render_template, redirect, session, url_for
import requests
from settings import ROOT_URL, API_URL, OK_CODES

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/posts")
def posts():
    url = f"{API_URL}/posts"
    try:
        res = requests.get(url)
        if res.status_code in OK_CODES:
            posts = res.json()
            return render_template('posts/posts.html', posts=posts)
    except Exception as e:
        error_message = f"Something went wrong in loading posts: {e}"
        return render_template('error_page.html',error_message=error_message)


@app.route("/posts/<post_id>")
def post(post_id): 
    url = f"{API_URL}/posts/{post_id}"
    try:
        res = requests.get(url)
        if res.status_code in OK_CODES:
            post = res.json()
            return render_template('posts/post.html', post=post)
    except Exception as e:
        error_message = f"Something went wrong in loading post {post_id}"
        log_message = f"{error_message}: {e}"
        logger.error(log_message)
        return render_template('error_page.html',error_message=error_message)


@app.route("/signup", methods = ["get", "post"])
def signup():
    if request.method == 'POST':
        url = f"{API_URL}/users"
        try:
            res = requests.post(url, json={**request.form})
            if res.status_code in OK_CODES:
                return redirect(url_for("login"))
        except Exception as e:
            error_message = f"User with params {dict(request.form)} not loaded"
            return render_template('error_page.html',error_message=error_message)
    else:
        return render_template('user/signup.html')


@app.route("/login", methods = ["get", "post"])
def login():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')
        email = request.form.get('email')
        if username and password and email:
            try:
                url = f"{API_URL}/users/user_by_name/{username}"
                res = requests.get(url)
                if res.status_code in OK_CODES:
                    session['username'] = username
                    session["user_id"] = res.json().get("id")
                    return redirect(url_for('my_cabinet'))
                else:
                    message = "Проверьте правильность введенных данных."
                    return render_template('user/login.html', message=message)
            except Exception as e:
                raise Exception(f"Something wrong with login user {dict(request.form)}: {e}")
    else:
        message = "Введите данные для того, чтобы войти в личный кабинет."
        return render_template('user/login.html', message=message)


@app.route("/logout", methods = ["post"])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/cabinet", methods = ["get", "post"])
def my_cabinet():
    username = session.get("username")
    user_id = session.get("user_id")
    if username and user_id:
        if request.method == 'POST':
            title = request.form.get('title') 
            text = request.form.get('post_text')
            if title and text:
                try:
                    create_post_url = f"{API_URL}/posts/create_post"
                    res = requests.post(create_post_url, json={"title":title,
                                                                "text":text,
                                                                "author": user_id})
                    if res.status_code in OK_CODES:
                        post_id = res.json().get("id")
                        new_post_url = f""
                        return redirect(f"{ROOT_URL}/posts/{post_id}", code=302)
                    else:
                        error_message = "Что-то пошло не так, попробуйте еще перезайти в кабинет."
                        return render_template('error_page.html',error_message=error_message)
                except Exception as e:
                    return render_template('error_page.html',error_message=e)
        else:
            return render_template('user/cabinet.html')
    else:
        return redirect(url_for("login"))




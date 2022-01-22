from views import app
from settings import APP_SECRET_KEY, HOST

if __name__ == "__main__":
	app.config['SECRET_KEY'] = APP_SECRET_KEY
	app.run(debug=True, host=HOST)
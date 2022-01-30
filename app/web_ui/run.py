from views import app
from settings import APP_SECRET_KEY

if __name__ == "__main__":
	app.config['SECRET_KEY'] = APP_SECRET_KEY
	app.run(debug=True, host='0.0.0.0', port=5001)
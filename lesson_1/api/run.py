from views import app

if __name__ == "__main__":
	app.config['SECRET_KEY'] = "Your_secret_string"
	app.run(debug=True,host='0.0.0.0')
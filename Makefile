Makefile: ;

run:
	FLASK_ENV=development FLASK_APP=./src/handlers/app.py flask run
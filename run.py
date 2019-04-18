# run.py
# This simply launches our app server

from flask import Flask

from app import app

if __name__ == '__main__':
	app.run()
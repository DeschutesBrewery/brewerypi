import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
	BOOTSTRAP_SERVE_LOCAL = False if os.environ.get("BOOTSTRAP_SERVE_LOCAL") == "0" else True
	EXPORT_DATABASE_FILENAME = "BreweryPi.sql"
	EXPORT_ELEMENT_ATTRIBUTES_FILENAME = "elementsAttributes.csv"
	EXPORT_EVENT_FRAME_ATTRIBUTES_FILENAME = "eventFrameAttributes.csv"
	EXPORT_FOLDER = "exports"
	EXPORT_TAGS_FILENAME = "tags.csv"
	IMPORT_DATABASE_FILENAME = "BreweryPi.sql"
	IMPORT_ELEMENT_ATTRIBUTES_FILENAME = "elementAttributes.csv"
	IMPORT_EVENT_FRAME_ATTRIBUTES_FILENAME = "eventFrameAttributes.csv"
	IMPORT_FOLDER = "imports"
	IMPORT_TAGS_FILENAME = "tags.csv"
	IS_AWS = True if os.environ.get("IS_AWS") == "1" else False
	IS_RASPBERRY_PI = True if os.environ.get("IS_RASPBERRY_PI") == "1" else False
	LOCAL_TIMEZONE = os.environ.get("LOCAL_TIMEZONE")
	MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "BreweryPi"
	MYSQL_HOST = os.environ.get("MYSQL_HOST") or "localhost"
	MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "brewery"
	MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "pi"
	NOTIFICATIONS_INTERVAL_IN_MILLISECONDS = os.environ.get("NOTIFICATIONS_INTERVAL") or 10000
	SECRET_KEY = os.environ.get("SECRET_KEY") or "Replace with a hard to guess string."
	SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
	SQLALCHEMY_SERVER_URI = f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

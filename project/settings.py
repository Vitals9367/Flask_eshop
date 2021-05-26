import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse

class Config:
    SECRET_KEY = 'uuu so secret'

    SQLALCHEMY_DATABASE_URI = "idk"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    WHOOSHEE_MIN_STRING_LEN = 3
    WHOOSHEE_WRITER_TIMEOUT = 3

    FLASK_ADMIN_SWATCH = 'cerulean'

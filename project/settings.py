import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse

class Config:
    SECRET_KEY = '6f137bcbe4bff73bc8f6f4c59a3c5029'

    SQLALCHEMY_DATABASE_URI = "postgres://ejgwszmtjbkudt:3f0e8fb8919e2d1237698be4caa2196fcdf52d380381701ac474767b6eb1d225@ec2-63-34-97-163.eu-west-1.compute.amazonaws.com:5432/d61ae8b2jon7st"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    WHOOSHEE_MIN_STRING_LEN = 3
    WHOOSHEE_WRITER_TIMEOUT = 3

    FLASK_ADMIN_SWATCH = 'cerulean'

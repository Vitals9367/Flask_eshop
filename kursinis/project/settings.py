import os
import urllib.parse

params = urllib.parse.quote_plus(
    "DRIVER={SQL Server};SERVER=xamdb.database.windows.net;DATABASE=XamarinDB;UID=vitalijusal9367;PWD=mariukas1A.")


class Config:
    SECRET_KEY = '6f137bcbe4bff73bc8f6f4c59a3c5029'
    FLASK_ENV = 'development'

    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    WHOOSHEE_MIN_STRING_LEN = 3
    WHOOSHEE_WRITER_TIMEOUT = 3

    FLASK_ADMIN_SWATCH = 'cerulean'

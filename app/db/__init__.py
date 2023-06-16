import os

from app.db.connection import DBConnection

database = DBConnection(os.path.join('.', 'data', 'botdata.db'))

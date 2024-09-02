# myapp/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

engine = create_engine('postgresql://darshan:1234@localhost:5432/my_db')


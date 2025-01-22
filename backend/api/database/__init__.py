"""Create SQLAlchemy engine and session objects."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

conn_string = 'postgresql+psycopg2://postgres:rootpassword@localdb/ITP4606'
engine = create_engine(conn_string)
session = Session(engine)
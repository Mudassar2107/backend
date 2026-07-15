from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. The Connection String (The exact coordinates to your database)
SQLACLCHEMY__URL = "postgresql://mudassar:postgres@localhost:5432/todo_db"

#2. The Engine (The actual connection cable)
engine = create_engine(SQLACLCHEMY__URL)

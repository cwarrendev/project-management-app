from sqlmodel import SQLModel
from app.database import engine

def rebuild_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    rebuild_db()

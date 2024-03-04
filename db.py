from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base
default_db_url = 'sqlite:////Users/endyb.dev/Developer/codev/ai-db-manager/db.sqlite3'
# engine = create_engine(default_db_url, echo=True)
# Base.metadata.create_all(engine)


class DB:
    def __init__(self, db_url: str = default_db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=True)
        self.session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )

    def create_database(self):
        Base.metadata.create_all(self.engine)
    
    def session(self):
        db_session = self.session_factory()
        try:
            yield db_session()
        except Exception as e:
            print(f"Rolling back, because of exception: {e}")
        finally:
            db_session.close()

db = DB()

db.create_database()
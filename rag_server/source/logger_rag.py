import os
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RagLogger():
    def __init__(self):
        self._session = SessionLocal()
        self.record = RagLog()

    def commit(self):
        try:
            self._session.add(self.record)
            self._session.commit()
        except Exception as ex:
            self._session.rollback()
            raise ex
        finally:
            self._session.close()

class RagLog(Base):
    __tablename__ = 'rag_logs' 
    UserInput = Column(Text)
    SubqueriesRequest = Column(Text)
    SubqueriesResponse = Column(Text)
    EmbeddingsUnique = Column(Text)
    EmbeddingsScored = Column(Text)
    EmbeddingsTop = Column(Text)
    MainRequest = Column(Text)
    MainResponse = Column(Text)
    Id = Column(Integer, primary_key=True)
    CreatedDate = Column(DateTime)
    LastModifiedDate = Column(DateTime)
    IsSuccess = Column(Boolean)
    ErrorMessage = Column(Text)

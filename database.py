from sqlalchemy import  create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL= "sqlite:///./expenses.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

sessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


class DBExpense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    activity = Column(String, index=True)
    cost = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)
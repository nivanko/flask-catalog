from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    """docstring for """
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(25), nullable = False)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    description = Column(String(250))
    picture = Column(String(50))
    creator = Column(String(50), nullable = False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


# Create DB schema
engine = create_engine('postgresql:///catalog')
Base.metadata.create_all(bind=engine)

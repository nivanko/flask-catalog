from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    # table name set to 'users' to avoid confict with postgres function 'user'
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(250), nullable = False, unique = True)
    fullname = Column(String(250), nullable = False)


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
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)


# Create DB schema
engine = create_engine('postgresql:///catalog')
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Fill DB with sample data
    category1 = Category(name = "Backpacks")
    session.add(category1)
    category2 = Category(name = "Tents")
    session.add(category2)
    category3 = Category(name = "Camp Bedding")
    session.add(category3)
    category4 = Category(name = "Camp Kitchen")
    session.add(category4)
    category5 = Category(name = "Water")
    session.add(category5)
    category6 = Category(name = "Lighting")
    session.add(category6)
    category7 = Category(name = "Electronics")
    session.add(category7)
    category8 = Category(name = "Gadgets")
    session.add(category8)
    category9 = Category(name = "Gear")
    session.add(category9)
    category10 = Category(name = "Health")
    session.add(category10)
    category11 = Category(name = "Safety")
    session.add(category11)

    user1 = User(username = "nivanko", fullname = "Nikolay Ivanko")
    session.add(user1)

    user1 = session.query(User).filter_by(username = "nivanko").one()

    item1 = Item(name = "Hiking Packs", category_id = 1, user_id = user1.id)
    session.add(item1)
    item2 = Item(name = "Day Packs", category_id = 1, picture = "daypack.jpg",
                description = ("A daypack is a smaller, frameless backpack "
                "that can hold enough contents for a day hike, or a day's "
                "worth of other activities."),
                user_id = user1.id)
    session.add(item2)

    session.commit()

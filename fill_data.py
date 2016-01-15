from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from setup import Base, Category, Item

# Use PostgreSQL database, local connection
engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

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

session.commit()

# item = Item(name = "", category_id = )
item1 = Item(name = "Hiking Packs", category_id = 1, creator = "nikolay.i@didww.com")
session.add(item1)
item2 = Item(name = "Day Packs", category_id = 1, picture = "daypack.jpg", description = "A daypack is a smaller, frameless backpack that can hold enough contents for a day hike, or a day's worth of other activities.", creator = "nikolay.i@didww.com")
session.add(item2)

session.commit()

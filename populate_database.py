from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import CatalogCategory, CatalogItem, Base
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#foo
category1 = CatalogCategory(name = "Foo")
session.add(category1)
session.commit()

item1 = CatalogItem(name = "FooA", description = "description for fooA", catalog_category = category1)
session.add(item1)
session.commit()

item2 = CatalogItem(name = "FooB", description = "description for fooB", catalog_category = category1)
session.add(item2)
session.commit()

item3 = CatalogItem(name = "FooC", description = "description for fooC", catalog_category = category1)
session.add(item3)
session.commit()

#bar
category2 = CatalogCategory(name = "Bar")
session.add(category2)
session.commit()

item1 = CatalogItem(name = "BarA", description = "description for barA", catalog_category = category2)
session.add(item1)
session.commit()

item2 = CatalogItem(name = "BarB", description = "description for barB", catalog_category = category2)
session.add(item2)
session.commit()

item3 = CatalogItem(name = "BarC", description = "description for barC", catalog_category = category2)
session.add(item3)
session.commit()

#bar
category3 = CatalogCategory(name = "Baz")
session.add(category3)
session.commit()

item1 = CatalogItem(name = "BazA", description = "description for bazA", catalog_category = category3)
session.add(item1)
session.commit()

item2 = CatalogItem(name = "BazB", description = "description for bazB", catalog_category = category3)
session.add(item2)
session.commit()

item3 = CatalogItem(name = "BazC", description = "description for bazC", catalog_category = category3)
session.add(item3)
session.commit()

print "added catalog items!"


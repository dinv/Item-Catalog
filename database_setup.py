from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    picture = Column(String(80), nullable = False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'    : self.name,
           'email'   : self.email,
           'picture' : self.picture,
       }

class CatalogCategory(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    items = relationship("CatalogItem", cascade="all, delete-orphan")

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class CatalogItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    catalog_category_id = Column(Integer,ForeignKey('category.id'))
    catalog_category = relationship(CatalogCategory)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
       }

engine = create_engine('sqlite:///catalog.db')
 
Base.metadata.create_all(engine)

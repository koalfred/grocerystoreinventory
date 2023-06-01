# This is where I learned to remove the dollar sign ($) from the prices when cleaning up the data: https://builtin.com/software-engineering-perspectives/python-remove-character-from-string

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brands(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price', Integer)
    date_updated = Column('Date Updated', Date)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
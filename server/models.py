from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    purchase = relationship("Purchase", back_populates="user")
    review = relationship("Review", back_populates="user")
    wishlist = relationship("Wishlist", back_populates="user")
    cart = relationship("Cart", back_populates="user")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    discount = Column(Float)
    short_description = Column(String)
    full_description = Column(String)
    img_path = Column(String)
    purchased_product = relationship("Purchase", back_populates="product")
    reviewed_product = relationship("Review", back_populates="product")
    wishlisted_product = relationship("Wishlist", back_populates="product")
    product_in_cart = relationship("Cart", back_populates="product")
    product_tag = relationship("ProductTag", back_populates="product")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    product_tag = relationship("ProductTag", back_populates="tag")


class Purchase(Base):
    __tablename__ = "purchases"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True)
    purchase_date = Column(Date)
    user = relationship("User", back_populates="purchase")
    product = relationship("Product", back_populates="purchased_product")


class Review(Base):
    __tablename__ = "reviews"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True)
    review_date = Column(Date)
    review_details = Column(String)
    review_recommendation = Column(String)
    user = relationship("User", back_populates="review")
    product = relationship("Product", back_populates="reviewed_product")


class Wishlist(Base):
    __tablename__ = "wishlists"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True)
    user = relationship("User", back_populates="wishlist")
    product = relationship("Product", back_populates="wishlisted_product")


class Cart(Base):
    __tablename__ = "carts"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True)
    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="product_in_cart")


class ProductTag(Base):
    __tablename__ = "product_tags"
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True)
    tag = relationship("Tag", back_populates="product_tag")
    product = relationship("Product", back_populates="product_tag")
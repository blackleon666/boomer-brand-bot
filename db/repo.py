import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.models import Base, User, Product, Order, Complaint, Campaign
from crypto.encrypt import encrypt_text, decrypt_text

# Get the database path from config
from config import DB_PATH

# Database setup
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User operations
def get_or_create_user(db, telegram_id: int, username: str = None, first_name: str = None):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# Product operations (assuming products are pre-populated from social media)
def get_products(db):
    return db.query(Product).all()

def get_product_by_id(db, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# Order operations
def create_order(db, user_id: int, product_id: int, quantity: int = 1):
    order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order_status(db, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    return order.status if order else None

# Complaint operations with encryption
def log_complaint(db, user_id: int, message: str):
    encrypted_message = encrypt_text(message)
    complaint = Complaint(user_id=user_id, message=encrypted_message)
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint.id

def get_complaint(db, complaint_id: int):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if complaint:
        complaint.message = decrypt_text(complaint.message)
    return complaint

# Campaign operations
def get_active_campaigns(db):
    return db.query(Campaign).filter(Campaign.is_active == True).all()

def add_campaign(db, message: str):
    campaign = Campaign(message=message)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign
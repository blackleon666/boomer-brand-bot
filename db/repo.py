import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from cryptography.fernet import Fernet

from config import DB_PATH, ENCRYPTION_KEY

# Database setup
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================
# MODELS - VERİTABANI TABLOLARI
# ============================================
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_interaction = Column(DateTime(timezone=True), server_default=func.now())
    conversation_context = Column(Text, nullable=True)  # Son 5 mesajı saklar
    total_messages = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price_visible = Column(Boolean, default=False)
    price_value = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_post_id = Column(String, nullable=True)
    source_date = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer, default=1)
    status = Column(String, default='hazırlanıyor')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Complaint(Base):
    __tablename__ = 'complaints'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message_encrypted = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved = Column(Boolean, default=False)

class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

# ============================================
# YARDIMCI FONKSİYONLAR
# ============================================
def get_cipher():
    if not ENCRYPTION_KEY:
        return None
    return Fernet(ENCRYPTION_KEY.encode())

def encrypt_text(plaintext):
    cipher = get_cipher()
    if not cipher:
        return plaintext
    return cipher.encrypt(plaintext.encode()).decode()

def decrypt_text(encrypted_text):
    cipher = get_cipher()
    if not cipher:
        return encrypted_text
    return cipher.decrypt(encrypted_text.encode()).decode()

# ============================================
# KULLANICI İŞLEMLERİ
# ============================================
def get_or_create_user(db, telegram_id: int, username: str = None, first_name: str = None):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id, 
            username=username, 
            first_name=first_name,
            conversation_context=""
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def update_user_context(db, telegram_id: int, new_message: str):
    """Kullanıcının konuşma bağlamını güncelle - Öğrenme"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return
    
    # Son 5 mesajı sakla
    context = user.conversation_context or ""
    messages = context.split("||") if context else []
    messages.append(new_message)
    # Sadece son 5 mesajı tut
    messages = messages[-5:]
    user.conversation_context = "||".join(messages)
    user.total_messages = (user.total_messages or 0) + 1
    user.last_interaction = func.now()
    
    db.commit()

def get_user_context(telegram_id: int) -> str:
    """Kullanıcının önceki konuşmalarını getir"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user and user.conversation_context:
            return user.conversation_context.replace("||", " | ")
        return ""
    finally:
        db.close()

# ============================================
# ÜRÜN İŞLEMLERİ
# ============================================
def get_products(db):
    return db.query(Product).all()

def get_product_by_id(db, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# ============================================
# SİPARİŞ İŞLEMLERİ
# ============================================
def create_order(db, user_id: int, product_id: int, quantity: int = 1):
    order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order_status(db, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    return order.status if order else None

# ============================================
# ŞİKAYET İŞLEMLERİ
# ============================================
def log_complaint(db, user_id: int, message: str):
    encrypted_message = encrypt_text(message)
    complaint = Complaint(user_id=user_id, message_encrypted=encrypted_message)
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint.id

# ============================================
# KAMPANYA İŞLEMLERİ
# ============================================
def get_active_campaigns(db):
    return db.query(Campaign).filter(Campaign.is_active == True).all()

def add_campaign(db, message: str):
    campaign = Campaign(message=message)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Connection URL - replacing postgres:// with postgresql:// for SQLAlchemy compatibility
DATABASE_URL = "postgres://postgres:6eEZzlFtdjI85h1uaBMBu5BXXkgUMWr8umEvpz0FAhYjOlnrnkZuz33tW6Eoftok@93.177.102.172:5432/postgres"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    card_id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    logs = relationship("AccessLog", back_populates="user")

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String, ForeignKey("users.card_id"), nullable=False)
    scan_time = Column(DateTime, default=datetime.utcnow)
    action = Column(String, nullable=False)  # 'ENTRY' or 'EXIT'

    user = relationship("User", back_populates="logs")

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist).")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for CLI and direct usage
def add_user(card_id, full_name):
    db = SessionLocal()
    try:
        user = User(card_id=card_id, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return True
    except IntegrityError:
        db.rollback()
        return False
    finally:
        db.close()

def get_user(card_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.card_id == card_id).first()
        if user:
            # Return dict to be compatible with old CLI code structure if needed
            return {"card_id": user.card_id, "full_name": user.full_name, "created_at": user.created_at}
        return None
    finally:
        db.close()

def get_last_action(card_id):
    db = SessionLocal()
    try:
        log = db.query(AccessLog).filter(AccessLog.card_id == card_id).order_by(AccessLog.scan_time.desc()).first()
        return log.action if log else None
    finally:
        db.close()

def log_access(card_id, action):
    db = SessionLocal()
    try:
        log = AccessLog(card_id=card_id, action=action)
        db.add(log)
        db.commit()
        return log
    finally:
        db.close()

def get_logs(card_id=None):
    db = SessionLocal()
    try:
        query = db.query(AccessLog).join(User).order_by(AccessLog.scan_time.desc())
        if card_id:
            query = query.filter(AccessLog.card_id == card_id)
        
        results = []
        for log in query.all():
            results.append({
                "full_name": log.user.full_name,
                "card_id": log.card_id,
                "scan_time": log.scan_time,
                "action": log.action
            })
        return results
    finally:
        db.close()

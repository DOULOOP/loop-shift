from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import database as db_module
from database import get_db, User, AccessLog, init_db

app = FastAPI(title="Card Access System API")

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Pydantic Models
class UserCreate(BaseModel):
    card_id: str
    full_name: str

class UserResponse(BaseModel):
    card_id: str
    full_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class ScanRequest(BaseModel):
    card_id: str

class LogResponse(BaseModel):
    id: int
    card_id: str
    action: str
    scan_time: datetime
    full_name: Optional[str] = None # Added for convenience

    class Config:
        orm_mode = True

# API Endpoints

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.card_id == user.card_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Card ID already registered")
    
    new_user = User(card_id=user.card_id, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{card_id}", response_model=UserResponse)
def read_user(card_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.card_id == card_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/scan", response_model=LogResponse)
def scan_card(scan: ScanRequest, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.card_id == scan.card_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Card ID not recognized. Please register first.")

    # Determine action (Entry/Exit)
    last_log = db.query(AccessLog).filter(AccessLog.card_id == scan.card_id).order_by(AccessLog.scan_time.desc()).first()
    
    if last_log and last_log.action == 'ENTRY':
        new_action = 'EXIT'
    else:
        new_action = 'ENTRY'

    new_log = AccessLog(card_id=scan.card_id, action=new_action)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    # Construct response with user name
    response = LogResponse.from_orm(new_log)
    response.full_name = user.full_name
    return response

@app.get("/history", response_model=List[LogResponse])
def get_history(card_id: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(AccessLog).join(User).order_by(AccessLog.scan_time.desc())
    
    if card_id:
        query = query.filter(AccessLog.card_id == card_id)
    
    logs = query.limit(limit).all()
    
    # Map to response with names
    results = []
    for log in logs:
        log_resp = LogResponse.from_orm(log)
        log_resp.full_name = log.user.full_name
        results.append(log_resp)
        
    return results

@app.get("/")
def read_root():
    return {"message": "Welcome to the Card Access System API"}

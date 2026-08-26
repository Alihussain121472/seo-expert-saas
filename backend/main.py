from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta

import models
import schemas
import auth
from database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SEO Expert API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI SEO Expert Agent API"}

# --- AUTH ENDPOINTS ---
@app.post("/api/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login_for_access_token(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # Using UserCreate for email/password simplification. Ideally use OAuth2PasswordRequestForm
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- WEBSITES ENDPOINTS ---
@app.get("/api/websites", response_model=list[schemas.WebsiteResponse])
def get_user_websites(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    websites = db.query(models.Website).filter(models.Website.owner_id == current_user.id).all()
    return websites

from fastapi import BackgroundTasks

def run_background_audit(website_id: str, url: str, db: Session):
    try:
        from crawler import crawl_page
        from agents.audit import run_seo_audit
        import models
        
        crawl_data = crawl_page(url)
        audit_result = run_seo_audit(crawl_data)
        
        new_audit = models.SEOAudit(
            website_id=website_id,
            score=audit_result.overall_score,
            technical_score=audit_result.technical_score,
            on_page_score=audit_result.on_page_score
        )
        db.add(new_audit)
        
        for rec in audit_result.recommendations:
            task = models.SEOTask(
                website_id=website_id,
                title=rec.title,
                description=rec.description,
                priority=rec.priority
            )
            db.add(task)
        db.commit()
    except Exception as e:
        print(f"Background audit failed for {url}: {e}")

@app.post("/api/websites", response_model=schemas.WebsiteResponse)
def add_website(website: schemas.WebsiteCreate, background_tasks: BackgroundTasks, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_website = models.Website(url=website.url, name=website.name, owner_id=current_user.id)
    db.add(new_website)
    db.commit()
    db.refresh(new_website)
    
    # Automatically trigger the AI Agent to start working immediately
    background_tasks.add_task(run_background_audit, new_website.id, new_website.url, SessionLocal())
    
    return new_website

from agents.manager import get_seo_manager_response, ChatRequest
from agents.audit import run_seo_audit
from crawler import crawl_page

@app.post("/api/chat")
def chat_with_agent(request: dict, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = request.get("message", "")
    language = request.get("language", "English")
    
    # Gather context
    websites = db.query(models.Website).filter(models.Website.owner_id == current_user.id).all()
    website_data = [{"id": w.id, "url": w.url, "name": w.name} for w in websites]
    
    context = {
        "user_name": current_user.full_name,
        "websites": website_data,
        "tasks": [] # Fetch pending tasks here in full implementation
    }
    
    chat_req = ChatRequest(message=message, user_id=current_user.id, preferred_language=language, context=context)
    response_text = get_seo_manager_response(chat_req)
    
    return {"reply": response_text}

@app.post("/api/websites/{website_id}/audit")
def trigger_audit(website_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    website = db.query(models.Website).filter(models.Website.id == website_id, models.Website.owner_id == current_user.id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
        
    crawl_data = crawl_page(website.url)
    audit_result = run_seo_audit(crawl_data)
    
    # Save audit result to DB
    new_audit = models.SEOAudit(
        website_id=website.id,
        score=audit_result.overall_score,
        technical_score=audit_result.technical_score,
        on_page_score=audit_result.on_page_score
    )
    db.add(new_audit)
    
    # Save tasks
    for rec in audit_result.recommendations:
        task = models.SEOTask(
            website_id=website.id,
            title=rec.title,
            description=rec.description,
            priority=rec.priority
        )
        db.add(task)
        
    db.commit()
    return {"message": "Audit completed successfully", "score": audit_result.overall_score}


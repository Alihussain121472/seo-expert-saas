from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    websites = relationship("Website", back_populates="owner")

class Website(Base):
    __tablename__ = "websites"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    url = Column(String, index=True, nullable=False)
    name = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="websites")
    audits = relationship("SEOAudit", back_populates="website")
    tasks = relationship("SEOTask", back_populates="website")

class SEOAudit(Base):
    __tablename__ = "seo_audits"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    website_id = Column(String, ForeignKey("websites.id"))
    score = Column(Float, nullable=True)
    technical_score = Column(Float, nullable=True)
    on_page_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    website = relationship("Website", back_populates="audits")

class SEOTask(Base):
    __tablename__ = "seo_tasks"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    website_id = Column(String, ForeignKey("websites.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="Medium") # Critical, High, Medium, Low
    status = Column(String, default="Not Started") # Not Started, In Progress, Completed, Ignored
    affected_pages = Column(Text, nullable=True) # JSON list of URLs
    created_at = Column(DateTime, default=datetime.utcnow)
    
    website = relationship("Website", back_populates="tasks")

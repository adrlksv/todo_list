from sqlalchemy import (Column, Integer, String, JSON, 
                        CheckConstraint, Boolean, ForeignKey, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime


Base = declarative_base()

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False)
    permissions = Column(JSON)
    users = relationship("User", back_populates="role")

    # __table_args__ = (
    #     CheckConstraint("role_name IN ('admin', 'user', 'guest')",
    #                     name="role_name_constraint")
    # )

    def __str__(self):
        return f"Role(id={self.id}, name={self.name})"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    role = relationship("Role", back_populates="users")
    tasks = relationship("Task", back_populates="user")

    def __str__(self):
        return f"User(id={self.id}, email={self.email})"

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="tasks")

    def __str__(self):
        return f"Task(id={self.id}, task_name={self.task_name}, description={self.description})"

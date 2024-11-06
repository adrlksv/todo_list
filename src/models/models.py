from sqlalchemy import (Table, Column, Integer, MetaData,
                        String, Boolean, TIMESTAMP)

from datetime import datetime


metadata = MetaData()

task = Table(
    "task",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task_name", String, nullable=True),
    Column("description", String, nullable=True),
    Column("is_completed",Boolean, default=False, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow, nullable=True),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True),
)

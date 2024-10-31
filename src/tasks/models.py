from sqlalchemy import (MetaData, Table, Column, Integer, 
                        String, TIMESTAMP)

from datetime import datetime


metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("email", String),
    Column("registered_at", String, default=datetime.utcnow)
)

task = Table(
    "task",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task_name", String),
    Column("description", String),
    Column("created_at", TIMESTAMP, default=datetime.utcnow)
)

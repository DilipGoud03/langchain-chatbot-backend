from sqlalchemy import Column, Integer, String
from datetime import datetime
from db import Base
from sql.models.user_addresses import UserAddresses
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=True, default=False)
    user_type = Column(String(255), nullable=True, default='employee')
    created_at = Column(String(255), default=datetime.now(), nullable=False)
    updated_at = Column(String(255), nullable=False, onupdate=datetime.now())
    addresses = relationship(UserAddresses, cascade="all,delete", backref='users')

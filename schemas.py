from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Profile(BaseModel):
    id: int
    name: str
    address: str
    mobile: str
    password: str
    email: str


class ReadProfile(BaseModel):
    id: int
    name: str
    address: str
    mobile: str
    password: str
    email: str
    class Config:
        from_attributes = True


class Records(BaseModel):
    id: int
    username: str
    address: str
    pincode: str


class ReadRecords(BaseModel):
    id: int
    username: str
    address: str
    pincode: str
    class Config:
        from_attributes = True


class Class(BaseModel):
    id: int


class ReadClass(BaseModel):
    id: int
    class Config:
        from_attributes = True


class Users(BaseModel):
    id: int
    username: str
    password: str
    test: str
    test123: str


class ReadUsers(BaseModel):
    id: int
    username: str
    password: str
    test: str
    test123: str
    class Config:
        from_attributes = True


class Students(BaseModel):
    id: int
    name: str
    age: str


class ReadStudents(BaseModel):
    id: int
    name: str
    age: str
    class Config:
        from_attributes = True



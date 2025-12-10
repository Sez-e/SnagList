from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from session import get_db


router = APIRouter()
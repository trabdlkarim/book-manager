import json
from pathlib import Path

__path = Path(__file__).resolve().parent
BOOKS = []

with open(str(__path / 'books.json')) as data:
   BOOKS = json.load(data) 

import json
from pathlib import Path

__path = Path(__file__).resolve().parent
__books = []

with open(str(__path / 'books.json')) as data:
 __books = json.load(data) 

__authors_dic = [ {'name': book['author'], 'country': book['country']} for book in __books ]

DEFAULT_AUTHORS = [dict(t) for t in  set([tuple(author.items()) for author in __authors_dic ])]
# coding: utf-8

from pony.orm import *
from datetime import datetime

__author__ = 'think'

db = Database()

class BookPoint(db.Entity):
    id = PrimaryKey(int)
    book_version_id = Required(int)
    book_version_name = Required(str, 50)
    book_type_id = Required(int)
    book_type_name = Required(str, 50)
    point_name = Required(str, 100)
    subject_name = Required(str, 50)
    father_id = Required(int)

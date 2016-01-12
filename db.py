# coding: utf-8

from pony.orm import *
from models import *

__author__ = 'think'


sql_debug(True)


db.bind("mysql",
        host="568486bb14d22.sh.cdb.myqcloud.com", port=3454,
        user="cdb_outerroot",passwd="yitiku1228",db="tongbu_points",
        charset="utf8")

db.generate_mapping(create_tables=True)

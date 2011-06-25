# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------
from db.bookentry import BookEntryTable
from db import master_session
import math

class BookEntry(object):
    
    def __init__(self):
        self._data = []
    
    def load_all(self):
        self._data = self.get_all()
        
    def get_entries(self):
        MAX_SIZE = 4
        data = []
        length = int(math.ceil(len(self._data)/float(MAX_SIZE)))
        for i in xrange(length):
            before = i*MAX_SIZE
            after = i*MAX_SIZE + MAX_SIZE
            data.append(self._data[before:after])
        return data
        
    def get_all(self):
        s = master_session()
        return s.query(BookEntryTable).order_by(BookEntryTable.id).all()
    
class BookEntryUpdater(object):
    
    @staticmethod
    def add(title, img, term, searchindex, node):
        b = BookEntryTable(title, img, term, searchindex, node)
        s = master_session()
        s.add(b)
        s.commit()
        return b.id
    
    @staticmethod
    def update(id, img):
        b = BookEntryUpdater.get_one(id)
        b.img = img
        s = master_session()
        s.add(b)
        s.commit()
        
    @staticmethod
    def get_all():
        s = master_session()
        return s.query(BookEntryTable).order_by(BookEntryTable.id).all()
    
    @staticmethod
    def get_one(id):
        s = master_session()
        return s.query(BookEntryTable).filter_by(id=id).one()

    @staticmethod
    def truncate():
        s = master_session()
        s.execute("TRUNCATE %s" % BookEntryTable.__tablename__)

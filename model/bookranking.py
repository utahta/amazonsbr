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
from db import master_session
from db.bookranking import BookRankingTable0, BookRankingTable1
from model.updatesys import UpdateSys
from db.bookentry import BookEntryTable

class BookRanking(object):
    
    def __init__(self):
        usys = UpdateSys()
        if usys.get_rankno() == 0:
            rankclass = BookRankingTable0
        elif usys.get_rankno() == 1:
            rankclass = BookRankingTable1
        else:
            raise Exception('Invalid rankno. rankno:%s' % usys.get_rankno())
        self._klass = rankclass
        self._entries = []
        self._entry_id = 0
        self._total_num = None
        self._page = 1
        self._limit = 10
        self._book_entry = None
        
    def load_entries(self, entry_id, page=1, limit=10):
        page -= 1
        if page < 0:
            page = 0
        offset = page * limit
        print page, offset, limit
        s = master_session()
        self._entries = s.query(self._klass).filter_by(entry_id=entry_id).limit(limit).offset(offset)
        self._entry_id = entry_id
        self._total_num = s.query(self._klass).filter_by(entry_id=entry_id).count()
        self._page = page
        self._limit = limit
        self._book_entry = s.query(BookEntryTable).filter_by(id=entry_id).one()
    
    def get_entries(self):
        return self._entries
    
    def get_entry_id(self):
        return self._entry_id
    
    def get_total_num(self):
        return self._total_num
    
    def get_entry_title(self):
        if self._book_entry:
            return self._book_entry.title
        return ''
    
class BookRankingUpdater(object):
    def __init__(self):
        usys = UpdateSys()
        if usys.get_update_rankno() == 0:
            rankclass = BookRankingTable0
        elif usys.get_update_rankno() == 1:
            rankclass = BookRankingTable1
        else:
            raise Exception('Invalid rankno. rankno:%s' % usys.get_update_rankno())
        self._klass = rankclass
    
    def add(self, entry_id, rank, **kwargs):
        s = master_session()
        s.add(self._klass(entry_id, rank, **kwargs))
        s.commit()

    def truncate(self):
        s = master_session()
        s.execute("TRUNCATE %s" % self._klass.__tablename__)

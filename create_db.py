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
from db.bookranking import BookRankingTable0, BookRankingTable1
from db import master_engine, master_session
from db.updatesys import UpdateSysTable

def create_master_tables(t):
    try:
        t.drop(bind=master_engine)
    except:
        pass
    t.create(bind=master_engine)

# Create table
create_master_tables(UpdateSysTable.__table__)
create_master_tables(BookEntryTable.__table__)
create_master_tables(BookRankingTable0.__table__)
create_master_tables(BookRankingTable1.__table__)

# Insert default row
t = UpdateSysTable()
master_session.add(t)

master_session.commit()

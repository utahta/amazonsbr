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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.dialects.mysql import INTEGER as Integer

Base = declarative_base()
class BookEntryTable(Base):
    __tablename__ = 'tb_bookentry'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id = Column(Integer(unsigned=True), autoincrement=True, primary_key=True)
    title = Column(String(length=256), nullable=False)
    img = Column(String(length=256), nullable=False)
    term = Column(String(length=256), nullable=False)
    searchindex = Column(String(length=256), nullable=False)
    node = Column(String(length=256), nullable=False)
    
    def __init__(self, title, img, term, searchindex, node):
        self.title = title
        self.img = img
        self.term = term
        self.searchindex = searchindex
        self.node = node
        
    def __repr__(self):
        return "<id:%s title:%s img:%s term:%s searchindex:%s node:%s>" % (
                self.id, self.title, self.img, self.term, self.searchindex, self.node)

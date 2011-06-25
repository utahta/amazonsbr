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
class BookRankingTable(object):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id = Column(Integer(unsigned=True), autoincrement=True, primary_key=True)
    entry_id = Column(Integer(unsigned=True), nullable=False, index=True)
    rank = Column(Integer(unsigned=True), nullable=False, index=True)
    title = Column(String(length=256), nullable=False)
    img = Column(String(length=256), nullable=False)
    smallimg = Column(String(length=256), nullable=False)
    url = Column(String(length=1024), nullable=False)
    baseurl = Column(String(length=256), nullable=False)
    author = Column(String(length=256), nullable=False)
    fmtprice = Column(String(length=64), nullable=False)
    publicationdate = Column(String(length=64), nullable=False)
    publisher = Column(String(length=256), nullable=False)
    pages = Column(Integer(unsigned=True), nullable=False)
    
    def __init__(self, entry_id, rank, **kwargs):
        self.entry_id = entry_id
        self.rank = rank
        self.title = kwargs.get('title')
        self.img = kwargs.get('img')
        self.smallimg = kwargs.get('smallimg')
        self.url = kwargs.get('url')
        self.baseurl = kwargs.get('baseurl')
        self.author = kwargs.get('author')
        self.fmtprice = kwargs.get('fmtprice')
        self.publicationdate = kwargs.get('publicationdate')
        self.publisher = kwargs.get('publisher')
        self.pages = kwargs.get('pages')
        
    def __repr__(self):
        return "<entry_id:%s rank:%s title:%s img:%s url:%s baseurl:%s>" % (
                self.entry_id, self.rank, self.title, self.img, self.url, self.baseurl)

class BookRankingTable0(Base, BookRankingTable):
    __tablename__ = 'tb_bookranking_0'
    def __init__(self, entry_id, rank, **kwargs):
        BookRankingTable.__init__(self, entry_id, rank, **kwargs)

class BookRankingTable1(Base, BookRankingTable):
    __tablename__ = 'tb_bookranking_1'
    def __init__(self, entry_id, rank, **kwargs):
        BookRankingTable.__init__(self, entry_id, rank, **kwargs)

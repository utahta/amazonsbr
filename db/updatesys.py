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
from sqlalchemy.dialects.mysql import INTEGER as Integer

Base = declarative_base()
class UpdateSysTable(Base):
    __tablename__ = 'tb_updatesys'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id = Column(Integer(unsigned=True), primary_key=True)
    rankno = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False)
    
    def __init__(self):
        self.id = 1
        self.rankno = 0
        self.available = 1
        
    def __repr__(self):
        return "<id:%s rankno:%s available:%s>" % (
                self.id, self.rankno, self.available)

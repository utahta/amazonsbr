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
from db.updatesys import UpdateSysTable

class UpdateSys(object):
    def __init__(self):
        s = master_session()
        o = s.query(UpdateSysTable).one()
        self.rankno = o.rankno
        self.available = o.available
    
    def get_rankno(self):
        return self.rankno
    
    def get_update_rankno(self):
        return 1 - self.rankno
    
    def run_update(self):
        s = master_session()
        num_rows = s.query(UpdateSysTable).filter_by(id=1, available=1).update({'available':0})
        s.commit()
        return num_rows > 0
    
    def updated(self):
        rankno = self.get_update_rankno()
        s = master_session()
        num_rows = s.query(UpdateSysTable).filter_by(id=1, available=0).update({'rankno':rankno, 'available':1})
        s.commit()
        return num_rows > 0

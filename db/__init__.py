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
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from config import DB_MASTER

master_engine = create_engine(DB_MASTER)
master_session = scoped_session(sessionmaker(bind=master_engine))

def session_remove():
    master_session.remove()

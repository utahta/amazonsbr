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
from flask import Flask
from config import appconfig
from controller.top import topapp
from controller.ranking import rankapp

app = Flask(__name__)
app.debug = appconfig['debug']
app.register_module(topapp)
app.register_module(rankapp, url_prefix='/ranking')

if __name__ == '__main__':
    app.run(appconfig['host'])
    
application = app

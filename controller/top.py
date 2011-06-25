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
from flask import Module, render_template
from model.bookentry import BookEntry

topapp = Module(__name__)

@topapp.route('/')
def index():
    entry = BookEntry()
    entry.load_all()
    return render_template('index.html', entry=entry)

@topapp.route('/about')
def about():
    return render_template('about.html')

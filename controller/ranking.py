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
from flask import Module, render_template, request
from model.bookranking import BookRanking
from util.pagenav import PageNav

rankapp = Module(__name__)

@rankapp.route('/<int:id>')
def index(id):
    page = int(request.values.get('page', 1))
    limit = 10
    width = 3
    ranking = BookRanking()
    ranking.load_entries(id, page, limit)
    nav = PageNav(ranking.get_total_num(), limit, page, width).create()
    return render_template('ranking.html', ranking=ranking, nav=nav)

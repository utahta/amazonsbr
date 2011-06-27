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
import math

class PageNav(object):
    class Link(object):
        def __init__(self, prev_page, next_page, page, max_page, list_pages, start_flag, end_flag):
            self.prev_page = prev_page
            self.next_page = next_page
            self.page = page
            self.max_page = max_page
            self.list_pages = list_pages
            self.start_flag = start_flag
            self.end_flag = end_flag
        
        def __repr__(self):
            return "<prev:%s next:%s page:%s max:%s list:%s start:%s end:%s>" % (
                    self.prev_page, self.next_page, self.page, self.max_page, self.list_pages, self.start_flag, self.end_flag)
    
    def __init__(self, total_num, limit, radius=10):
        """
        total_num:
        limit: 
        """
        total_num = int(total_num)
        if total_num <= 0:
            raise Exception("Invalid arguments. total_num >= 1. total_num:%s" % total_num)
        limit = int(limit)
        if limit <= 0:
            raise Exception("Invalid arguments. limit >= 1. limit:%s" % limit)
        self._total_num = total_num
        self._limit = limit
        self._max_page = int(math.ceil(total_num / limit))
        self._radius = radius
    
    def get(self, page):
        """
        page: 1 - N
        """
        page = int(page)
        if page <= 0:
            raise Exception("Invalid arguments. page >= 1. page:%s" % page)
        max_page = self._max_page
        radius = self._radius
        start_flag = False
        end_flag = False
        
        if page == 1:
            prev_page = 1
        else:
            prev_page = page -1
        if page < max_page:
            next_page = page + 1
        else:
            next_page = max_page
        
        list_pages = []
        if max_page < radius:
            for i in xrange(page, max_page+1):
                list_pages.append(i)
        else:
            if (page+radius) > max_page:
                start_res = page + radius - max_page
            else:
                start_res = 0
            if (page-radius) < 0:
                end_res = radius - page
            else:
                end_res = 0
            
            if (page - radius) <= 2:
                start_page = 1
            else:
                start_flag = True
                if (page - radius - start_res) > 0:
                    start_page = page - radius - start_res
                else:
                    start_page = page - radius
                    
            if (page + radius) >= (max_page-1):
                end_page = max_page
            else:
                end_flag = True
                if (page + radius + end_res) < max_page:
                    end_page = page + radius + end_res
                else:
                    end_page = page + radius
            
            for i in xrange(start_page, end_page+1):
                list_pages.append(i)
        return PageNav.Link(prev_page, next_page, page, max_page, list_pages, start_flag, end_flag)

if __name__ == "__main__":
    total_num = 201
    radius = 3
    p = PageNav(total_num, 10, radius)
    for i in xrange(1, 13):
        print p.get(i)
    
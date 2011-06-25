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
from amazon.api import item_search
import urlparse
import urllib
import json
import time
import re
from model.bookranking import BookRankingUpdater
from model.bookentry import BookEntryUpdater
from model.updatesys import UpdateSys
import sys
import codecs
from lxml import objectify

# for cron
sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)
sys.stderr = codecs.lookup('utf_8')[-1](sys.stderr)

class AmazonItem(object):
    def __init__(self, item, keywords):
        self.title = item.ItemAttributes.Title.text
        keywords = re.escape(keywords)
        c = re.compile(keywords, re.IGNORECASE)
        if c.search(self.title):
            self.include_keywords = 1
        else:
            self.include_keywords = 0
        try:
            self.img = item.MediumImage.URL.text
        except AttributeError:
            self.img = ""
        try:
            self.smallimg = item.SmallImage.URL.text
        except AttributeError:
            self.smallimg = ""
        self.url = item.DetailPageURL.text
        p = urlparse.urlparse(urllib.unquote(self.url.encode('utf8')))
        self.baseurl = urlparse.urlunparse((p[0], p[1], p[2], '', '', '')).decode('utf8')
        try:
            if len(item.ItemAttributes.Author) > 1:
                self.author = ",".join([a.text for a in item.ItemAttributes.Author])
            else:
                self.author = item.ItemAttributes.Author.text
        except AttributeError:
            self.author = ''
        try:
            self.fmtprice = item.ItemAttributes.ListPrice.FormattedPrice.text
        except AttributeError:
            self.fmtprice = ""
        try:
            self.publicationdate = item.ItemAttributes.PublicationDate.text
        except AttributeError:
            self.publicationdate = ""
        try:
            self.publisher = item.ItemAttributes.Publisher.text
        except AttributeError:
            self.publisher = ""
        self.pages = int(item.ItemAttributes.NumberOfPages)
        try:
            self.salesrank = int(item.SalesRank)
        except AttributeError:
            self.salesrank = 4294967295
        self.hateb = self._get_hateb()
        self.rt = self._get_rt()
        self.like = self._get_like()
        print self.title, self.include_keywords, self.hateb, self.rt, self.like, self.salesrank
        
    def _get_hateb(self):
        for i in xrange(3): # retry 3
            try:
                result = urllib.urlopen('http://b.hatena.ne.jp/entry/jsonlite/?url=%s' % (self.baseurl.encode('utf8')))
                obj = json.loads(result.read())
            except:
                print '--- get hateb retry %d ---' % i
                time.sleep(1)
                continue
            if obj:
                return int(obj['count'])
            else:
                return 0
        return 0
    
    def _get_rt(self):
        for i in xrange(3): # retry 3
            try:
                result = urllib.urlopen('http://urls.api.twitter.com/1/urls/count.json?url=%s' % (self.baseurl.encode('utf8')))
                obj = json.loads(result.read())
            except:
                print '--- get rt retry %d ---' % i
                time.sleep(1)
                continue
            if obj:
                return int(obj['count'])
            else:
                return 0
        return 0
    
    def _get_like(self):
        for i in xrange(3): # retry 3
            try:
                result = urllib.urlopen('https://api.facebook.com/method/fql.query?query=select like_count,total_count,share_count,click_count from link_stat where url="%s"' % (self.baseurl.encode('utf8')))
                root = objectify.fromstring(result.read())
            except:
                print '--- get like retry %d ---' % i
                time.sleep(1)
                continue
            if len(root):
                return int(root.link_stat.total_count.text)
            else:
                return 0
        return 0
    
    def get_dict(self):
        return {
            'title': self.title, 'img': self.img, 'url': self.url, 'baseurl': self.baseurl,
            'author': self.author, 'fmtprice': self.fmtprice, 'publicationdate': self.publicationdate,
            'publisher': self.publisher, 'pages': self.pages, 'smallimg': self.smallimg
        }
    
    def __cmp__(self, other):
        if self.include_keywords == other.include_keywords:
            self_point = self.hateb + self.rt + self.like
            other_point = other.hateb + other.rt + other.like
            if self_point == other_point:
                return cmp(self.salesrank, other.salesrank)
            else:
                return cmp(self_point, other_point)
        return cmp(self.include_keywords, other.include_keywords)
    
    def __repr__(self):
        return '<title:%s img:%s url:%s baseurl:%s hateb:%s>' % (self.title, self.img, self.url, self.baseurl, self.hateb)

# main
usys = UpdateSys()
if not usys.run_update():
    print 'already running.'
    sys.exit()

# Truncate
bookrank = BookRankingUpdater()
bookrank.truncate()

# Update
for e in BookEntryUpdater.get_all():
    entry_id = e.id
    opt = {}
    opt['Keywords'] = e.term
    opt['SearchIndex'] = e.searchindex
    if e.node:
        opt['BrowseNode'] = e.node
    opt['ResponseGroup'] = 'Medium,Reviews'
    opt['ItemPage'] = 1
    print entry_id, opt
    
    root = item_search(**opt)
    total_results = int(root.Items.TotalResults)
    print total_results
    keywords = opt['Keywords']
    items = []
    if(total_results > 0):
        for item in root.Items.Item:
            try:
                items.append(AmazonItem(item, keywords))
            except:
                continue
            time.sleep(0.5)
        
        total_pages = int(root.Items.TotalPages)
        if(total_pages > 11):
            total_pages = 11
        for page in xrange(2, total_pages):
            opt['ItemPage'] = page
            root = item_search(**opt)
            for item in root.Items.Item:
                try:
                    items.append(AmazonItem(item, keywords))
                except:
                    continue
                time.sleep(0.5)
    
    print 'length:%s' % len(items)
    items.sort(reverse=True)
    items = items[:100]
    if len(items) > 0:
        item = items[0]
        BookEntryUpdater.update(entry_id, item.img)
    
    rank = 1
    for item in items:
        bookrank.add(entry_id, rank, **item.get_dict())
        rank += 1

usys.updated()

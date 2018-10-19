#!/usr/bin/env python3

"""
code reused from project  https://github.com/Backlist/backlist-workflows by Brian Jones

The MIT License (MIT)

Copyright (c) 2015 Backlist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import re
from pyzotero import zotero

def create_collection(collection_name, items):
    test_collection = dict([
        ('name', collection_name)
    ])

    collections_data = json.loads(json.dumps(zot.collections()))
    
    #testing if collection exists
    for collection in  collections_data:
            if collection['data']['name'] == collection_name:
                collection_id = collection['data']['key']
                print("Reusing existing collection…")

    if len(collection_id) < 0:
        response = zot.create_collection([test_collection])
        collection_result = json.loads(json.dumps(response))
        print("Creating collection…")
        collection_id = collection_result['success']['0']

    print("Creating items…")
    created_items = zot.create_items(items)
    # print(created_items)
    for key in created_items['successful'].keys():
        print("Retrieve item…")
        item = zot.item(created_items['successful'][key]['key'])
        print("Add item to Collection…")
        zot.addto_collection(collection_id, item)

def prepare_item(item):
    #print("Preparing item...")
    #print(item)
    template = zot.item_template(item['itemtype'])
    template['creators'] = []
    if 'author' in item:
        authors = creators_list(item['author'], 'author')
        template['creators'] += authors
    template['title'] = item['title']
    if 'publisher' in item.keys():
        template['publisher'] = item['publisher']
    if 'edition' in item.keys():
        template['edition'] = item['edition']
    if 'date' in item.keys():
        template['date'] = item['date']   
    template['url'] = item['url']
    template['libraryCatalog'] = item['source']
    
    return template

def creators_list(creator_names, creator_type):
    creators = []
    for name in creator_names.split(' and '):
        creator = {}
        creator['creatorType'] = creator_type
        creator['firstName'] = ' '.join(name.split(' ')[:-1])
        creator['lastName'] = name.split(' ')[-1]
        creators += [creator]
    
    return creators

zot_library_id = "YOUR_ZOTERO_LIBRARY_ID"
zot_library_type = "YOUR_ZOTERO_LIBRARY_TYPE"
zot_api_key = "YOUR_ZOTERO_API_KEY"
# Zotero Api Init
zot = zotero.Zotero(zot_library_id, zot_library_type, zot_api_key)
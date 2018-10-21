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
import yaml
import re
from pyzotero import zotero

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    
zot = zotero.Zotero(cfg['zot_library_id'],cfg['zot_library_type'],cfg['zot_api_key'])

def create_collection(collection_name):
    test_collection = dict([
        ('name', collection_name)
    ])
    collections_data = json.loads(json.dumps(zot.collections()))
    collection_id = ""
    #testing if collection exists
    for collection in  collections_data:
            if collection['data']['name'] == collection_name:
                collection_id = collection['data']['key']
                print(f"Reusing existing collection with key {collection_id}…")

    if  not collection_id:
        response = zot.create_collection([test_collection])
        collection_result = json.loads(json.dumps(response))
        print(f"Creating collection {collection_name}…")
        collection_id = collection_result['success']['0']
    
    return collection_id

def create_items(collection_id, items):
    print("Creating items…")
    created_items = zot.create_items(items)
    # print(created_items)
    for key in created_items['successful'].keys():
        print("Retrieve item…")
        item = zot.item(created_items['successful'][key]['key'])
        print(f"Add item to Collection {collection_id}…")
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
    template['extra'] = item['id']
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


#!/usr/bin/env python3

import retrieve_author_ppn as autppn
import retrieve_references as refs
import zot_helpers as pyzot
from itertools import islice

researchers = autppn.constructOutput('test.csv')

autppn.writeCsv('out.csv', researchers)

for researcher in researchers:
    ppn = researcher['ppn']
    creator_names = researcher['firstname']+" "+researcher['lastname']
    collection_name = researcher['lastname'].lower()+"_"+researcher['ppn']
    json_loaded = refs.getReferences(ppn)
    biblio = refs.getRefsByRole(json_loaded, 'aut', creator_names)
    total_items = len(biblio)

    print(f"Pushing {total_items} items in Zotero bibliography : {collection_name}")
    collection_id = pyzot.create_collection(collection_name)
    # print(collection_id)

    for i in range(0, total_items, 50):
        start = i
        if i+50 <= total_items:
            end = i+50
        else :
            end = total_items
        pyzot.create_items(collection_id, list(islice(biblio, start, end)))
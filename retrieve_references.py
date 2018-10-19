#!/usr/bin/env python3

import csv
import urllib.request,urllib.parse,json 
import re
import os, ssl
import zot_helpers as pyzot


# SSL exception
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

def getReferences(ppn):
    svc = "https://www.idref.fr/services/references/"+ppn+".json"
    req = urllib.request.urlopen(svc)
    data = req.read().decode('utf-8')
    return json.loads(data)
    # print(j_obj)

def getRefsByRole(obj, aut_role, creator_names):
    refs = obj['sudoc']['result']['role']
    biblio = [] 
    if len(refs) > 0 :
        for role in refs :
            if role['marc21Code'] == aut_role :
                docs = role['doc']
                if len(docs) > 0 :
                    for d in docs:

                        if d['referentiel'] == 'sudoc':
                            citation = d['citation'].split("/")
                            itemtype = 'book'
                            title = citation[0]
                            if len(citation) > 2:
                                edition = citation[2]
                                edition_list = citation[2].split(",")
                                publisher = edition_list[0].split(":")[-1]
                                if len(edition_list) > 1:
                                    date = ""
                                    date_litt = edition_list[1]
                                    date = re.search("([0-9]{4})", date_litt).group()
                            i = {'id':d['id'],'source':d['referentiel'],'itemtype':itemtype,'author': creator_names, 'title': title,'publisher': publisher, 'edition': edition, 'date': date, 'url': d['URI']}
                        elif d['referentiel'] == 'bnf':
                            citation = d['citation'].split("/")
                            itemtype = 'book'
                            title = citation[0]
                            if len(citation) > 2:
                                edition = citation[2]
                                date = ""
                                date = re.search("([0-9]{4})", edition).group()
                            i = {'id':d['id'],'source':d['referentiel'],'itemtype':itemtype,'author': creator_names, 'title': title,'edition': edition, 'date': date, 'url': d['URI']}
                        elif d['referentiel'] == 'theses':
                            itemtype = 'thesis'
                            i = {'id':d['id'],'itemtype':itemtype,'source':d['referentiel'],'author': creator_names,'title': d['citation'],'url': d['URI']}
                        else :
                            itemtype = 'journalArticle'
                            i = {'id':d['id'],'itemtype':itemtype,'source':d['referentiel'],'author': creator_names,'title': d['citation'],'url': d['URI']}
                        #print(i)
                        biblio.append(i)
    items = []
    for i in biblio:
        items.append(pyzot.prepare_item(i))
    
    return items


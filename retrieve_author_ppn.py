#!/usr/bin/env python3

import csv
import urllib.request,urllib.parse,json 
import os, ssl

# SSL exception
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

def getPpn(name,firstname,birthdate):
    query = urllib.parse.quote(name)+"%20"+urllib.parse.quote(firstname)+"%20"+birthdate
    svc = "https://www.idref.fr/Sru/Solr?q=persname_t:%22"+query+"%22%20AND%20recordtype_z:a&sort=score%20desc&version=2.2&start=0&rows=30&indent=on&fl=id,ppn_z,recordtype_z,affcourt_z&wt=json"
    # print(svc)
    ppn = ""
    req = urllib.request.urlopen(svc)
    data = req.read().decode('utf-8')
    j_obj = json.loads(data)
    numfound = j_obj['response']['numFound']
    if numfound > 0:
        ppn = j_obj['response']['docs'][0]['ppn_z']
    if numfound == 0 and birthdate != "":
        ppn = getPpn(name,firstname,"")
    
    return ppn

def constructOutput(input_file):
    output = []
    with open(input_file, 'r') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        for row in reader:
            ppn = getPpn(row[1],row[2],row[3])
            author = {'user_id':row[0] ,'firstname':row[2], 'lastname': row[1], 'ppn': ppn}
            output.append(author)
            csvfile.close()
    
    return output

def writeCsv(file, list_of_dicts):
    keys = list_of_dicts[0].keys()
    with open(file, 'w', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)
        output_file.close()

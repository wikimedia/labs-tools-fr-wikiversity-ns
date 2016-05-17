#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re
### Accessoire pour determiner le nombre de sous-pages pami les documents 
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

ns_id = 12
ns_label = site.namespace(ns_id) # Label local du namespace

### document.py
#   cf dernière étape exp. dpt.
##title = u'Projet:Laboratoire/Propositions/Espace_de_noms_Département/Documents'
#page = pywikibot.Page(site, title)
#gen_links = page.linkedPages(namespaces=ns_id)
#c1,c2 = 0, 0
#for link in gen_links:
  #link =  str(link)
  #resep = re.compile('/')
  #gen = re.findall(resep, link)
  ## print x
  #nb = len(gen)
  #print nb
  #if nb==1:
    #print link
    #c1 = c1+1
  #elif nb>1:
    #print  link
    #c2 = c2+1
#print c1
#print c2


print '---------'
print ns_id


gen_hlp = site.allpages(namespace=ns_id)  

label = site.namespace(ns_id)
print label
#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 14 - Category - Catégorie
### Licence CeCiLL voir Licence.txt

import pywikibot
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 14   

title = u'fr:Catégorie:Départements'
page = pywikibot.page.Category(site, title)
#articles = page.articles(recurse=True) # liste tous les articles dasn cat et subcat
articles = page.articles()
prefix = u'fr:Catégorie:'
for article in articles:
  print article
  suffix = article.title(withNamespace=False)
  title = prefix + suffix
  print title
  page = pywikibot.page.Category(site, title)
  gen = page.articles(recurse=True)
  c=0
  for g in gen:
    c=c+1
  print c
    
  

  #title = article
  #page = pywikibot.page(site, title)
  #print page.title(withNamespace=False)
#c=0
#for article in articles:
  #print article
  #c=c+1
  #print c

print page.title(withNamespace=False) # tronque le titre court
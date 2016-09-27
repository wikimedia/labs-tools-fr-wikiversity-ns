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

### Analyse le contenu de la catégorie donnée en title
#   Pour chaque page/article dans la catégorie
#   compile le titre de la catégorie homonyme
#   Calcul le nombre de pages total dans chaque catégorie de maière récursive
#
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
  # ajouter le nombre aux propriétés de la page "all_in_cat" = int
  
#for page in dict_page:
  #page_prop = dict_page[page]
  #page = str(page)
  #if page == '[[fr:Aide:Catégorie]]':
    #test = 1000000000000
    #page_prop['test'] =test

  #title = article
  #page = pywikibot.page(site, title)
  #print page.title(withNamespace=False)
#c=0
#for article in articles:
  #print article
  #c=c+1
  #print c

print page.title(withNamespace=False) # tronque le titre court
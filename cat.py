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

nsdata = ns_collect_data(ns_id) # Scan l'espace de noms collecte les données
dict_page = nsdata['dict_page'] # reconnait le dictionnaire des pages

### Collecte des propriétés des catégories
#   empty, hidden, subcat, articles, pas members(optional - test- doublon)
count = 0 # TEST visualise la progression du script
cat_mon = ['fr:Catégorie:Facultés', 'fr:Catégorie:Départements', 'fr:Catégorie:Départements de recherche', 'fr:Catégorie:Recherches par facultés']
#for page in dict_page:
  #count = count +1 
  #print count
  ##if page == 
  #page_prop = dict_page[page]
  ##page = pywikibot(site, page)
  #empty = page.isEmptyCategory()
  #hidden = page.isHiddenCategory()
  
  ##for i in cat_mon:
  ##subcat = page.subcategories()
  ##subcat = gen_to_list(subcat)
  ##page_prop['subcat'] = subcat
  ##articles = page.articles()
  ##articles = gen_to_list(articles)
  ##page_prop['articles'] = articles
  ##members = page.members()
  ##members = gen_to_list(members)
  ##page_prop['members'] = members
  #print page
  #print type(page)
  #upage = unicode(page)
  #if upage == u'[[fr:Catégorie:Accord]]':
    #print 'yyyyyyyyyyeeeeeeeeeesssssss'
  
  ##print '###'
  ##print '# MEMBERS #'
  ##gen_to_list
  ##for member in members:
    ##print member
  ##print '# SUBCAT #'
  ##for cat in subcat:
    ##print cat
  #if empty:
    #page_prop['empty'] = empty

    ##print 'VIDE'
    ##print page
  #if hidden:
    #page_prop['hidden'] = hidden
    ##print 'CACHÉ'
    ##print page
  ##print '###########'

for cat in cat_mon:
  title = unicode(cat, 'utf-8')
  page = pywikibot.page.Category(site, title)  # PWB crée un objet page_de_catégorie
  page_prop=dict_page[page]

  empty = page.isEmptyCategory()
  hidden = page.isHiddenCategory()
  subcat = page.subcategories()
  subcat = gen_to_list(subcat)
  page_prop['subcat'] = subcat
  articles = page.articles()
  articles = gen_to_list(articles)
  page_prop['articles'] = articles
  members = page.members()
  members = gen_to_list(members)
  page_prop['members'] = members
  print dict_page[page]

  

table_prop_code = wlms_table_prop(ns_id, nsdata) # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages')   # la table des pages
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code  # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 

# Notes
# class category(page)
# articles()
#     |      Yield all articles in the current category..> all pages not categories
# isEmptyCategory(self, *args, **kwargs)
#  Return True if category has no members (including subcategories).
# isHiddenCategory(self, *args, **kwargs)
#     |      Return True if the category is hidden.
# members(self, recurse=False, namespaces=None, step=None, total=None, content=False)
#     |      Yield all category contents (subcats, pages, and files).
# subcategories(*__args, **__kw)
#     |      Iterate all subcategories of the current category.
#########
# method from page
# getCategoryRedirectTarget(self)
#     |      If this is a category redirect, return the target category title.
# isCategory(self)
#            Return True if the page is a Category, False otherwise.
# isCategoryRedirect(self)
#            Return True if this is a category redirect page, False otherwise.
#########
#    Catégorie:Facultés
#    Catégorie:Départements
#    Catégorie:Départements de recherche
#    Catégorie:Recherches par facultés

## Annotations
# en collectant les boléesna empty et hidden pour chaque page (execution ligne de commande locale),
# le script dure 15 minutes
# en ajoutant les articles, subcats et membres le script dure plus de 30 min et echoue lors de la
# sauvegarde "toobigdata"
# 
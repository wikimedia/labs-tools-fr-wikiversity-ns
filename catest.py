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


def get_linked_cat(collector_file):
  title = collector_file
  page = pywikibot.Page(site, title) # objet page  PWB
  lcat = get_linked_p(page, 14)
  lcat = gen_to_list(lcat)
  return lcat
  
def count_recursive_subcats(lcat): # Compte recursif des pages dans les sous-catégories
  for cat in lcat :
    subcats = cat.subcategories()
    count_recursive(subcats)
  
def count_recursive(subcats) :
  for subcat in subcats :
    all_in_cat = subcat.articles(recurse=True)  # liste recursive de tous les articles cat et subcat
    all_in_cat = gen_to_list(all_in_cat)
    all_in_cat = len(all_in_cat)
    page_prop = dict_page[subcat]
    page_prop['all_in_cat'] = all_in_cat
    print all_in_cat

###
collector_file = u'fr:Projet:Laboratoire/Espaces de noms/Catégorie/Comptage récursif'
lcat = get_linked_cat(collector_file)
#print l
count_recursive_subcats(lcat)
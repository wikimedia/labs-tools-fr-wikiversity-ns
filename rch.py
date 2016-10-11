#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 104 Recherche
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot 

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 104   

### ETAPE 1 
nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']


### Ajoute la liste des doc de recherche au dictionnaire des pages
#   Filtre les departements de recherche
#   Collecte les liens vers ns_104 retourne la liste l_doc
for page in dict_page: # Analyse des départements de recherche
  page_prop = dict_page[page]
  l_doc = []           # Liste des documents de recherche liés à un dpt
  pref = "fr:Recherche:Département:" # prefix des departement de recherche
  # ATTENTION il faut collecter les liens sur la sous-page /Contenu
  s = str(page)
  if pref in s: #and page_prop['nsep'] == 0: # si departement de recherche
    if '/Contenu' in s:
      gen = get_linked_p(page, 104)          # collecter les liens vers ns_104
      for doc in gen :         # chaque document de recherche
	l_doc.append(doc)      # est ajouté à la liste l_doc
  page_prop['l_doc'] = l_doc # place la liste dans le dictionnaire des propriétés
  
table_prop_code = wlms_table_prop(ns_id, nsdata) # la table des propriétés de l'espace de noms
table_pages_code = wlms_table_pages(dict_page) ###TEST wlms_table_pages(nsdata)       # la table des pages
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code  # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
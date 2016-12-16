#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 102 - Projet - Projet
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 102   

### Collect data
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms
dict_page = nsdata['dict_page'] # récupère le dictionnaire des pages
# VERIFIER prefixe ou regex suivant :
prefix_list = [u'Wikiversité',] # Liste UNICODE des pages dont on souhaite collecter les dates
ns_get_date(dict_page, prefix_list, nsdata['label']) # Collecte les dates de 1ere revisio
### Write Lua table  
table_prop_code = wlms_table_prop(ns_id, nsdata) # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages')   # la table des pages
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code  # Concatener le code des tables Lua
### Save Lua module
module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
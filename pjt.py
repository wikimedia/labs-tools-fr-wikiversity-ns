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
ns_talk_id = ns_id + 1 # Identifiant espace de discussion relatif

### Collect data
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms
dict_page = nsdata['dict_page'] # récupère le dictionnaire des pages
#   Talk space
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion

prefix_list = [u'Projet:Wikiversité',] # Liste UNICODE des pages dont on souhaite collecter les dates
ns_get_date(dict_page, prefix_list, nsdata['label']) # Collecte les dates de 1ere revision

### Write Lua table  
table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # la table des pages
lua_code = table_prop_code + table_pages_code     # Concatener le code des tables Lua
module_name = u'Nsm/Table/' + str(ns_id)            # enregistre le module du namespace
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'Nsm/Table/' + str(ns_talk_id)           # enregistre le module de l'espace discussion relatif
### Save Lua module
write_module_lua(module_name, lua_code)               # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code)     # Ecriture des tables de l'espace discussion
#print lua_code                                       # TEST affiche le code du module
#print module_name
#print talk_module_name
#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms Aide de la Wikiversité francophone
### Licence CeCiLL voir Licence.txt
import pywikibot ###, re #, sys
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 12   # identifiant espace de noms Aide

### Collect data MAIN SPACE
nsdata = ns_collect_data(ns_id)       # Scan l'espace de noms VERSION 2
main_dict = nsdata['dict_page']
### Collect data DISCUSSIONS NAMESPACES
ns_talk_id = ns_id + 1 # Identifiant espace de discussion relatif
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de noms VERSION 2
talk_dict = nstalk['dict_page']       # 

### Write Lua tables
table_prop_code  = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(main_dict, 'pages')  # la table des pages
lua_main_code    = table_prop_code + table_pages_code # Concatener le code Lua
main_module_name = u'ns_' + nsdata['label']  # enregistre le module de l'espace de noms
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'ns_' + nstalk['label']  # enregistre le module de l'espace discussion relatif
#   Save Modules
write_module_lua(main_module_name, lua_main_code) # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion
#print lua_main_code                         # TEST affiche le code du module
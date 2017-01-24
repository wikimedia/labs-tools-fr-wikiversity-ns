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
ns_id = 12             # identifiant espace de noms Aide
ns_talk_id = ns_id + 1 # Identifiant espace de discussion relatif

### Collect data 
#   MAIN SPACE
nsdata = ns_collect_data(ns_id)       # Scan l'espace de noms 
main_dict = nsdata['dict_page']
#   DISCUSSIONS NAMESPACES
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion

### Write Lua tables
### wlms_table(nsid, nsdata)
table_prop_code  = wlms_table_prop(ns_id, nsdata)     # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(main_dict, 'pages')     # la table des pages
lua_main_code    = table_prop_code + table_pages_code # Concatener le code Lua
subject_module_name = u'Nsm/Table/' + str(ns_id)      # nom du module de l'espace
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'Nsm/Table/' + str(ns_talk_id)    # nom du module de l'espace discussion
#   Save Modules
write_module_lua(subject_module_name, lua_main_code)  # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code)     # Ecriture des tables de l'espace discussion
#print lua_main_code                                  # TEST affiche le code du module
#print subject_module_name
#print talk_module_name
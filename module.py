#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms Module 828
### Licence CeCiLL voir Licence.txt

import pywikibot
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 828   
ns_talk_id = ns_id + 1

### Collect namespace data 
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms collecte les données
dict_page = nsdata['dict_page'] # reconnait le dictionnaire des pages

is_doc(dict_page)   # Ajoute propriété is_doc (Vrai si est une sous-pages /Documentation) 
have_doc(dict_page) # Ajoute propriété have_doc, si vrai  ajoute own_doc (titre de la doc associée)
  
### Collect DISCUSSIONS NAMESPACE data
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de noms VERSION 2
talk_dict = nstalk['dict_page']       # 
### Write tables
table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # la table des pages
lua_code = table_prop_code + table_pages_code     # Concatener le code Lua
module_name = u'Nsm/Table/' + str(ns_id)  # enregistre le module du namespace
# Discussion's tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'Nsm/Table/' + str(ns_talk_id)  # enregistre le module de l'espace discussion relatif
# ATTENTION Le label vient avec première majuscule
### Write table's modules
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion
#print lua_code                         # TEST affiche le code du module
#print module_name
#print talk_module_name
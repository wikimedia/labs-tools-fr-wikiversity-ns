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
ns_id = 12   # identifiant namespace

#### Collect data 
#nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
#dict_page = nsdata['dict_page']

### DISCUSSIONS NAMESPACES
ns_talk_id = ns_id + 1
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de noms VERSION 2
dict_page = nstalk['dict_page']       # ATTENTION nom du dictionnaire immuable

### Write Lua tables
table_prop_code = wlms_table_prop(ns_id, nstalk)   # la table des propriétés de l'espace de noms
table_pages_code =  wlms_table(dict_page, 'talkpages') # la table des pages ATTENTION definit variable
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code      # Concatener le code Lua
### Save Module
module_name = u'ns_' + nstalk['label']   # enregistrer une table dans le module de l'espace relatif
print lua_code                           # TEST affiche le code du module
#print module_name
#print comment
#write_module_lua(module_name, lua_code) # Pas un nouveau module seulement une nlle table dans le module d'origine

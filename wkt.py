#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt
import pywikibot ###, re, sys
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 4  

### ETAPE 1 
nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']

## Collection des dates de 1ère révision
prefix_list = [u'La salle café', 
	       u'Pages à supprimer', 
	       u'Administrateur/Candidature', 
	       u'Bureaucrate/Candidature]',] # UNICODE

ns_get_date(dict_page, prefix_list, nsdata['label'])  # dates de 1ère révision
  
table_prop_code = wlms_table_prop(ns_id, nsdata) # la table des propriétés de l'espace de noms ¿ns_id?
table_pages_code = wlms_table(dict_page, 'pages')   # la table des pages
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code  # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
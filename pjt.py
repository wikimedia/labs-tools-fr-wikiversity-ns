#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re #Rev.5#, sys
from namespaceLib import *

### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)

ns_id = 102   #Rev.5
ns_label = site.namespace(ns_id) # Label local du namespace

title = u' Projet:Laboratoire/Espaces de noms/' # + Projet/

### ETAPE 1 
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)
[total, redirection, racine, sous_page, verif, dict_page, ns_id] = prop


page_prop = dict_page

lua_code = write_t_prop(ns_id, prop)  
table_code =  write_t_pages(page_prop) ### la table des propriétés de l'espace de noms
lua_code = lua_code + table_code       ### la table des pages
# Concatener le code Lua ici
lua_code = unicode(lua_code, 'utf-8')
module_name = u'ns_' + ns_label
write_module(module_name, lua_code)    ### Ecriture du module
### FIN ETAPE 1
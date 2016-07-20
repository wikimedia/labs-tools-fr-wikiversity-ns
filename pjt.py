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

### ETAPE 1 
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label] = prop
### COLLECTER LES DATE 1ere REVISION POUR	fr:Projet:Wikiversité/
lua_code = write_t_prop(ns_id, prop)   ### la table des propriétés de l'espace de noms
table_code =  write_t_pages(dict_page) ### la table des pages
table_code = unicode(table_code, 'utf_8')
lua_code = lua_code + table_code       
# Concatener le code Lua ici
#lua_code = unicode(lua_code, 'utf-8')
module_name = u'ns_' + ns_label
write_module(module_name, lua_code)    ### Ecriture du module
### FIN ETAPE 1
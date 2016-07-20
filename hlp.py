#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re #, sys
from namespaceLib import *

### Outil d'analyse et report de données sur l'espace de noms Aide de la Wikiversité francophone
### Licence CeCiLL voir Licence.txt

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

ns_id = 12   # identifiant namespace

### ETAPE 1 
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)            # Scan l'espace de noms 
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label] = prop # On a besoin uniquement de dict_page
# ajouter ns_label à la liste (ou tuple) des prop.
prop_code = write_t_prop(ns_id, prop)   # la table des propriétés de l'espace de noms
table_code =  write_t_pages(dict_page)  # la table des pages
table_code = unicode(table_code, 'utf-8') 
# Concatener le code Lua ici
lua_code = prop_code + table_code       
#lua_code = unicode(lua_code, 'utf-8')   # convertit le texte du module en Unicode
module_name = u'ns_' + ns_label         # enregistre le module du namespace
write_module(module_name, lua_code)     # Ecriture du module #TEST 
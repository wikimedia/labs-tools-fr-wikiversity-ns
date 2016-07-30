#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot ###, re #, sys
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
prop.append(lang) 
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop # On a besoin uniquement de dict_page
prop_code = write_t_prop(ns_id, prop)   # la table des propriétés de l'espace de noms
table_code =  write_t_pages(dict_page)  # la table des pages
# Concatener le code Lua ici
lua_code = prop_code + table_code       
module_name = u'ns_' + ns_label         # enregistre le module du namespace
# print lua_code                        # TEST
write_module(module_name, lua_code)     # Ecriture du module #TEST 
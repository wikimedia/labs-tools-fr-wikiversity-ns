#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re, sys
from namespaceLib import *

### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

ns_id = 104   #Rev.5
ns_label = site.namespace(ns_id) # Label local du namespace

### ETAPE 1 
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
prop.append(lang)                # ajoute le code langue pour former le préfixe des filtres
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop
### Lister les pages Recherche:Département analyser les sous-pages ~/Contenu
lua_code = write_t_prop(ns_id, prop)  
table_code =  write_t_pages(dict_page) ### la table des propriétés de l'espace de noms
lua_code = lua_code + table_code       ### la table des pages
# Concatener le code Lua ici
#lua_code = unicode(lua_code, 'utf-8')
module_name = u'ns_' + ns_label
write_module(module_name, lua_code)    ### Ecriture du module
### FIN ETAPE 1
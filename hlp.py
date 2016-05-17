#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re #, sys
from namespaceLib import *
### Outil d'analyse et report de données sur l'espace de noms Aide de la Wikiversité francophone
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

ns_id = 12   #Rev.5
ns_label = site.namespace(ns_id) # Label local du namespace
title = u' Projet:Laboratoire/Espaces de noms/' # Chemin de base pour les listes Python

prop = ns_prop(ns_id)
[c, c_redir, c_racine, c1,c2, c3, verif, dict_page, ns_id] = prop

print prop[0]
print prop[1]
print prop[2]
print prop[3]
print prop[4]
print prop[5]
print '-----'
print prop[6] 

page_prop = dict_page             # Toute les pages et leur propriétés
lua_code = write_t_prop(ns_id, prop)  
table_code =  write_t_pages(page_prop)
lua_code = lua_code + table_code
# Concatener le code Lua ici

lua_code = unicode(lua_code, 'utf-8')
print lua_code ### TEST
module_name = u'ns_' + ns_label
write_module(module_name, lua_code) ### ATTENTION

#dict_racine = get_root(dict_page)
#witxt = write_list_root(dict_racine)
#title = title + 'Liste des pages'
#comment = u'Ecrit la liste des pages racines de l\'espace de noms avec le nombre sous-pages - https://tools.wmflabs.org/fr-wikiversity-ns'
#witxt = witxt + u'[[Catégorie:Laboratoire]]'
##print witxt # TEST
#page = pywikibot.Page(site, title)
#page.text = witxt
#page.save(comment)  # ATTENTION
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

prop = ns_prop(ns_id)
[c, c_redir, c_racine, c1,c2, c3, verif, dict_page, ns_id] = prop #Rev.5
print ns_id # ns_id
print c # total page VARNAME
print c_redir # Redirections
print prop[2] # root pages
print prop[3] # sub-peges lev.1
print prop[4] # sub-pages lev.2
print prop[5] # sub-pages more level
print '-----'
print prop[6] # Verif

page_prop = dict_page             # Toute les pages et leur propriétés

dict_racine = get_root(dict_page) # Uniquement les pages root avec leur sous-page

#witxt = write_list_root(dict_racine)
#print witxt  # TEST
#title = title + ns_label + '/Liste des pages'
#comment = u'Ecrit la liste des pages racines de l\'espace de noms avec le nombre de sous-pages- youni_verciti_bot'
#witxt = witxt + u'[[Catégorie:Laboratoire]]'
#page = pywikibot.Page(site, title)
#page.text = witxt
#page.save(comment)  # ATTENTION

lua_code = write_t_prop(ns_id, prop)  
table_code =  write_t_pages(page_prop)
lua_code = lua_code + table_code
# Concatener le code Lua ici
lua_code = unicode(lua_code, 'utf-8')
module_name = u'ns_' + ns_label
write_module(module_name, lua_code)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
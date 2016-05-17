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

### write_module() écrit un module vide
#
def write_module(module_name, lua_code): # Compiler tout le code du module au préalabe
  title = u'Module:'
  # UNICODE
  title = title + module_name
  comment = u'Nouveau module ajouté par l\'outil fr-wikiversity-ns sur tools.labs.org'
  module = 'local p = {}\n'
  module = module + lua_code
  module = module + '\nreturn p'
  page = pywikibot.Page(site, title)
  page.text = module
  page.save(comment) # TRY
  

### write_t_prop() écrit la table des propriétés de l'espace de noms
#   retourne une table au format clé = valeur
# 
def write_t_prop():
  t = 'p.t' + str(ns_id) + '_prop = {'
  t = t + 'total = ' + str(c)  + ', '
  t = t + 'nb_redir = ' + str(c_redir) + ', '
  t = t + 'nb_racine = ' + str(c_racine) + ', '
  t = t + 'c1 = ' + str(c1) + ', '
  t = t + 'c2 = ' + str(c2) + ', '
  t = t + 'c3 = ' + str(c3) + ', '
  t = t + '}\n'
  return t

lua_code = write_t_prop()  
# Concatener le code Lua ici
module_name = u'ns_' + ns_label
write_module(module_name, lua_code)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
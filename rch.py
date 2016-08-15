#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot ###, re, sys
from namespaceLib import *

### Outil d'analyse et report de données sur l'espace de noms numero 104 Recherche
### Licence CeCiLL voir Licence.txt

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 104   #Rev.5

### ETAPE 1 
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
prop.append(lang)                # ajoute le code langue pour former le préfixe des filtres
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop

### Lister les pages Recherche:Département analyser les sous-pages ~/Contenu
lua_code = write_t_prop(ns_id, prop)  ### la table des propriétés de l'espace de noms

### FIN ETAPE 1
total_tr = 0
for page in dict_page: # Analyse des départements de recherche
  page_prop = dict_page[page]
  l_doc = []           # Liste des documents d erecherche liés à un dpt
  pref = "fr:Recherche:Département:"  # prefix des departement de recherche
  s = str(page)
  rdpt_tr = 0
  if pref in s and page_prop[0] == 0: # si departement de recherche
    print page
    gen = get_linked_p(page, 104)   # collecter les liens vers ns_104
    for doc in gen :        # chaque document de recherche
      l_doc.append(doc)     # est ajouté à la liste l_doc
      total_tr = total_tr+1 #TEST
      rdpt_tr=rdpt_tr+1     #TEST
      print doc             #TEST
    print rdpt_tr           #TEST
  page_prop.append(l_doc)   # Ajoute la liste des doc de recherche à celle des prop de la page
  #print type(page_prop[1])
  d_prop = {}
  d_prop['nsep'] = page_prop[0]
  d_prop['date1'] = page_prop[1]
  d_prop['cible'] = page_prop[2]
  d_prop['l_doc'] = page_prop[3]
  dict_page[page] = d_prop

table_code =  w_t_pages(dict_page)    ### la table des pages
lua_code = lua_code + table_code       
# Concatener le code Lua ici
module_name = u'ns_' + ns_label
print total_tr
#print lua_code
write_module(module_name, lua_code)    ### TEST Ecriture du module


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
prop = ns_prop(ns_id)   # Scan l'espace de noms renvoi liste de propriétés contenant dictionnaire de pages
prop.append(ns_label)   # ajoute le label local de l'espace à la liste des propriétés
prop.append(lang)       # prefix fr:
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop
### COLLECTER LES DATE 1ere REVISION POUR	fr:Projet:Wikiversité/
get_date_for = [u'Wikiversité',] # UNICODE
for page in dict_page:
  name = unicode(page)
  page_prop = dict_page[page]        # déclare la liste de propriétés de la page
  [nb_sep, date, cible] = page_prop
  # La liste des pages dont on souhaite collecter la date de creation
  for groupe in get_date_for:
    groupe = prefix(groupe, lang, ns_label)
  for groupe in get_date_for:
    if unicode(groupe) in name:
      first_rev = page.oldest_revision # genère un tuple contenant les info. de la première revision
      get_date = first_rev.timestamp   # copie la valeur date et heure de création
      page_prop[1] = get_date          # place la date dans la liste à l'indice correspondant
### DATES FIN
lua_code = write_t_prop(ns_id, prop)   ### la table des propriétés de l'espace de noms
table_code =  write_t_pages(dict_page) ### la table des pages
lua_code = lua_code + table_code       
# Concatener le code Lua ici
module_name = u'ns_' + ns_label
#print lua_code #TEST
write_module(module_name, lua_code)    #TEST Ecriture du module
### FIN ETAPE 1
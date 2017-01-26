#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt
import pywikibot ###, re, sys
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 4  
ns_talk_id = ns_id + 1 # Identifiant espace de discussion relatif

### Collecte données espace Wikiversité
nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']
### PLACER DANS PROJET l_plan est rleatif à une page de l'espace projet !
#   Projet:Laboratoire/Espaces de noms/Wikiversité/Plan 
#   Collecter les liens depuis cette page vers ns_4 et retourner la propriété l_plan
# title = u'Projet:Laboratoire/Espaces de noms/Wikiversité/Plan'
# page  = pywikibot.Page(site, title) # Créé un objet page PWB
###

#   Collecte données espace Discussion wikiversité
nstalk = ns_collect_data(ns_talk_id)      # Scan l'espace de discussion
talk_dict = nstalk['dict_page']           # Dictionnaire des pages de discussion

## Collection des dates de 1ère révision
prefix_list = [u'La salle café', 
	       u'Pages à supprimer', 
	       u'Administrateur/Candidature', 
	       u'Bureaucrate/Candidature]',] # UNICODE
ns_get_date(dict_page, prefix_list, nsdata['label'])  # dates de 1ère révision

### Composition des tables Wikitexte
table_prop_code = wlms_table_prop(ns_id, nsdata)      # la table des propriétés de l'espace de noms ¿ns_id?
table_pages_code = wlms_table(dict_page, 'pages')     # la table des pages
lua_code = table_prop_code + table_pages_code         # Concatener le code Lua
module_name = u'Nsm/Table/' + str(ns_id)              # enregistre le module du namespace
#   Espace discussion
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'Nsm/Table/' + str(ns_talk_id)    # enregistre le module de l'espace discussion relatif
### Sauvegarde modules
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code)     # Ecriture des tables de l'espace discussion
#print lua_code                                       # TEST affiche le code du module
#print module_name
#print talk_module_name
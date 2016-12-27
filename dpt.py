#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 108 - Département - Départementt
### Licence CeCiLL voir Licence.txt
import pywikibot ###, re, sys
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 108            # NAMESPACE ID
ns_talk_id = ns_id + 1 # Identifiant espace de discussion relatif

### Collecte données  
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page'] # récupère le dictionnaire des pages
#   Espace discussion
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion

# POURQUOI UNIQUEMENT ICI ? Liste des sous-pages pour les départements 'lsp'
splited_dicts = split_root(dict_page)       # Ajouter option split_root(dict_pages, opt[,|sub|both])
dict_root_sub = get_sub_list(splited_dicts) # Ajoute la liste des sous-pages aux propriétés des pages racines

### Determine le nombre de liens par themes par niveaux
#   Verifie si la page existe le nombre de leçons
#   Ajoute un dictionnaire d_lesson contenant les listes : 
#   l_theme, l_niveaux, l_add, all_lessons, l_exist

for p in dict_root_sub: # A VERIFIER bcp de code
  d_lesson = {}                     # Initialise un dictionnaire pour les stats sur les leçons
  page_prop = dict_root_sub[p]      # p
  [niveau, date1, cible, lsp] = page_prop #??? VERIFIER 
  theme   = check_link_in_subpage(p, '/Leçons par thèmes', 0)
  niveau  = check_link_in_subpage(p, '/Leçons par niveaux', 0)
  rch_out = check_link_in_subpage(p, '/Leçons par thèmes', 104)
  l_rch   = check_link_in_subpage(p, '/Travaux de recherche', 104)
  f_niveau = []          # pour filtrer les doublons qui ne sont pas déjà dans la sous-page Leçons par thèmes
  for lesson in niveau:  # de la sous-page Leçons par niveaux
    if lesson in theme:  # 
      pass
    else:
      f_niveau.append(lesson)    # ajoute la lesson à la liste filtrée
  all_lessons = theme + f_niveau # La somme des liens apres fiiltrage doublons
  lesson_exist = []              # Liste des liens dont la page existe après test
  for page in all_lessons:
    exist = page.exists()        # Si la page existe
    if exist:
      lesson_exist.append(page) # place le lien dans la liste
    else:
      pass
  d_lesson['l_theme']  = theme          # les stats des leçons dans un dictionnaire
  d_lesson['n_theme']  = len(theme)
  d_lesson['l_niveau'] = niveau
  d_lesson['n_niveau'] = len(niveau)
  d_lesson['l_add']    = f_niveau	# Liste liens Uniquement depuis Leçons par niveaux
  d_lesson['n_add']    = len(f_niveau)	# Nombre de liens Uniquement depuis Leçons par niveaux
  d_lesson['all_lessons'] = all_lessons # ajoute la liste des leçons fusionnée RENOMMER l_lessons
  d_lesson['n_lessons'] = len(all_lessons)
  d_lesson['l_exist']   = lesson_exist	# Liste des liens vers espace principal
  d_lesson['n_exist']   = len(lesson_exist)
  d_lesson['rch_out']   = rch_out	# Liste des liens recherche mal placés
  d_lesson['n_rch_out']	= len(rch_out)
  d_lesson['l_rch']     = l_rch		# Liste des liens vers travaux de recherche
  d_lesson['n_rch']	= len(l_rch)    # Ajout du nombre de travaux de recherche
  page_prop['d_lesson'] = d_lesson      # Ajout du dictionnaire des leçons RENOMMER D_LINKS
  dict_root_sub[p]      = page_prop     # Actualise les propriétes de la page???

table_prop_code = wlms_table_prop(ns_id, nsdata)  # Écrit la table Lua des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # Écrit la table Lua des pages de l'espace de noms
lua_code = table_prop_code + table_pages_code     # Concatener le code Lua
module_name = u'ns_' + nsdata['label']            # enregistre le module du namespace
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'ns_' + nstalk['label']           # enregistre le module de l'espace discussion relatif
### Sauvegarde des modules
write_module_lua(module_name, lua_code)           # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion
#print lua_code                                   # TEST affiche le code du module

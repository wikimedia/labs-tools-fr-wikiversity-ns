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
ns_id = 108  # NAMESPACE ID

### ETAPE 1 
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page'] # récupère le dictionnaire des pages

### Determine le nombre de liens par themes par niveaux
#   Verifie si la page existe le nombre de leçons
#   Ajoute un dictionnaire d_lesson contenant les listes : 
#   l_theme, l_niveaux, l_add, all_lessons, l_exist
merged = merge_sub2(dict_page)    # merge_sub2 RENOMMER
dict_root_sub = root_sub2(merged) # Ajoute la liste des sous-pages aux propriétés des pages racines
for p in dict_root_sub: # A VERIFIER bcp de code
  d_lesson = {}                     # Initialise un dictionnaire pour les stats sur les leçons
  page_prop = dict_root_sub[p]      # p
  [niveau, date1, cible, lsp] = page_prop #??? VERIFIER 
  theme = check_link_in_subpage(p, '/Leçons par thèmes', 0)
  niveau = check_link_in_subpage(p, '/Leçons par niveaux', 0)
  rch_out = check_link_in_subpage(p, '/Leçons par thèmes', 104)
  l_rch   = check_link_in_subpage(p, '/Travaux de recherche', 104)
  f_niveau = []          # pour filtrer les doublons qui ne sont pas déjà dans la sous-page Leçons par thèmes
  for lesson in niveau:  # de la sous-page Leçons par niveaux
    if lesson in theme:  # 
      pass
    else:
      f_niveau.append(lesson)   # ajoute la lesson à la liste filtrée
  all_lessons = theme + f_niveau
  lesson_exist = []        # Liste des liens dont la page existe
  for page in all_lessons:
    exist = page.exists()       # Si la page existe
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

table_prop_code = wlms_table_prop(ns_id, nsdata) # Écrit la table Lua des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages')   # Écrit la table Lua des pages de l'espace de noms
# ATTENTION wlms_table_pages 
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code    # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 


#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot ###, re, sys
from namespace_lib import *
from lua_mw_lib import *

### Outil d'analyse et report de données sur l'espace de noms numero 108 - Département - Départementt
### Licence CeCiLL voir Licence.txt
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 108  # NAMESPACE ID

### CHK SUB FOR LNK --- AMELIORER
#   Cherche les liens dans les sous-pages
def check_lessons_in_sp(page, string):
  sp = str(page)
  sp = sp[2:-2] + string
  title = unicode(sp, 'utf-8')
  page = pywikibot.Page(site, title)
  exist = page.exists()
  if exist:
    gen = get_linked_p(page, 0) # titre de la page et namespace id
  else:
    gen = []
  return gen

### ETAPE 1 
nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']

merged = merge_sub2(dict_page)
[dict_racine, dict_sub] = merged
dict_root_sub = root_sub2(merged)

for p in dict_root_sub: # A VERIFIER bcp de code
  d_lesson = {}
  page_prop = dict_root_sub[p]
  [niveau, date1, cible, lsp] = page_prop
  gen_theme = check_lessons_in_sp(p, '/Leçons par thèmes')
  gen_niveau = check_lessons_in_sp(p, '/Leçons par niveaux')
  l_theme, l_niveau = [], []                     # 
  for lesson in gen_theme:
    l_theme.append(lesson)
  for lesson in gen_niveau:
    l_niveau.append(lesson)   
  f_niveau = []            # pour filtrer les doublons qui ne sont pas déjà dans la sous-page Leçons par thèmes
  for lesson in l_niveau:  # de la sous-page Leçons par niveaux
    if lesson in l_theme:  # 
      pass
    else:
      f_niveau.append(lesson)       # ajoute la lesson à la liste filtrée
  all_lessons = l_theme + f_niveau
  lesson_exist = []
  for page in all_lessons:
    exist = page.exists()       # Si la page existe
    if exist:
      lesson_exist.append(page) # Liste des Liens existants
    else:
      pass
  d_lesson['l_theme'] = l_theme # les stats des leçons dans un dictionnaire
  d_lesson['l_niveau'] = l_niveau
  d_lesson['l_add'] = f_niveau
  d_lesson['all_lessons'] = all_lessons # ajoute la liste des leçons fusionnée
  d_lesson['l_exist'] = lesson_exist
  #if len(lesson_exist) == 0: # Liste des départements vides pour dates à collecter
  #  dpt_vide =               # Copier dans un dict pour ajout des dates
  page_prop['d_lesson'] = d_lesson   # Ajout du dictionnaire des leçons
  dict_root_sub[p] = page_prop       # Actualise les propriétes de la page

table_prop_code = wlms_table_prop(ns_id, nsdata) # la table des propriétés de l'espace de noms ¿ns_id?
table_pages_code = wlms_table_pages(dict_page)   ###TEST wlms_table_pages(nsdata)       # la table des pages
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code    # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
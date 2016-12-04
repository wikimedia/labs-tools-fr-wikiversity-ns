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
  #theme = check_lessons_in_sp(p, '/Leçons par thèmes', 0)  # place les liens dans generateur 
  niveau = check_link_in_subpage(p, '/Leçons par niveaux', 0)
  #niveau = check_lessons_in_sp(p, '/Leçons par niveaux', 0)
  rch_out = check_link_in_subpage(p, '/Leçons par thèmes', 104)
  #rch_out = check_lessons_in_sp(p, '/Leçons par thèmes', 104)
  l_rch   = check_link_in_subpage(p, '/Travaux de recherche', 104)
  #l_rch   = check_lessons_in_sp(p, '/Travaux de recherche', 104)
  #theme   = gen_to_list(theme)
  #niveau  = gen_to_list(niveau)
  #rch_out = gen_to_list(rch_out)
  #l_rch   = gen_to_list(l_rch)
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
  d_lesson['l_niveau'] = niveau
  d_lesson['l_add']    = f_niveau
  d_lesson['all_lessons'] = all_lessons # ajoute la liste des leçons fusionnée
  d_lesson['l_exist']   = lesson_exist
  d_lesson['rch_out']   = rch_out
  d_lesson['l_rch']     = l_rch
  page_prop['d_lesson'] = d_lesson      # Ajout du dictionnaire des leçons
  dict_root_sub[p]      = page_prop     # Actualise les propriétes de la page???

table_prop_code = wlms_table_prop(ns_id, nsdata) # Écrit la table Lua des propriétés de l'espace de noms
table_pages_code = wlms_table_pages(dict_page)   # Écrit la table Lua des pages de l'espace de noms
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code    # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
print lua_code                         # TEST affiche le code du module
# write_module_lua(module_name, lua_code) # Ecriture du module #TEST 

#### CHK SUB FOR LNK --- AMELIORER
##   Cherche les liens dans les sous-pages 
##   /Leçons par thèmes & niveaux
## AJOUTER argument pour l'espace de destination (0 principal, 104 Rch)
#def check_lessons_in_sp(page, string, nsid): # string contient le nom de la sous-page
  #sp = str(page)               # Convertit en string
  #sp = sp[2:-2] + string       # ajoute les crochets
  #title = unicode(sp, 'utf-8') # Convertit en unicode
  #page = pywikibot.Page(site, title) # Créé un objet page PWB 
  #exist = page.exists()              # Test si la page existe
  #if exist:
    #gen = get_linked_p(page, nsid) # titre de la page et namespace id RECUPERER le numero en argument
  #else: # La page n'existe pas!
    #gen = [] #???
  #return gen # retourner une LISTE de préférence
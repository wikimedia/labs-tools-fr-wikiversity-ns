#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licence CeCILL compatible Gnu-Gpl (License.txt)

### Liste les pages de l'espace de nom "Département" nº 108 
#   Verifie si redirection et cherche la cible
#   Liste les sous-pages. les liens dans leçons par thèmes et leçons par niveaux
#   Compare les deux listes de liens et les fusionnent
#   Verifie si les pages derrière les liens existent
### Compare le nombre de page d'interface et le nombre de leçons du département

import pywikibot
from namespaceLib import *

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

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

ns_id = 108  # NAMESPACE ID
ns_label = site.namespace(ns_id) # Label local du namespace

### ETAPE 1 
#   
prop = ns_prop(ns_id)
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
prop.append(lang)                # ajoute le code langue pour former le préfixe des filtres
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop
### La date d’importation via l’historique avec le résumé suivant: (00 révisions importées depuis…

merged = merge_sub(dict_page)
[dict_racine, dict_sub] = merged
dict_root_sub = root_sub(merged)

for p in dict_root_sub:
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
  page_prop.append(d_lesson)    # Ajout du dictionnaire des leçons
  dict_root_sub[p] = page_prop  # Actualise les propriétes de la page

# Affecte des valeurs nulles aux sous-pages
for page in dict_sub:        # les propriétes des sous-pages doivent correspondre à celles des departements 
  page_prop = dict_sub[page] # Les valeurs de sub_dict sont mises à jour dans dict_page
  page_prop.append(lsp)
  l_theme, l_niveau, l_add, all_lessons, l_exist = [], [], [], [], [] # on place des liste vides
  d_lesson['l_theme'] = l_theme #
  d_lesson['l_niveau'] = l_niveau
  d_lesson['l_add'] = f_niveau
  d_lesson['all_lessons'] = all_lessons
  d_lesson['l_exist'] = lesson_exist
  page_prop.append(d_lesson)
  dict_sub[page] = page_prop # met à jour les propriétés dans sub_dict (lié à dict_page)


### Verifier les catégories avec Lua?

lua_code = write_t_prop(ns_id, prop)   # la table des propriétés de l'espace de noms
table_code =  write_dpt(dict_page)     # la table des pages
# Concatener le code Lua ici           # ATTENTION Ajouter les dates et utilisateur pour départe
lua_code = lua_code + table_code       
module_name = u'ns_' + ns_label        # Nom du module contment videenant le code des tables Lua
print lua_code
write_module(module_name, lua_code)    ### Ecriture du module



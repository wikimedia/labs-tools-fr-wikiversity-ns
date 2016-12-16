#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 104 Recherche
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot 

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 104   

### FONCTIONS NS 104

### Liste des documents de recherche liés dans la sous-page "/Contenu"
#   Charger la liste des pages à analyser via celle des articles dans la catégorie Laboratoire de recherche
def find_content(page): # reçoit un objet page retourne l'objet sous-page/Contenu
  spage = str(page)
  content = spage[2:-2] + '/Contenu'
  title = unicode(content, 'utf-8')
  page = pywikibot.Page(site, title)
  return page
  
def rch_labo():
  category_title = u'fr:Catégorie:Laboratoire de recherche' # à partir de la catégorie
  page = pywikibot.page.Category(site, category_title)      # créé la l'objet page.cat PWB
  articles = page.articles()       # collecte liste des articles de la catégorie
  articles = list(articles) # MIEUX : articles = list(articles)
  for article in articles:  # chaque article de la catégorie
    page = find_content(article) # objet page pour la sous-page Contenu
    exist = page.exists()        # test si trouve /Contenu
    if exist: 
      gen = get_linked_p(page, 104) # collecte les liens sur cette page vers ns Recherche
      l_gen = list(gen)        # MIEUX convertit le gen en liste
      for mypage in dict_page: # 
	if mypage == article:
	  page_prop = dict_page[mypage]
	  page_prop['l_doc'] = l_gen   # place la liste dans le dictionnaire des propriétés
	  page_prop['class_doc'] = '\'lab\'' # NOUVELLE VARIABLE
      # ATTENTION les liens sont sur la sous-page /Contenu mais nous les affectons aux propriétés
      # de la page du departement (page supérieure ou racine)
  return dict_page

### ETAPE 1 
nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']


### Ajoute la liste des doc de recherche au dictionnaire des pages
#   Filtre les departements de recherche
### Collecte les liens vers ns_104 retourne la liste l_doc
for page in dict_page:  # Analyse des départements de recherche
  page_prop = dict_page[page]
  prefix = "fr:Recherche:Département:" # prefix des departement de recherche
  s = str(page)
  if prefix in s and page_prop['nsep'] == 0: # si departement de recherche
    subp = find_content(page) # Objet pour la sous-page "/Contenu"
    exist = subp.exists()     # test si trouve /Contenu
    if exist:
      gen = get_linked_p(subp, 104) # titre de la page et namespace id
      l_gen = list(gen)
      page_prop['class_doc'] = '\'dptr\'' # NOUVELLE VARIABLE
      page_prop['l_doc'] = l_gen            # place la liste dans le dictionnaire des propriétés
  #ATTENTION les liens sont sur la sous-page /Contenu 

dict_page = rch_labo()

table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # TEST wlms_table() 
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code  # Concatener le code Lua

module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
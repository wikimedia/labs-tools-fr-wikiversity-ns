#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 14 - Category - Catégorie
### Licence CeCiLL voir Licence.txt
import pywikibot
from namespace_lib import *
from lua_mw_lib import *


def get_linked_cat(collector_file):  # Reçoit le titre du formulaire d'inscription
  title = collector_file
  page = pywikibot.Page(site, title) # objet page  PWB
  gen_cat = get_linked_p(page, 14)   # GEN
  return gen_cat   # Retourne un generateur contenant la liste des catégories à superviser

def get_members(collected_cat) :
  for page in collected_cat:
    page_prop = dict_page[page]  # propriétés de la page
    subcats = page.subcategories() # PWB generateur de sous-catégories
    subcats = list(subcats)	   # conversion en liste
    page_prop['subcats'] = subcats # ATTENTION var name articles, subcat(s)
    articles = page.articles()     # PWB generateur des articles
    articles = list(articles)      # conversion en liste
    page_prop['articles'] = articles

def get_subcats_in(gen_cat): # Retourne gen subcats pour chaque cat in collected
  all_subcats = []           # Une liste contenant des generators
  for cat in gen_cat :       # Retourne le generateur de sous-cat pour chaque categorie inscrite
    gsub = cat.subcategories()
    all_subcats.append(gsub)
  return all_subcats
  
def count_recursive(all_sub) : # reçoit une liste de generateurs
  #test = {}  # DEBUG Tuple test pour filtrer le résultat
  for gen in all_sub :
    for page in gen :
      #print str(page) ## CATEGORIE FACULTé
      c_recursive(page)
      #test[page] = page_prop
  #return test
  
def c_recursive(page) :
  gen_all = page.articles(recurse=True)  # liste recursive de tous les articles cat et subcat
  all_in_list = list(gen_all)   ###ATTENTION Processus très long
  all_in_cat = len(all_in_list)
  page_prop = dict_page[page]
  page_prop['all_in_cat'] = all_in_cat
  #print page_prop['all_in_cat']
  
### Construit la liste des catégories éponymes, à partir de la liste des articles dans la catégorie
#   Permet de grouper les catégories des departements (& facultés)
#   Teste si la catégorie existe et retourne une liste de catégories éponymes
def cat_eponyme(cat_title) :
  title = cat_title         # Objet titre pour la catégorie
  page = pywikibot.page.Category(site, title) # objet page PWB
  articles = page.articles()                  # génère la liste des articles
  prefix = u'fr:Catégorie:' # determine le prefix pour la catégorie homonyme
  l_rcat = []
  for article in articles:  # pour chaque article contenu dans la catégorie         
    #print article
    suffix = article.title(withNamespace=False) # Tronque le titre court de l'article
    title = prefix + suffix                     # Compile le titre complet de la categorie eponyme
    page = pywikibot.page.Category(site, title) # crée un objet page pour la catégorie éponyme
    exist = page.exists()             		# Test si la page existe
    if exist:
      l_rcat.append(page)			# Ajoute la catégorie éponyme à la liste
  return l_rcat


lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 14   
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms collecte les données
dict_page = nsdata['dict_page'] # reconnait le dictionnaire des pages

### Collecte unitaire
cat_members = u'Projet:Laboratoire/Espaces de noms/Catégorie/Collecte'
gen_cats = get_linked_cat(cat_members)
get_members(gen_cats)

### Collecte sous-catégories
subcats_members = u'Projet:Laboratoire/Espaces de noms/Catégorie/Collecte sous-catégories'
gen_subcats = get_linked_cat(subcats_members)
l_subcats = get_subcats_in(gen_subcats)
for gen in l_subcats :
  get_members(gen)

### Comptage récursif 
r_count = u'fr:Projet:Laboratoire/Espaces de noms/Catégorie/Comptage récursif'
# ATTENTION vérifier le comptage récursif pour Géologie et Géographie

### Comptage récursif sous catégories
r_count_subp = u'fr:Projet:Laboratoire/Espaces de noms/Catégorie/Comptage récursif sous catégories'
lcat = get_linked_cat(r_count_subp)
all_sub = get_subcats_in(lcat)
count_recursive(all_sub) #

##  Les catégories des départements ne sont pas groupées
l_rcat = cat_eponyme(u'fr:Catégorie:Départements')
for page in l_rcat :
  c_recursive(page)
  
### FIN collecte data

table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # la table des pages
lua_code = table_prop_code + table_pages_code
# Concatener le code Lua ici
module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 

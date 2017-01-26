#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 14 - Category - Catégorie
### Licence CeCiLL voir Licence.txt
import pywikibot
from namespace_lib import *
from lua_mw_lib import *

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 14 
ns_talk_id = ns_id + 1 # Identifiant de l'espace de discussion

def get_linked_cat(collector_file):  # Reçoit le titre du formulaire d'inscription
  title = collector_file             # 
  page = pywikibot.Page(site, title) # objet page  PWB
  gen_cat = get_linked_p(page, 14)   # GEN liens vers l'espace cat sur le formulaire
  return gen_cat   # Retourne un generateur contenant la liste des catégories à superviser

# ATTENTION màj
def get_members(collected_cat) : # Reçoit un generateur contenant les catégories
  for page in collected_cat:     # pour chaque catégorie
    subcats  = page.subcategories() # PWB generateur de sous-catégories
    articles = page.articles()      # PWB generateur des articles
    subcats  = list(subcats)	    # conversion en liste
    articles = list(articles)       # conversion en liste
    page_prop = dict_page[page]     # propriétés de la page
    page_prop['subcats']  = subcats  # Enregistre liste des sous-cat dans le dictionnaire
    page_prop['articles'] = articles # Enregistre liste des articles dans le dictionnaire

def get_subcats_in(gen_cat): # Retourne gen subcats pour chaque cat in collected
  all_subcats = []           # Une liste contenant des generators
  for cat in gen_cat :       # Retourne le generateur de sous-cat pour chaque categorie inscrite
    gsub = cat.subcategories() # Gen Pwb sous-catégories
    all_subcats.append(gsub)   # Ajoute dans la liste globale
  return all_subcats           # Retourne toutes les sous-catégories compilées dans une liste
  
def count_recursive(all_sub) : # reçoit une liste de generateurs
  for gen in all_sub : # Pour chaque Generateur
    for page in gen :    # Itération des catégories dans le génerateur
      c_recursive(page)  #  Appel sous-fonction qui retourne le total dans 'all_in_cat'
  
def c_recursive(page) : # Reçoit page categorie ; Compte recursif et ajoute le total dans 'all_in_cat'
  gen_all = page.articles(recurse=True)  # liste recursive de tous les articles cat et subcat
  all_in_list = list(gen_all)   ###ATTENTION Processus très long
  all_in_cat = len(all_in_list)
  page_prop = dict_page[page]
  page_prop['all_in_cat'] = all_in_cat
  #print page_prop['all_in_cat']
  
### Construit la liste des catégories éponymes, à partir de la liste des articles dans la catégorie
#   Permet de grouper les catégories des departements (& facultés)
#   Test si la catégorie existe et retourne la liste des catégories éponymes
def cat_eponyme(cat_title) :
  title = cat_title         # Objet titre pour la catégorie
  page = pywikibot.page.Category(site, title) # objet page PWB
  articles = page.articles()                  # génère la liste des articles
  prefix = u'fr:Catégorie:' # determine le prefix pour la catégorie homonyme
  l_cat_epo = []
  for article in articles:  # pour chaque article contenu dans la catégorie         
    #print article
    suffix = article.title(withNamespace=False) # Tronque le titre court de l'article
    title = prefix + suffix                     # Compile le titre complet de la categorie eponyme
    page = pywikibot.page.Category(site, title) # crée un objet page pour la catégorie éponyme
    exist = page.exists()             		# Test si la page existe
    if exist:
      l_cat_epo.append(page)			# Ajoute la catégorie éponyme à la liste
  return l_cat_epo

### Collect namespace's data
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms collecte les données
dict_page = nsdata['dict_page'] # reconnait le dictionnaire des pages
#   Collect talkpages data
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion

### COLLECT CATEGORY MEMBERS
cat_members     = u'Projet:Laboratoire/Espaces de noms/Catégorie/Collecte'
subcats_members = u'Projet:Laboratoire/Espaces de noms/Catégorie/Collecte sous-catégories'
r_count         = u'Projet:Laboratoire/Espaces de noms/Catégorie/Comptage récursif'
r_count_subp    = u'Projet:Laboratoire/Espaces de noms/Catégorie/Comptage récursif sous catégories'
#   UNITAIRE
gen_cats = get_linked_cat(cat_members)
get_members(gen_cats)
#   SOUS-CATÉGORIES
gen_subcats = get_linked_cat(subcats_members)
l_subcats = get_subcats_in(gen_subcats)
for gen in l_subcats :
  get_members(gen)
#   COMPTAGE RÉCURSIF 
#   ATTENTION vérifier le comptage récursif pour Géologie et Géographie
#gen_cat = get_linked_cat(r_count)
#for cat in gen_cat :
  #c_recursive(cat) #
#   COMPTAGE RÉCURSIF SOUS CATÉGORIES
lcat = get_linked_cat(r_count_subp)
all_sub = get_subcats_in(lcat)
count_recursive(all_sub) #

##  Les catégories des départements ne sont pas groupées donc pas inscrites
l_cat_epo = cat_eponyme(u'fr:Catégorie:Départements') # Collecte des catégories éponymes
for page in l_cat_epo : # Pour chaque catégorie éponyme
  c_recursive(page)     # Comptage recursif
  
### Ecriture du code Lua pour les tables
table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # la table des pages
lua_code = table_prop_code + table_pages_code     # Concatener le code Lua ici
module_name = u'Nsm/Table/' + str(ns_id)          # Nom du module
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code des tables
talk_module_name = u'Nsm/Table/' + str(ns_talk_id)    # Nom du module pour l'espace discussion relatif
### Enregistrement des modules
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion
#print lua_code                         # TEST affiche le code du module
#print module_name
#print talk_module_name

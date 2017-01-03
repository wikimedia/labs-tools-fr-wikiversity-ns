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

r_count         = u'Projet:Laboratoire/Espaces de noms/Catégorie/Comptage récursif'

def get_linked_cat(collector_file):  # Reçoit le titre du formulaire d'inscription
  title = collector_file             # 
  page = pywikibot.Page(site, title) # objet page  PWB
  gen_cat = get_linked_p(page, 14)   # GEN liens vers l'espace cat sur le formulaire
  return gen_cat   # Retourne un generateur contenant la liste des catégories à superviser
def get_subcats_in(gen_cat): # Retourne gen subcats pour chaque cat in collected
  all_subcats = []           # Une liste contenant des generators
  for cat in gen_cat :       # Retourne le generateur de sous-cat pour chaque categorie inscrite
    gsub = cat.subcategories() # Gen Pwb sous-catégories
    all_subcats.append(gsub)   # Ajoute dans la liste globale
  return all_subcats           # Retourne toutes les sous-catégories compilées dans une liste
  
def count_recursive(all_sub) : # reçoit une liste de generateurs
  for gen in all_sub : # Pour chaque Generateur
    print gen
    for page in gen :    # Itération des catégories dans le génerateur
      print page
      c_recursive(page)  #  Appel sous-fonction qui retourne le total dans 'all_in_cat'
  
def c_recursive_old(page) : # Reçoit page categorie ; Compte recursif et ajoute le total dans 'all_in_cat'
  gen_all = page.articles(recurse=True)  # liste recursive de tous les articles cat et subcat
  print 'gen all OK'
  all_in_list = list(gen_all)   ###ATTENTION Processus très long
  all_in_cat = len(all_in_list)
  print all_in_cat
  page_prop = dict_page[page]
  page_prop['all_in_cat'] = all_in_cat
  #print page_prop['all_in_cat']
  
### DEBUG
def c_recursive(page) : # Reçoit page categorie ; Compte recursif et ajoute le total dans 'all_in_cat'
  gen_all = page.articles(recurse=True)  # liste recursive de tous les articles cat et subcat
  print 'gen all OK'
  #for n in gen_all :
    #print n
  all_in_list = list(gen_all)   ###ATTENTION Processus très long
  all_in_cat = len(all_in_list)
  print all_in_cat
  page_prop = dict_page[page]
  page_prop['all_in_cat'] = all_in_cat
  print page_prop['all_in_cat']

### Collect namespace's data
nsdata = ns_collect_data(ns_id) # Scan l'espace de noms collecte les données
dict_page = nsdata['dict_page'] # reconnait le dictionnaire des pages

#   COMPTAGE RÉCURSIF 
#   ATTENTION vérifier le comptage récursif pour Géologie et Géographie
#   COMPTAGE RÉCURSIF SOUS CATÉGORIES
gen_cat = get_linked_cat(r_count)
all_sub = get_subcats_in(gen_cat)
count_recursive(all_sub) #

#for cat in gen_cat :
  #print cat
  #c_recursive(cat) #
  
#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 104 Recherche
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot 

### NOUVELLE FONCTION a publier dans namespace_lib ?
def save_links(listname, param, page_prop) : # Filtrer du dictionnaire au préalable !
  l_param = 'l_' + param  # clé de la liste
  n_param = 'n_' + param  # clé de la valeur
  page_prop[l_param] = listname         # ajoute listes departement aux propriétés de la faculté L_DPT  
  page_prop[n_param] = len(listname)    # ajoute le nombre aux propriétés
  
### FONCTIONS NS 104
#   Améliorer/simplifier en filtrant le dictionnaire au départ
#   une fonction en aval chk_lnk(dict, subpage|prefix|cat, propname)
#   ADAPTER FX rch_labo() / FAC : chk_lnk_dpt
### Calcul et ajoute nombre et liste des liens pour les departements de recherche
def departement_recherche(dp) : 
  for page in dp:  # Analyse des DÉPARTEMENTS DE RECHERCHE
    page_prop = dp[page]
    prefix = "fr:Recherche:Département:" # prefix des departement de recherche
    s = str(page)
    if prefix in s and page_prop['nsep'] == 0: # si departement de recherche
      ldptr = check_link_in_subpage(page, '/Contenu', ns_id)
      save_links(ldptr, 'dptr', page_prop)
### Calcul et ajoute nombre et liste des liens pour les laboratoires de recherche
def rch_labo(): 
  category_title = u'fr:Catégorie:Laboratoire de recherche' # à partir de la catégorie
  page = pywikibot.page.Category(site, category_title)      # créé la l'objet page.cat PWB
  articles = page.articles() # collecte liste des articles de la catégorie
  articles = list(articles)  # convertit en liste
  for article in articles:   # chaque article de la catégorie
    list_lab = check_link_in_subpage(article, '/Contenu', ns_id) # Liste des liens
    for mypage in dict_page: # Itération du dictionnaire
      if mypage == article:  # Page du disctionnaire correspondante
	page_prop = dict_page[mypage]           # Déclare les propriétés
	save_links(list_lab, 'lab', page_prop)  # place nombre et liste dans dictionnaire
  return dict_page

### VARIABLES
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 104   
ns_talk_id = ns_id + 1 # Identifiant de l'espace de discussion

### Collecte des données
nsdata = ns_collect_data(ns_id)  # Scan l'espace de noms 
dict_page = nsdata['dict_page']
# Les liens sur la sous-page /Contenu sont affectés aux propriétés de la page supérieure.
departement_recherche(dict_page)
dict_page = rch_labo() 
### Collecte des données de l'espace discussion
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion 

### Ecritures des tables lua
table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # TEST wlms_table() 
lua_code = table_prop_code + table_pages_code     # Concatener le code Lua
module_name = u'ns_' + nsdata['label']            # enregistre le module du namespace
##   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code des tables
talk_module_name = u'ns_' + nstalk['label']  # Nom du module pour l'espace discussion relatif
#   Write modules
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion
#print lua_code                         # TEST affiche le code du module


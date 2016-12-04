#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 106 - Faculté
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot 
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 106  # NAMESPACE ID

### chk_lnk_dpt(dict_page) Pour chaque Faculté,
#   liste et compte les liens vers ns departements 108
#   ajoute les parametres ldpt & n_dpt - voir check_link_in_subpage()
def chk_lnk_dpt(dict_page) :
  for page in dict_page:
    page_prop = dict_page[page]
    count_dpt = 0  # n_dpt calcul le nombre de départements pour la faculté
    if page_prop['nsep'] == 0 :         # ATTENTION tjrs les racines nb_sep = 0 donc page racine 
      ldpt = check_link_in_subpage(page, '/Départements', 108) # BUG corrigé :ventilation des départements
      page_prop['ldpt'] = ldpt      # ajoute listes departement aux propriétés de la faculté      
      page_prop['n_dpt'] = len(ldpt)  # ajoute le nombre aux propriétés
  return dict_page

### Inverse le dictionnaire des facultés en dictionnaire de departements
#   Retourne la première liste de départements
#   ATTENTION la collecte des redirection est desactivée
#   probablement inutile ici...
def tupleinvert():
  dpt_fac = {}
  for page in dict_page:       # Pour Chaque faculté
    page_prop = dict_page[page] # une liste de parametres
    if page_prop['nsep'] == 0:  # Filtre des pages racines
      for departement in page_prop['ldpt' ]: # pour chaque departement dans cette faculté
	dpt_params = {}                      # initialise DICTIONNAIRE des prop du dept
	if not departement in dpt_fac:   # Si le departement n'est pas dans le tuple inverse
          l_fac = []                     # Initialise Liste des faculté pour ce departement
          l_fac.append(page)             # Ajoute la faculté dans la liste  
          dpt_params['l_fac'] = l_fac    # copie la liste des facultés dans le nouveau dictionnaire
          dpt_fac[departement] = dpt_params # enregistre clé valeur dans le tuple inverse
        else:                               # Le departement est deja dans le tuple inverse
          dpt_params = dpt_fac[departement] # Recupere la liste  
          dpt_params['l_fac'].append(page)  # Ajoute la faculté dans la liste CONTENUE dans le dictionnaire
  return dpt_fac

### Collect data
nsdata = ns_collect_data(ns_id)    # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']    # retourne le dictionnaire des pages
dict_page = chk_lnk_dpt(dict_page) # Ajoute la liste de liens pour les departements
### Write data
table_prop_code = wlms_table_prop(ns_id, nsdata) # Écrit la table Lua des propriétés de l'espace de noms
table_pages_code = wlms_table_pages(dict_page)   # Écrit la table Lua des pages de l'espace de noms
dpt_fac= tupleinvert()                           # Inverse le dictionnaire
table_dpt_code = wlms_table(dpt_fac,'dpt_fac')   # Écrit la table spécifique de contrôle des départements
### Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code + table_dpt_code # Concatener le code Lua
### Save Data
module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
#print lua_code                         # TEST affiche le code du module
write_module_lua(module_name, lua_code) # TEST Ecriture du module

#def chk_lnk_dpt_old(dict_page) :
  #merged = merge_sub2(dict_page)    # merge_sub2 RENOMMER
  #dict_root_sub = root_sub2(merged) # Ajoute la liste des sous-pages aux propriétés des pages racines
  #for page in dict_page:
    #page_prop = dict_page[page]
    #count_dpt = 0  # n_dpt calcul le nombre de départements pour la faculté
    #if page_prop['nsep'] == 0 :         # ATTENTION tjrs les racines nb_sep = 0 donc page racine 
      ### construire l'objet page pour la sous-page ~/Départements
      #gen_dpt = get_linked_p(page, 108) # Récupère la liste des liens vers l'espace departement 
      #list_dpt = []                     # initialise une liste vide 
      #for g in gen_dpt:                 # Pour chaque lien dans le générateur
	#list_dpt.append(g)              # place le lien dans la liste
      #page_prop['ldpt'] = list_dpt      # ajoute listes departement aux propriétés de la faculté      
      #for dpt in list_dpt:              # pour chaque département
	#count_dpt = count_dpt + 1       # Compte le nombre de départements
	#page_prop['n_dpt'] = count_dpt  # ajoute le nombre aux propriétés
  #return dict_page
  
#### CHK SUB FOR LNK --- AMELIORER
##   Cherche les liens dans les sous-pages 
##   COPIE DPT LIB
##   argument pour l'espace de destination (0 principal, 104 Rch)
#def check_link_in_subpage(page, sub, nsid): # sub contient le nom de la sous-page
  #title = str(page)               # Convertit en sub
  #title = title[2:-2] + sub          # ajoute les crochets
  #title = unicode(title, 'utf-8')    # Convertit en unicode
  #page = pywikibot.Page(site, title) # Créé un objet page PWB 
  #exist = page.exists()              # Test si la page existe
  #if exist:
    #links = get_linked_p(page, nsid)   # titre de la page et namespace id RECUPERER le numero en argument
  ##else: # La page n'existe pas!
  ##  gen = [] #??? 
  #links = gen_to_list(links)  # convertit le générateur en liste python
  #return links # retourner une LISTE 
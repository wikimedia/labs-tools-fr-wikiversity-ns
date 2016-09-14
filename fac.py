#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot ###, re, sys
from namespace_lib import *
from lua_mw_lib import *

### Outil d'analyse et report de données sur l'espace de noms numero 106 - Faculté
### Licence CeCiLL voir Licence.txt
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 106  # NAMESPACE ID

### CHK LNK Dpt for FAC
#   Liste et compte les liens vers ns departements 108
#   ajoute les parametres ldpt & n_dpt
#   AMELIORER (séparer racines(fx), separer cont, type liste donc len(list)
def chk_lnk_dpt(dict_page) :
  for page in dict_page:
    page_prop = dict_page[page]
    count_dpt = 0  
    if page_prop['nsep'] == 0 :         # ATTENTION tjrs les racines nb_sep = 0 donc page racine 
      gen_dpt = get_linked_p(page, 108) # Récupère la liste des liens vers l'espace departement 
      list_dpt = []                     # place 
      for g in gen_dpt:
	list_dpt.append(g)
      page_prop['ldpt'] = list_dpt       # ajoute listes departement aux propriétés de la faculté      
      for dpt in list_dpt:               # pour chaque département
	count_dpt = count_dpt + 1        # Compte le nombre de dṕartement
	page_prop['n_dpt'] = count_dpt # ajoute le nombre de départements aux propriétés
  return dict_page


### Inverse le dictionnaire des fac en dictionnaire de departement
def tupleinvert():
  dpt_fac = {}
  for page in dict_page:   #  Pour Chaque faculté
    page_prop = dict_page[page]     # une liste de parametres
    #[nb_sep, date1, cible, gen_dpt, n_dpt] = page_prop # Liste des parametre deja dans le tuple
    if page_prop['nsep'] == 0: # ATTENTION
      for departement in page_prop['ldpt' ]:     # pour chaque departement dans cette faculté
	redir = departement.isRedirectPage()
	target_departement = ''
	if redir == True:
	  target_departement = departement.getRedirectTarget()
	if not departement in dpt_fac:  # Si le departement n'est pas dans le tuple inverse
          l_fac = []                     # Initialise Liste des faculté pour ce departement
          l_fac.append(page)             # Ajoute la faculté dans la liste
          dpt_params = [page_prop['cible'], l_fac]
          dpt_fac[departement] = dpt_params   # enregistre clé valeur dans le tuple inverse
        else:                            # Le departement est deja dans le tuple inverse
          dpt_params = dpt_fac[departement]   # Recupere la liste 
          [cible, l_fac] = dpt_params
          l_fac.append(page)             # Ajoute la faculté dans la liste
  return dpt_fac

### ETAPE 1 
nsdata = ns_collect_data(ns_id)           # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']
dict_page = chk_lnk_dpt(dict_page)        # Ajoute la liste de liens pour les departements
table_prop_code = wlms_table_prop(ns_id, nsdata) # la table des propriétés de l'espace de noms ¿ns_id?
table_pages_code = wlms_table_pages(dict_page)   ###TEST wlms_table_pages(nsdata)       # la table des pages
dpt_fac= tupleinvert()            # Inverse le dictionnaire
### AMELIORER la fonction doit recevoir le nom de la table
#   Deplacer fonction dans wlmslib
table_dpt_code = write_tableau(dpt_fac) # write_tableau - ecrit la table spécifique de contrôle sur département
###
# Concatener le code Lua ici
lua_code = table_prop_code + table_pages_code + table_dpt_code   # Concatener le code Lua
module_name = u'ns_' + nsdata['label']  # enregistre le module du namespace
print lua_code                          # TEST affiche le code du module
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 

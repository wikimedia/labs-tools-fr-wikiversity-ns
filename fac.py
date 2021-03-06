#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 106 - Faculté
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot 

### get_link(dict_page, param) Reçoit dictionnaire et nom du paramètre à ajouter.
#   utilise check_link_in_subpage() pour la liste des liens.
#   Ajoute les propriétés liste et taille de la liste dans les clés l_param et n_param
#   - voir check_link_in_subpage()
def get_link(dict_page, param) : # Filtrer du dictionnaire au préalable !
  for page in dict_page: 
    page_prop = dict_page[page] # Declare les propriétés de la page
    l_param = 'l_' + param  # clé de la liste
    n_param = 'n_' + param  # clé de la valeur
    if page_prop['nsep'] == 0 :         # ATTENTION tjrs les racines nb_sep = 0 donc page racine 
      ldpt = check_link_in_subpage(page, '/Départements', 108) # BUG corrigé :ventilation des départements
      page_prop[l_param] = ldpt         # ajoute listes departement aux propriétés de la faculté L_DPT  
      page_prop[n_param] = len(ldpt)    # ajoute le nombre aux propriétés
  return dict_page

### Inverse le dictionnaire des facultés en dictionnaire de departements
#   Retourne la première liste de départements
def tupleinvert(): # AJOUTER n_fac !
  dpt_fac = {}
  for page in dict_page:        # Pour Chaque faculté
    page_prop = dict_page[page] # une liste de parametres
    if page_prop['nsep'] == 0:  # Filtre des pages racines
      for departement in page_prop['l_dpt' ]: # pour chaque departement dans cette faculté
	dpt_params = {}                       # initialise DICTIONNAIRE des prop du dept
	if not departement in dpt_fac:   # Si le departement n'est pas dans le tuple inverse
          l_fac = []                     # Initialise Liste des faculté pour ce departement
          l_fac.append(page)             # Ajoute la faculté dans la liste  
          dpt_params['l_fac'] = l_fac    # copie la liste des facultés dans le nouveau dictionnaire
          dpt_fac[departement] = dpt_params # enregistre clé valeur dans le tuple inverse
        else:                               # Le departement est deja dans le tuple inverse
          dpt_params = dpt_fac[departement] # Recupere la liste  
          dpt_params['l_fac'].append(page)  # Ajoute la faculté dans la liste CONTENUE dans le dictionnaire
  for dpt in dpt_fac : # AJOUTER n_fac !
    dpt_params = dpt_fac[dpt]
    dpt_params['n_fac'] = len(dpt_params['l_fac'])
  return dpt_fac


lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 106  # NAMESPACE ID
ns_talk_id = ns_id + 1 # Identifiant espace de discussion relatif

### Collect data
nsdata = ns_collect_data(ns_id)    # Scan l'espace de noms VERSION 2
dict_page = nsdata['dict_page']    # retourne le dictionnaire des pages
dict_page = get_link(dict_page, 'dpt') # Ajoute la liste de liens pour les departements
#   Talkspace
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion
### Write data
table_prop_code = wlms_table_prop(ns_id, nsdata)  # Écrit la table Lua des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # Écrit la table Lua des pages de l'espace de noms
dpt_fac= tupleinvert()                            # Inverse le dictionnaire
table_dpt_code = wlms_table(dpt_fac,'dpt_fac')    # Écrit la table inverse pour contrôle des départements
lua_code = table_prop_code + table_pages_code + table_dpt_code  # Concatener le code Lua
module_name = u'Nsm/Table/' + str(ns_id)   # compile le nom du module de l'espace en minuscule
#    Talkspace
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'Nsm/Table/' + str(ns_talk_id)   # compile le noms du module en minuscule
### Save Data
write_module_lua(talk_module_name, lua_talk_code)     # Ecriture des tables de l'espace discussion
write_module_lua(module_name, lua_code) # TEST Ecriture du module
#print lua_code                         # TEST affiche le code du module
#print module_name
#print talk_module_name

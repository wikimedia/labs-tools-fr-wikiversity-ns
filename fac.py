#!/usr/bin/env python
# -*- coding: utf-8  -*-
import pywikibot, re, sys
from namespaceLib import *
### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family) 
ns_id = 106  # NAMESPACE ID

### Faculté - Fonctions spécifiques
#   tupleinvert() inverse le dictionnaire des facultés pour
#   établir une première liste de départements 
def tupleinvert():
  dpt_fac = {}
  for page in dict_page:   #  Pour Chaque faculté
    page_prop = dict_page[page]     # une liste de parametres
    [nb_sep, date1, cible, gen_dpt, n_dpt] = page_prop # Liste des parametre deja dans le tuple
    if nb_sep == 0: # ATTENTION
      for departement in gen_dpt:     # pour chaque departement dans cette faculté
	redir = departement.isRedirectPage()
	target_departement = ''
	if redir == True:
	  target_departement = departement.getRedirectTarget()
	if not departement in dpt_fac:  # Si le departement n'est pas dans le tuple inverse
          l_fac = []                     # Initialise Liste des faculté pour ce departement
          l_fac.append(page)             # Ajoute la faculté dans la liste
          dpt_params = [cible, l_fac]
          dpt_fac[departement] = dpt_params   # enregistre clé valeur dans le tuple inverse
        else:                           # Le departement est deja dans le tuple inverse
          dpt_params = dpt_fac[departement]   # Recupere la liste 
          [cible, l_fac] = dpt_params
          l_fac.append(page)             # Ajoute la faculté dans la liste
  return dpt_fac


### ETAPE 1 
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)            #
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
prop.append(lang)                # ajoute le code langue pour former le préfixe des filtres
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop
### La date d’importation via l’historique avec le résumé suivant: (00 révisions importées depuis…
lua_code = write_t_prop(ns_id, prop)  ### la table des propriétés de l'espace de noms
### AMeLIORER cherche les liens vers les departements
#   la page ~/Dépatements est transcluse dans la page de chaque faculté
#   dont on récupère les liens vers ns(108)
for page in dict_page:
  page_prop = dict_page[page]
  count_dpt = 0  
  if page_prop[0] == 0 : # si nb_sep = 0 donc page racine 
    list_dpt = get_linked_p(page, 108) # Récupère la liste des liens vers l'espace departement 
    # depuis la page faculté pas besoin de la sous-page departement
    page_prop.append(list_dpt)         # ajoute listes departement aux propriétés de la faculté      
    for dpt in list_dpt:               # pour chaque département
      count_dpt = count_dpt + 1        # Compte le nombre de dṕartement
  else:                                 # La page est une sous-page
    list_dpt = []                       # il faut une valeur 0
    page_prop.append(list_dpt)  # ajoute listes departement aux propriétés de la faculté
  page_prop.append(count_dpt)   # ajoute le nombre de départements aux propriétés
  dict_page[page] = page_prop

table_code =  write_t_pages2(dict_page) ### la table des pages #ATTENTION write_t_pages2
dpt_fac= tupleinvert()            # Inverse le dictionnaire
dpt_code = write_tableau(dpt_fac) # write_tableau - ecrit la table spécifique de contrôle sur département
lua_code = lua_code + table_code + dpt_code # trois tables prop, pages, dpt
# Concatener le code Lua ici
module_name = u'ns_' + ns_label
# print lua_code #TEST
write_module(module_name, lua_code)  # TEST ## Ecriture du module


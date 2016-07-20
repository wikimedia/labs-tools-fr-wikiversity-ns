#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re, sys
from namespaceLib import *

### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

ns_id = 4  #Rev.5 

### ETAPE 1 - Fonctions communes à tous les espaces de noms
#   
ns_label = site.namespace(ns_id) # Label local du namespace
prop = ns_prop(ns_id)      
prop.append(ns_label)            # ajoute le label local de l'espace à la liste des propriétés
print ns_label
print type(ns_label)
#ns_label = unicode(ns_label)
[total, redirection, racine, sous_page, verif, dict_page, ns_id, ns_label] = prop   ## Ajouter lang
### FIN ETAPE 1

### write_t_pages() reçoit le dictionnaire des pages
#   pour le transformer en code Lua de la table t_pages
#   Adapter pour les dict 3 colonnes avec dates Salle cafés
#   nom table lua = t + nom du dictionnaire
def write_t3dated(dict_name):
  # calcul du nom de la table
  t = 'p.t_salle_cafe = {\n'
  for page in dict_name:
    [nb_sep, cible, timestamp] = dict_name[page] # Comment obtenir les noms des prop de pages?
    t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', tms = \'' + str(timestamp) + '\', ' + str(cible)  + '},\n'
    # cible en dernier optionnel (encadrer timestamp par des guillemets)
  t = t + '}\n'
  return t

### Etape 2 - Fonctions spécifiques à l'espace de noms Wikiversité
#   Ajoute une table la salle café avec les dates

#dict_salle_cafe = {}
#dict_filtre = {}
#from datetime import datetime, date, time # inutile
for page in dict_page:
  name = str(page)
  page_prop = dict_page[page]        # déclare la liste de propriétés de la page
  [nb_sep, date, cible] = page_prop
  if 'fr:Wikiversité:La salle café' in name:
    #Pages à supprimer
    #Administrateur/Candidature
    #fr:Wikiversité:Bureaucrate/Candidature
    first_rev = page.oldest_revision   # genère un tuple contenant les info. de la première revision
    #print first_rev
    get_date = first_rev.timestamp    # copie la valeur date et heure de création
    #print get_date
    page_prop[1] = get_date
    # page_prop.append(timestamp)        # FAUX ajoute la date de 1ère révision à la liste
    #dict_salle_cafe[page] = page_prop
  #else:
    #dict_filtre[page] = page_prop      # filtre les pages restantes
#dict_page = dict_filtre                # supprime la salle de café du dictionnaire de page


### Etape 3 - Ecriture du module
ns_prop_code = write_t_prop(ns_id, prop)        # la table des propriétés de l'espace de noms
table_code =  write_t_pages(dict_page)          # la table des pages
#salle_cafe_code = write_t3dated(dict_salle_cafe) # fonction locale ecrit la table de la salle cafe
print type(ns_prop_code)
table_code = unicode(table_code, 'utf_8')
print type(table_code)
lua_code = ns_prop_code + table_code   #+ salle_cafe_code
# Concatener le code Lua ici
#lua_code = unicode(lua_code, 'utf-8')
module_name = u'ns_' + ns_label
#print(lua_code) 
write_module(module_name, lua_code)    ### Ecriture du module #TEST 



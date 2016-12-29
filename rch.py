#!/usr/bin/env python
# -*- coding: utf-8  -*-
### Outil d'analyse et report de données sur l'espace de noms numero 104 Recherche
### Licence CeCiLL voir Licence.txt
from namespace_lib import *
from lua_mw_lib import *
import pywikibot 

### FONCTIONS NS 104
def rch_labo(): 
  category_title = u'fr:Catégorie:Laboratoire de recherche' # à partir de la catégorie
  page = pywikibot.page.Category(site, category_title)      # créé la l'objet page.cat PWB
  articles = page.articles() # collecte liste des articles de la catégorie
  articles = list(articles)  # convertit en liste
  for article in articles:   # chaque article de la catégorie
    l_doc = check_link_in_subpage(article, '/Contenu', ns_id)
    for mypage in dict_page: # 
      if mypage == article:
	page_prop = dict_page[mypage]
	page_prop['l_doc'] = l_doc         # RENOMMER l_lab
	page_prop['n_doc'] = len(l_doc)    # Donc n_lab
	page_prop['class_doc'] = '\'lab\'' # NOUVELLE VARIABLE ATENTION MARCHE ARRIèRe
  return dict_page

### VARIABLES
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  
ns_id = 104   
ns_talk_id = ns_id + 1 # Identifiant de l'espace de discussion

### ETAPE 1 
nsdata = ns_collect_data(ns_id)  # Scan l'espace de noms 
dict_page = nsdata['dict_page']
### Collect data DISCUSSIONS NAMESPACES
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion 

### Ajoute la liste et le nombre de documents de recherche au dictionnaire des pages
### Filtre les departements de recherche Collecte les liens vers ns_104 
### ADAPTER FX rch_labo() / FAC : chk_lnk_dpt(dict_page A FAIRE : get_links_stat(dict, propname)
#   une fonction pour obtenir root_dict = ns_root_dict()
#   une fonction en aval chk_lnk(dict, subpage|prefix|cat, propname)
#   reste la condition qui est particulière ; filtre le dict puis appeler sub
for page in dict_page:  # Analyse des départements de recherche
  page_prop = dict_page[page]
  prefix = "fr:Recherche:Département:" # prefix des departement de recherche
  s = str(page)
  if prefix in s and page_prop['nsep'] == 0: # si departement de recherche
    l_doc = check_link_in_subpage(page, '/Contenu', ns_id)
    page_prop['l_doc'] = l_doc          # RENOMMER l_dptr
    page_prop['n_doc'] = len(l_doc)     # RENOMMER n_dptr nombre d'occurrences
    page_prop['class_doc'] = '\'dptr\'' # ABANDON NOUVELLE VARIABLE l_doc lab/dptr

dict_page = rch_labo() # ATTENTION liens sur la sous-page /Contenu affectés aux propriétés de la page supérieure ou racine.

### Ecritures des tables lua
table_prop_code = wlms_table_prop(ns_id, nsdata)  # la table des propriétés de l'espace de noms
table_pages_code = wlms_table(dict_page, 'pages') # TEST wlms_table() 
lua_code = table_prop_code + table_pages_code     # Concatener le code Lua
module_name = u'ns_' + nsdata['label']            # enregistre le module du namespace
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code des tables
talk_module_name = u'ns_' + nstalk['label']  # Nom du module pour l'espace discussion relatif
#   Write modules
write_module_lua(module_name, lua_code) # Ecriture du module #TEST 
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion
#print lua_code                         # TEST affiche le code du module

### DOUBLE EMPLOI CHK_LINK_IN_SUBPAGE
#### Liste des documents de recherche liés dans la sous-page "/Contenu"
##   Charger la liste des pages à analyser via celle des articles dans la catégorie Laboratoire de recherche
#def find_content(page): # reçoit un objet page retourne l'objet sous-page/Contenu
  ## VOIR check_link_in_subpage(page, '/subpage', ns_id)
  #spage = str(page)
  #content = spage[2:-2] + '/Contenu'
  #title = unicode(content, 'utf-8')
  #page = pywikibot.Page(site, title)
  #return page
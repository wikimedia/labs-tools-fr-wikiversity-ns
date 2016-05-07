#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licence CeCILL compatible Gnu-Gpl (License.txt)

### Liste les pages de l'espace de nom "Département" nº 108 
#   Verifie si redirection et cherche la cible
#   Liste les sous-pages. les liens dans leçons par thèmes et leçons par niveaux
#   Compare les deux listes de liens et les fusionnent
#   Verifie si les pages derrière les liens existent
### Compare le nombre de page d'interface et le nombre de leçons du département

import pywikibot
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

sous_pages = []
table_ns_108 = {}
all_sous_pages = [] # DEBUG liste brute des sous_pages
no_match = []       # DEBUG 
data_dpt = {}       # [departement] = sous_pages
#log = ''

### Fonction 1 -tupledpt()
#   Sépare les pages de départements et les sous-pages
#   Teste si redirection
#   Associe Département avec sous-page et redir
#   nb_pages et no_match pour contrôle
#   data_dpt[departement] = [sous_pages, redir, target_page]
def tupledpt():
  gen_dpt = site.allpages(namespace=108) #, prefix='k') TEST
  nb_pages = 0 # Compteur de pages
  curent = u''  # Compare la sous-page
  redir = False
  target_page = ''
  for page in gen_dpt:
    nb_pages = nb_pages + 1
    str_page = str(page) # il faut une chaine 
    if '/' in str_page:    #  SI Le titre de la page contient un separateur
      all_sous_pages.append(page)   # Ajoute dans liste de contrôle
      prefix = curent[ 0 : -2]      # supprime crochets fermants de la page courante
      if prefix in str_page:     # Si le prefixe de la page courante se trouve dans le nom de la sous-page
        sous_pages.append(page)  # Incrémente la liste des sous-pages
      else:   # ATTENTION Le prefix courant ne correspond pas
        no_match.append(page)   # Controle ; stock les sous-pages dont le prefix ne correspond pas
        pass
    else:   # Pas de separateur donc département
      departement = page
      curent = str_page
      print departement
      redir = departement.isRedirectPage()
      if redir == True:
	target_page = page.getRedirectTarget()
      else:
	target_page = 'N'    # un texte quelconque pour éviter nil
      sous_pages = []
      data_dpt[departement] = [sous_pages, redir, target_page]
  table_ns_108['total_pages'] = nb_pages
  table_ns_108['pseudo_dpt'] = len(data_dpt)
  table_ns_108['total_sous_pages'] = len(all_sous_pages)
  table_ns_108['no_match'] = no_match
  return data_dpt  # Retourne le tuple et la sommes des pages dans l'espace de noms

### La fonction findlinks()
#   Cherche les liens dans les pages speciales
#   Ajoute la liste des leçons par themes et par niveaux dans le tuple
def findlinks():
  count_dpt = 0
  for departement in sorted(data_dpt):
    count_dpt = count_dpt + 1
    print count_dpt
    dpt_params = data_dpt[departement]
    [sous_pages, redir, target_page] = dpt_params
    list_link_theme = []  # Liste Leçons par Thèmes
    list_link_niveau = [] # Liste Leçons par Niveaux
    str_departement = str(departement)
    theme = str_departement[2:-2] + '/Leçons par thèmes'
    title = unicode(theme, 'utf-8')     # Leçons par thèmes
    page = pywikibot.Page(site, title)  # La page 
    exist = page.exists()               # Teste
    if exist:     # Leçons par thèmes EXIST
      gen_lesson_theme = page.linkedPages(namespaces=0) # place les pages liéés dans un generateur
      for link_theme in gen_lesson_theme:  # chaque element du generateur
        list_link_theme.append(link_theme) # est stocké dans la liste des leçons par thèmes
      dpt_params.append(list_link_theme)
      data_dpt[departement] = dpt_params   # la liste est ajoutée au tuple    
    else:
      dpt_params.append(list_link_theme)
      data_dpt[departement] = dpt_params
    niveau = str_departement[2:-2] + '/Leçons par niveaux' # Compile le nom de  la page
    title = unicode(niveau, 'utf-8')   # Unicode pour PWB
    page = pywikibot.Page(site, title) # Leçon par niveaux
    exist = page.exists()
    if exist:   # Leçon par niveaux EXIST
      gen_lesson_niveau = page.linkedPages(namespaces=0) # place les pages liéés dans un generateur
      for link_niveau in gen_lesson_niveau:  # chaque element du generateur
        list_link_niveau.append(link_niveau) # est stocké dans la liste des leçons par 
      dpt_params.append(list_link_niveau)
      data_dpt[departement] = dpt_params   
    else: #'La page Leçon par niveau n\'existe pas!\n'
      dpt_params.append(list_link_niveau)
      data_dpt[departement] = dpt_params 
  return data_dpt

### Fonction linkexist()
#   compare les liens par thèmes et par niveau
#   verifie si la page du lien existe
def linkexist():
  for departement in data_dpt: # chaque departement
    dpt_params = data_dpt[departement]
    [sous_pages, redir, target_page, list_link_theme, list_link_niveau] = dpt_params
    list_link_add = []    # vider à chaque passage
    list_link_total = []  # vider à chaque passage
    list_link_exist = []  # vider à chaque passage
    for link_niveau in list_link_niveau:  # chaque leçon par niveau (tester avec if not)
      if link_niveau in list_link_theme:  # si contenue dans la liste par theme
        pass
      else:
        list_link_add.append(link_niveau) # Sinon ajoute dans la Liste Lien Additionnel
    dpt_params.append(list_link_add)
    list_link_total = list_link_theme + list_link_add   # Liste total des Lien = leçons par thèmes + par niveaux flitrées
    dpt_params.append(list_link_total)
    for link in list_link_total: 
      page = link            #
      exist = page.exists()  # Si la page existe
      if exist:
        list_link_exist.append(link)   # Liste des Liens existants
      else:
        pass
    dpt_params.append(list_link_exist)
    balance = len(list_link_exist) - (len(sous_pages) + 1)
    dpt_params.append(balance)
    data_dpt[departement] = dpt_params #sous_pages, redir, list_link_theme, list_link_niveau, list_link_add, list_link_total, list_link_exist, balance
  return data_dpt

### Fonction - write_lua_module()
#   Ecrit le code Lua dans le module Table_département
#   ns_departement = {page{}, sous_page{}, ...}
def write_lua_module():
  lua_code = 'local p = {}\np.ns_departement = {'
  for page in data_dpt:
    dpt_params = data_dpt[page]
    [liste_sous_page, redir, target_page, list_link_theme, list_link_niveau, list_link_add, list_link_total, list_link_exist, balance] = dpt_params
    lua_code = lua_code + '{name = ' + str(page) + ', \n'           # La page du supposé département
    lua_liste_sous_page = list_py_to_lua(liste_sous_page)  # La liste des sous-pages
    lua_code = lua_code + '    lsp = ' + lua_liste_sous_page + ', \n'        
    lua_code = lua_code + '    redir = ' + str(redir) + ', \n    cible = ' + str(target_page) + ', \n'# Redir & Cible_redir
    listes = [list_link_theme, list_link_niveau, list_link_add, list_link_total, list_link_exist]
    for liste in listes:  # traite chaque liste restante
      # Pour pouvoir mommer chaque liste dans la table Lua
      # il faut placer les listes dans un tuple dont les clés
      # seront utilisées dans la table Lua "list_link_thème = {...}"
      lua_liste = list_py_to_lua(liste) # via la fonction
      lua_code = lua_code + '    ' + lua_liste + ', \n'  # ajoute le code lua pour chacune
    lua_code = lua_code + '    }, \n' # Ferme la table page (departement)
  # On abandonne la colonne calculée 'balance' on peut la calculer plus tard dans le module
  # on utilisera table.maxn sos lua pour calculer la taille des listes
  lua_code = lua_code + '}\n'
  resume = write_resume_108()
  lua_code = lua_code + resume + 'return p'   # Ferme la table ns.departement et termine le module
  lua_code = unicode(lua_code, 'utf-8')       # UNICODE
  return lua_code
##  Fonction list_py_to_lua()
#   Convertit une liste Python en chaine de caractère pour code Lua-Scribunto
def list_py_to_lua(my_list):
  my_list_lua = '{' 
  for item in my_list:
    my_list_lua = my_list_lua + str(item) + ', '
  if len(my_list) == 0:
    my_list_lua =   my_list_lua + '}'
  else:
    my_list_lua =   my_list_lua + '}'
  my_list_lua = str(my_list_lua)
  return my_list_lua
## Fonction write_resume_108()
#  Ećrite la table Lua résumant l'espace de noms Departement 108
#  avec les nombres de pages, sous-pages et valeurs de controle
def write_resume_108():
  resume = 'p.resume_ns_108 = {\n'
  for key in table_ns_108:
    value = table_ns_108[key]
    if type(value) == list:
      resume = resume + '    ' + str(key) + ' = ' + list_py_to_lua(value) + ', \n'
    else:
      resume = resume + '    '+ str(key) + ' = ' + str(value) + ', \n'# 3 integer et une liste(no match)
  resume = resume + '}\n'
  return resume

###
# START - DEBUT 
###

data_dpt = tupledpt()   # , nb_pages
data_dpt = findlinks()
data_dpt = linkexist()
module_lua = write_lua_module()
title = u'Module:Table_département'  # u'Module:Catest' #TEST devie la sauvegarde vers un module de test
comment = u'Ecriture de la table de données de l\'espace de nom Département.'
page = pywikibot.Page(site, title)

page.text = module_lua
page.save(comment)   # ATTENTION écriture du 'Module:Table_département'
# print module_lua # TEST
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licence CeCILL compatible Gnu-Gpl (License.txt)

########################################################################
### Création d'une liste de faculté 
### basée sur l'analyse de l'espace de nom "Faculté:" num_id "106" via Pywikibot
### le script produit 3 pages, liste des facultés, liste des départements par faculté
### et  liste des départements
########################################################################

import pywikibot
lang = 'fr'                    
family = 'wikiversity'
site = pywikibot.Site(lang, family) 

### Variables etape-1
liste_facultes = []   # pages
liste_sous_pages = [] # sous-pages
liste_ns_106 = []     # liste pour résumer le nombre de pages dans l'espace de nom via t_ns_106
listes = [liste_facultes, liste_sous_pages, liste_ns_106]
### Variables etape-2
data_fac = {}         # key = faculté ; value = fac_params
### Variables etape-3
dpt_fac = {}          # Tuple invere

### Fonction etape-1 : scanfac retourne reourne 2 listes (pages et sous-page) ... + liste_ns_106
def scanfac():
  gen_fac = site.allpages(namespace=106)#, prefix='p')
  total_pages = 0
  for page in gen_fac:
    total_pages = total_pages + 1
    str_page = str(page)           # Une chaine pour rechercher '/'
    if '/' in str_page: # SOUS-PAGE
      liste_sous_pages.append(page)  # La liste des sous-pages
    else:               # PAGE
      liste_facultes.append(page)    # La liste des facultés
  liste_ns_106.append(total_pages)   # Les 3 valeurs ne sont pas nommée
  liste_ns_106.append(len(liste_facultes)) # Il faudrait un disctionnaire
  liste_ns_106.append(len(liste_sous_pages)) # pour associer les valeurs à des clés
  return listes
### Fonction etape 2: tuplefac retourne un tuple, data_fac qui associe les facultés et leurs paramètres
### data_fac[faculte] = fac_params (sous_page_fac, gen_dpt, nombre_departement)
### et la fonction imprime un fichier csv ; tableau simple sur 3 colonnes
def tuplefac():
  count_fac = 0
  liens_departements = 0   # valeur de controle
  for faculte in liste_facultes:   # pour chaque faculté
    count_fac = count_fac + 1
    fac_params = []     # liste contenanat celle des departements (gen_dpt) puis nombre_departement
    sous_page_fac = []  # Liste les sous_pages de chaque faculté dans ns
    str_faculte = str(faculte)
    str_faculte = str_faculte[0:-2] + '/'  # tronque les crochets fermants et Ajoute le separateur
    for sous_page in liste_sous_pages:     # Attribue les sous-pages sur la base du prefix
      str_sous_page = str(sous_page)       # 
      if str_faculte in str_sous_page:     # en comparant les deux chaines
	sous_page_fac.append(sous_page)    # Pas d'autre verification...    
    fac_params.append(sous_page_fac)       # Affecte la liste sp_fac comme premier elemnt de liste fac_params
    fac_params.append(len(sous_page_fac))
    gen_dpt = faculte.linkedPages(namespaces=108)
    fac_params.append(gen_dpt)
    nombre_departement = 0   # Initialise le compteur de département
    for departement in gen_dpt:   # Pour chaque lien dans le generateur PWB
      nombre_departement = nombre_departement + 1   # Compte les départements
    fac_params.append(nombre_departement)   # Le nombre de dṕartement par faculté
    redir = faculte.isRedirectPage()
    target_faculte = 'No' # Si chaine vide Lua ne sauve pas le code
    if redir == True:
      target_faculte = faculte.getRedirectTarget()
    fac_params.append(redir)            
    fac_params.append(target_faculte)   # Ajouter les nouveaux param. à la fin (index code module Lua)
    data_fac[faculte] = fac_params
    liens_departements = liens_departements + nombre_departement
    print str(count_fac) + " sur: " + str(nombre_faculte)
  print str(liens_departements) + 'liens_departements\n'
  return data_fac

### Fonction 3 tupleinvert() - La fonction inverse le tuple data_fac
### Liste des facultés par département
### departement |liste facultés | nombre de faculte
def tupleinvert():
  for page in data_fac:   #  Pour Chaque faculté
    fac_params = data_fac[page]     # une liste de parametres
    [sous_page_fac, nb_sous_page_fac, gen_dpt, nombre_departement, redir, target_faculte] = fac_params # Liste des parametre deja dans le tuple
    for departement in gen_dpt:     # pour chaque departement dans cette faculté
      redir = False
      redir = departement.isRedirectPage()
      target_departement = ''
      if redir == True:
	target_departement = departement.getRedirectTarget()
      if not departement in dpt_fac:  # Si le departement n'est pas dans le tuple inverse
        l_fac = []                     # Initialise Liste des faculté pour ce departement
        l_fac.append(page)             # Ajoute la faculté dans la liste
        dpt_params = [redir, target_departement, l_fac]
        dpt_fac[departement] = dpt_params   # enregistre clé valeur dans le tuple inverse
      else:                           # Le departement est deja dans le tuple inverse
        dpt_params = dpt_fac[departement]   # Recupere la liste 
        [redir, target_departement, l_fac] = dpt_params
        l_fac.append(page)             # Ajoute la faculté dans la liste
  return dpt_fac


### Fonction 5 - write_module() - Ecriture du module "Table faculté"
# Trier la table avant d'ecrire le module
# par nom puis essayer de placer les redir en debut de liste ensuite
def write_module(): # RENOMMER write_module
  result = 'local p = {}\n'
  # DEBUT fx write_table_fac()
  result = result + 'p.ns_faculte = {\n' # la table de l'ESPACE DE NOM
  for fac in sorted(data_fac):
    [sous_page_fac, nb_sous_page_fac, gen_dpt, nombre_departement, redir, target_faculte] = data_fac[fac]
    result = result + '    {name = ' + str(fac) + ', \n    data = {\n' + '        nbsp = ' + str(nb_sous_page_fac ) + ', \n        ' #', ' + 
    var_liste_sous_page = 'lsp = {'
    if len(sous_page_fac) == 0:
      var_liste_sous_page = var_liste_sous_page + '},'
    else:
      for sous_page in sous_page_fac :
        var_liste_sous_page = var_liste_sous_page + str(sous_page) + ', '
      var_liste_sous_page = var_liste_sous_page + '},' # ATTENTION INUTILE AVEC LUA de supprime la dernière virgule espace avant de fermer l'accolades
    result = result + var_liste_sous_page + '\n        nbdpt = ' + str(nombre_departement) + ', \n'
    var_liste_departement = '        ldpt = {' # Ouvre la table Lua
    c=0   ### Compte les departements
    for departement in gen_dpt:      ### PWB Generator !#@#
      c = c + 1   # Incremente le nombre de departement
      var_liste_departement = var_liste_departement + str(departement) + ', ' # ajoute le departement au code Lua
    if c == 0:    # Si aucun departement
      var_liste_departement = var_liste_departement + '}, \n' # VIDE penser à fermer la table lua
    else:         
      var_liste_departement = var_liste_departement + '}, \n'    #[:-2]
    result = result + var_liste_departement + '        redir = '+ str(redir) + ', \n        cible = ' + str(target_faculte) + ', \n        }, \n    }, \n'
  result = result + '}\n'  #[:-2]
  # STOP ici ajouter la table DEPARTEMENT dpt_fac AVANT RETURN P
  lua_table_departement = write_table_dpt() # La fonction ajoute la table des départements
  result = result + lua_table_departement
  # Ajouter la table t_ns_106
  lua_resume_namespace = write_resume_namespace_106()
  result = result + lua_resume_namespace
  result = result + 'return p\n' ### page /documentatio \n[[Catégorie:Modules tests]]
  result = unicode(result, 'utf-8')
  return result

# Fonction 5.1 - write_table_dpt() - Ecrit le code lua de la table dpt_fac
def write_table_dpt():
  lua_code = 'p.t_departements = {\n    '   # la tables des DEPARTEMENTS à l'exception de toutes les autres pages 
  for departement in sorted(dpt_fac):
    [redir, target_departement, l_fac] = dpt_fac[departement]
    lua_code = lua_code + '{'
    lua_code = lua_code + str(departement) + ', \n'
    if len(l_fac) == 0:
      lua_code = lua_code + '{}, \n'
    else:
      lua_code = lua_code + '        {'
      for faculte in l_fac:
	lua_code = lua_code + str(faculte) + ', '
      lua_code = lua_code + '}, \n        ' 
    lua_code = lua_code + str(redir) + ', ' + str(target_departement) + '\n    }, \n'
  lua_code = lua_code + '}\n'
  return lua_code
# Fonction 5.2 write_t_ns_106() _ Ecrit le code Lua de la table 
def write_resume_namespace_106():
  lua_code = 'p.t_ns_106 = {\n'
  for i in liste_ns_106:
    lua_code = lua_code + '   ' + str(i) + ', \n'
  lua_code = lua_code + '}'
  return lua_code   
###

### Etape-1
listes = scanfac()  # Calcul liste_facultes ; liste_sous_pages
nombre_faculte = len(liste_facultes)
print str(nombre_faculte) + ' Facultés\nListe des départements pour chaque faculté'
### Etape-2
data_fac = tuplefac() # Calcul les propriete des facultés
### Etape-3
dpt_fac = tupleinvert() # Inverse le tuple, calcul le nb de dpt
### TEST
#print '#########'
#for i in liste_ns_106:
#  print i
### Etape 5 - Ecriture du module Lua-scribunto "Module:Table faculté"
code_module = write_module()

# print code_module
title = u'Module:Table faculté' #u'Module:Catest' # ATTENTION 
comment = u'Le module reçoit les données depuis le srcipt Python "fac.py" (cf vocabulary-index on Wikimedia Tool Labs).'
page = pywikibot.Page(site, title)
page.text = code_module
page.save(comment)
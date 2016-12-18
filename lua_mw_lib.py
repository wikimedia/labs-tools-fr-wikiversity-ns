#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Licence CeCill voir licence.txt
### Function library Write Lua tables in Module Scribunto 
### Output files of fr-wikiversity-ns
import pywikibot
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

wmls_table_close = '}\n' # ferme la table principale
wmls_table_next = '},\n' # ferme une sous-table item suivant attendu

### write_lua_module(nom, code) écrit un module vide avec la variable "p"
#   reçoit la partie courte du nom et le code à inserer
def write_module_lua(module_name, lua_code): # Compiler tout le code du module au préalabe
  import __main__ # Pour obtenir le nom du script principal (pas celui de la librairie)
  title = u'Module:' # UNICODE
  title = title + module_name
  comment = u'Module actualisé par : ' + __main__.__file__ + ' ; [[Utilisateur:Youni Verciti]].'
  module = 'local p = {}\n'
  module = module + lua_code
  module = module + '\nreturn p'
  page = pywikibot.Page(site, title)
  page.text = module
  #exist = page.exists()  # Test si la page existe (Empêche page.save de réécrire le module
  #if exist:
    #comment = u'Module actualisé par : ' + __main__.__file__ 
    ##page.save(comment)
  #else:
    #comment = u'Nouveau module créé par :' + __main__.__file__
  #print comment
  page.save(comment)

### wlms_table(python_dict, table_name)
#   reçoit le dictionnaire et le nom de la table en argument
#   compile le code et appel une sous fonction wmls_table_input() pour
#   convertir le dictionnaire des propriété en code Lua
def wlms_table(python_dict, table_name):    # La fonction reçoit un dictionnaire python 
  t = 'p.t_' + table_name + ' = {\n' # et le nom de la table Lua à créer ; compilé ici
  for data in python_dict:
    t = t + '{page = ' + str(data) + ', ' # VAR_TITLE ATTENTION définit variable,compile le nom de la page
    page_prop = python_dict[data]         # déclare le dictionnaire des proriétés de la page
    t = t + wmls_table_input(page_prop)   # compile le code Lua du dict. des propriétés de page
  t = t + wmls_table_close                # fin de table
  t = unicode(t, 'utf_8')
  return t

### wmls_table_input() AMELIORER la fonction reçoit le dictionnaire page_prop
#   TESTER type = int
#   Il faut reproduire les tests pour type=dict
def wmls_table_input(page_prop):
  t = ''
  for prop in page_prop:
    if page_prop[prop] == '':  # si la valeur est vide
      pass                     # Ne code pas le paramètre 
	#t = t + str(prop) + ' = \'\', '    # formate le code lua
    if type(page_prop[prop]) == list:
      t = t + str(prop) + ' = ' + wmls_list_to_lua(page_prop[prop])
    elif prop == 'date1': # AMELIORER type int on reconnait la date par le nom du param.
	t = t + str(prop) + ' = \'' + str(page_prop[prop]) + '\', ' # formate le code lua
    elif type(page_prop[prop]) == dict :   # type = DICT #print type(page_prop[i])
	# sous-fonction ; ici on sait que le dict contient des listes
	# il faudrait tester le type de chaque valeur autre sous-fonction
	mydict = page_prop[prop]
	for key in mydict:
	  v = mydict[key] 
	  # Rustine pour d_lessons AMéliorer :
	  if type(v) == int :
	    t = t + str(key) + ' = ' + str(v) + ', ' # Ce sont des entiers
	  if type(v) == list : 
	    t = t + str(key) + ' = ' + wmls_list_to_lua(v)   # Ce sont des listes
    else:
      t = t + str(prop) + ' = ' + str(page_prop[prop]) + ', '  # formate k, v
  t = t + wmls_table_next  # ferme la table ajoute une virgule
  return t
####DOUBLE EMPLOI avec wlms_table(python_dict, table_name)
##  REMPLACER PAR wlms_table(dict_page, 'pages') -> hlp, cat
## ATTENTION OFF
#def wlms_table_pages(dict_page): 
  #t = 'p.t_pages = {\n'  # placer la chaine dans une variable
  #for page in dict_page: # pour chaque page
    #t = t + '{page = ' + str(page) + ', ' # compile clé et valeur
    #page_prop = dict_page[page]           # le dictionnaire des proriétés de la page
    #t = t + wmls_table_input(page_prop)   # comple le code Lua des propriétés
  #t = t + wmls_table_close                # fin de table
  #t = unicode(t, 'utf_8')                 # UNICODE
  #return t

### Construit la table Lua t_prop des propriétés de l'espce de noms
#   exclu le dictionnaire des pages
def wlms_table_prop(ns_id, nsdata): # 
  t1 = 'p.t_prop = {'
  for data in nsdata:     #print type(nsdata[data])
    if data <> 'dict_page':
      t1 = t1 + data + ' = \'' + unicode(nsdata[data]) + '\', ' # UNICODE compile le code de t_prop
  t1 = t1 + '}\n' # ferme la table de t_prop
  #UNICODE ICI
  return t1  

### Convertit une liste Python en table Lua
#   créé une table simple ipairs sans clé
def wmls_list_to_lua(l): # convertit une liste python en table Lua
  code = '{'                      # ouvre la table
  for i in l:  
    code = code + str(i) + ', '   # ipairs liste items sans clé
  code = code + '}, \n'           # ferme la table + saut de ligne
  return code                     # retourne le code Lua
# Version 2 sans la virgule finale (voir cat.py)
def wmls_list_to_lua2(l): # convertit une liste python en table Lua
  code = '{'                      # ouvre la table
  for i in l:  
    code = code + str(i) + ', '   # ipairs liste items sans clé
  code = code + '} \n'           # ferme la table + saut de ligne (SANS VIRGULE FINALE)
  return code                     # retourne le code Lua

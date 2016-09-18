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

### write_lua_module() écrit un module vide
#
def write_module_lua(module_name, lua_code): # Compiler tout le code du module au préalabe
  title = u'Module:' # UNICODE
  title = title + module_name
  comment = u'Nouveau module ajouté par l\'outil fr-wikiversity-ns sur tools.labs.org'
  module = 'local p = {}\n'
  module = module + lua_code
  module = module + '\nreturn p'
  page = pywikibot.Page(site, title)
  page.text = module
  page.save(comment) # TRY

### wlms_table(python_dict, table_name)
#   reçoit le dictionnaire et le nom de la table en argument
#   compile le code et appel une sous fonction wmls_table_input() pour
#   convertir le dictionnaire des propriété en code Lua
def wlms_table(python_dict, table_name):    # La fonction reçoit un dictionnaire python 
  t = 'p.t_' + table_name + ' = {\n' # et le nom de la table Lua à créer ; compilé ici
  for data in python_dict:
    t = t + '{page = ' + str(data) + ', ' # compile clé et valeur
    page_prop = python_dict[data]         # le dictionnaire des proriétés de la page
    t = t + wmls_table_input(page_prop)   # compile le code Lua du dict. des propriétés de page
  t = t + wmls_table_close                # fin de table
  t = unicode(t, 'utf_8')
  return t

### wmls_table_input() AMELIORER la fonction reçoit le dictionnaire
#   page_prop
#   Il faut reproduire tous les tests pour type=dict
def wmls_table_input(page_prop):
  t = ''
  for prop in page_prop:
    if page_prop[prop] == '':              # si la valeur est nulle
	t = t + str(prop) + ' = \'\', '    # formate le code lua
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
	  t = t + str(key) + ' = ' + wmls_list_to_lua(v) # Ce sont des listes
    else:
      t = t + str(prop) + ' = ' + str(page_prop[prop]) + ', '  # formate k, v
  t = t + wmls_table_next  # ferme la table ajoute une virgule
  return t

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

###DOUBLE EMPLOI avec wlms_table(python_dict, table_name)
#
def wlms_table_pages(dict_page): 
  t = 'p.t_pages = {\n'  # placer la chaine dans une variable
  for page in dict_page: # pour chaque page
    t = t + '{page = ' + str(page) + ', ' # compile clé et valeur
    page_prop = dict_page[page]           # le dictionnaire des proriétés de la page
    t = t + wmls_table_input(page_prop)   # comple le code Lua des propriétés
  t = t + wmls_table_close                # fin de table
  t = unicode(t, 'utf_8')                 # UNICODE
  return t

### Convertit une liste Python en table Lua
#   créé une table simple ipairs sans clé
def wmls_list_to_lua(l): # convertit une liste python en table Lua
  code = '{'                      # ouvre la table
  for i in l:  
    code = code + str(i) + ', '   # ipairs liste items sans clé
  code = code + '}, \n'           # ferme la table + saut de ligne
  return code                     # retourne le code Lua


#def wmls_table_input_old(pp):
  #t = ''
  #for p in pp:
    #if type(pp[p]) == list:
      #t = t + str(p) + ' = ' + wmls_list_to_lua(pp[p])
    #else:
      #t = t + str(p) + ' = ' + str(pp[p]) + ', '  # formate k, v
  #return t
  
#for i in page_prop:                   # pour chaque propriété
      ## ADAPTER wmls_table_input(pp)
      ## print (i)
      ## print type(page_prop[i])
      #if page_prop[i] == '':              # si la valeur est nulle
	#t = t + str(i) + ' = \'\', '      # formate le code lua
      #elif type(page_prop[i]) == list :   # si la valeur est une liste
	#t = t + str(i) + ' = ' + wmls_list_to_lua(page_prop[i])
      #elif i == 'date1': #AMELIORER type int on reconnait la date par le nom du param.
	#t = t + str(i) + ' = \'' + str(page_prop[i]) + '\', '      # formate le code lua
      #elif type(page_prop[i]) == dict :   # type = DICT
	##print type(page_prop[i])
	## sous-fonction ; ici on sait que le dict contient des listes
	## il faudrait tester le type de chaque valeur autre sous-fonction
	#mydict = page_prop[i]
	#for key in mydict:
	  #v = mydict[key]
	  #t = t + str(key) + ' = ' + wmls_list_to_lua(v) # Ce sont des listes
      #else:                               # la clé contient une valeur
	#t = t + str(i) + ' = ' + str(page_prop[i]) + ', '  # formate k, v
    #t = t + wmls_table_next                                # fin de ligne
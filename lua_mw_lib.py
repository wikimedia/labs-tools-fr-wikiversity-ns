#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Licence CeCill voir licence.txt
### Function library Write Lua table in Module Scribunto 
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
  
def wlms_table_prop(ns_id, nsdata): # construit la table Lua t_prop
  t1 = 'p.t_prop = {'
  for data in nsdata:
    #print type(nsdata[data])
    if data <> 'dict_page':
      t1 = t1 + data + ' = \'' + unicode(nsdata[data]) + '\', ' # UNICODE compile le code de t_prop
  t1 = t1 + '}\n' # ferme la table de t_prop
  return t1  

def wlms_table_pages(dict_page):
  t = 'p.t_pages = {\n'  # placer la chaine dans une variable
  for page in dict_page: # pour chaque page
    t = t + '{page = ' + str(page) + ', ' # compile clé et valeur
    page_prop = dict_page[page]           # le dictionnaire des proriétés de la page
    for i in page_prop:                   # pour chaque propriété
      #print (i)
      #print type(page_prop[i])
      if page_prop[i] == '':              # si la valeur est nulle
	t = t + str(i) + ' = \'\', '      # formate le code lua
      elif type(page_prop[i]) == list :   # si la valeur est une liste
	t = t + str(i) + ' = ' + wmls_list_to_lua(page_prop[i])
      elif i == 'date1': #AMELIORER type int on reconnait la date par le nom du param.
	t = t + str(i) + ' = \'' + str(page_prop[i]) + '\', '      # formate le code lua
      elif type(page_prop[i]) == dict :   # type = DICT
	#print type(page_prop[i])
	# sous-fonction ; ici on sait que le dict contient des listes
	# il faudrait tester le type de chaque valeur autre sous-fonction
	mydict = page_prop[i]
	for key in mydict:
	  v = mydict[key]
	  t = t + str(key) + ' = ' + wmls_list_to_lua(v) # Ce sont des listes
      else:                               # la clé contient une valeur
	t = t + str(i) + ' = ' + str(page_prop[i]) + ', '  # formate k, v
    t = t + wmls_table_next                                # fin de ligne
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

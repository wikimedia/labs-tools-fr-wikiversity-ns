#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Licence CeCill voir licence.txt

### Librairie de fonctions relatives aux espace de noms en général
### de la Wikiversité francophone en particulier
import pywikibot, re, sys
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

### This function wait the namespace id and do do a quick namespace scan 
### return total pages, redirections number, rootpages number, subpages numbers by level 1,2,more  
### scan pages properties: number of separators, redirection_target ; returned in a dict
def ns_prop(ns_id):
  gen_hlp = site.allpages(namespace=ns_id) #VARNAME gen_all
  Total, Redirection, Racine, sous_page= 0, 0, 0, 0 #, 0, 0
  resep = re.compile('/')
  dict_page = {}
  cible = ''
  for page in gen_hlp:
    cible = ''
    nb_sep = 0
    page_prop = []
    Total=Total+1
    redir = page.isRedirectPage()
    if redir == True:
	  cible= page.getRedirectTarget()
	  Redirection = Redirection +1
    regen = re.findall(resep, str(page))
    nb_sep = len(regen)
    if nb_sep<1 :
      Racine = Racine + 1      
    #elif nb_sep==1:
      #Sub1 = Sub1+1
    #elif nb_sep>1:
      #Sub2 = Sub2+1
    else:      
      sous_page = sous_page +1
    page_prop = [nb_sep, cible]
    dict_page[page] = page_prop
  verif = (Total-Racine-sous_page)
  prop=[Total, Redirection, Racine, sous_page, verif, dict_page, ns_id]
  return prop
### ns_list_page() reçoit le dictionnaire des pages associé aux propriétés
#   retourne le wikitexte contenant
#   un tableau triable des pages et leurs propriétés
### index, nom, nombre de separateur, cible si redirection
def ns_list_page(dict_page):
  index = 0
  witxt = '{|class="wikitable sortable"\n!Index\n!Nom\n!Nombre de separateurs\n!Cible'
  for page in sorted(dict_page):
    index = index + 1
    [nb_sep, cible] = dict_page[page]
    witxt = witxt +  u'\n|-\n|' + str(index) + '\n|' + unicode(page) + '\n|' + str(nb_sep) + '\n|' + unicode(cible)
  witxt = witxt + '\n|}'
  return witxt
### La fonction get_root() 
#   Isole les pages racines dans dict_racine, les sous-pages dans dict_sub
### Retourne un dictionnaire des pages root aves la liste des sous-pages associée
### ATTENTION fonction à déplacer/transcrire dans le(s) module(s) "Namespace vues"
dict_racine = {}
dict_sub = {}
def get_root(dict_page):
  for page in dict_page:
    page_prop = dict_page[page]
    nb_sep = page_prop[0]
    page = unicode(page)
    if nb_sep == 0:
      dict_racine[page] = page_prop
    else:
      dict_sub[page] = page_prop
  for racine in dict_racine:
    list_sub = []
    prefix = racine[:-2] # retire les crochets ]]
    for sub in dict_sub:
      if prefix in sub:
        list_sub.append(sub)
    dict_racine[racine] = list_sub
  for racine in dict_racine:
    list_sub = dict_racine[racine]
    #print len(list_sub)
    #for sub in list_sub:
      #print sub
  return dict_racine
### La fonction ecrit la liste des pages racines
#   nous avons besoin d'ecrire une page contenant un tableau pour les premières analyse
#   dans un second temps nous avons besoin d'ecrire une table sous forme de module Lua-Scribuntu
#   nous avons exclu le champs cible provisoirement (?)
### L'ideal serait une fonction qui ecrit une table Lua par défaut mais qui soit capable d'ecrire une page si param.
def write_list_root(dict_racine):
  index = 0
  witxt = '{|class="wikitable sortable"\n!Index\n!Nom\n!Nombre de sous-pages' #\n!Cible
  for racine in sorted(dict_racine):
    index = index + 1
    list_sub = dict_racine[racine]
    witxt = witxt +  u'\n|-\n|' + str(index) + '\n|' + unicode(racine) + '\n|' + str(len(list_sub)) #+ '\n|'  + unicode(cible)
  witxt = witxt + '\n|}'
  return witxt


### write_module() écrit un module vide
#
def write_module(module_name, lua_code): # Compiler tout le code du module au préalabe
  title = u'Module:'
  # UNICODE
  title = title + module_name
  comment = u'Nouveau module ajouté par l\'outil fr-wikiversity-ns sur tools.labs.org'
  module = 'local p = {}\n'
  module = module + lua_code
  module = module + '\nreturn p'
  page = pywikibot.Page(site, title)
  page.text = module
  page.save(comment) # TRY
  

### write_t_prop() écrit la table des propriétés de l'espace de noms
#   retourne une table au format clé = valeur
# 
def write_t_prop(ns_id, prop):
  [Total, Redirection, Racine, sous_page, verif, dict_page, ns_id] = prop #Rev.5
  t = 'p.t_prop = {'   # ' + str(ns_id) + ' ##  SIMPLIFICATION NECESSAIRE
  t = t + 'Total = ' + str(Total)  + ', '
  t = t + 'Redirection = ' + str(Redirection) + ', '
  t = t + 'Racine = ' + str(Racine) + ', '
  t = t + 'Sous_page = ' + str(sous_page) + ', '
  t = t + 'Identifiant = ' + str(ns_id) + ', '
  #t = t + 'Sub1 = ' + str(Sub1) + ', '
  #t = t + 'Sub2 = ' + str(Sub2) + ', '
  t = t + '}\n'
  return t

### write_t_pages() reçoit le dictionnaire Python 
#   pour le transformer en code Lua de la table t_pages
def write_t_pages(page_prop):
  t = 'p.t_pages = {\n'
  for page in page_prop:
    [nb_sep, cible] = page_prop[page]
    t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', ' + str(cible) + '},\n'
  t = t + '}\n'
  return t
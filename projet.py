#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re, sys
from namespaceLib import *

### Outil d'analyse et report de données sur l'espace de noms numero 4 Project-Wikiversité
### Licence CeCiLL voir Licence.txt

lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

prop = ns_prop(sys.argv[1])
[c, c_redir, c_racine, c1,c2, c3, verif, dict_page] = prop
print prop[0]
print prop[1]
print prop[2]
print prop[3]
print prop[4]
print prop[5]
print '-----'
print prop[6] 

page_prop = dict_page

title = u' Projet:Laboratoire/Espaces de noms/Wikiversité/'

### Isole les pages racines dans dict_racine
### les sous-pages dans dict_sub
dict_racine = {}
dict_sub = {}
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
  prefix = racine[:-2] # ]]
  for sub in dict_sub:
    if prefix in sub:
      list_sub.append(sub)
  dict_racine[racine] = list_sub

for racine in dict_racine:
  list_sub = dict_racine[racine]
  #print k
  print len(list_sub)
  for sub in list_sub:
    print sub

def ns_list_racine(dict_racine):
  index = 0
  witxt = '{|class="wikitable sortable"\n!Index\n!Nom\n!Nombre de sous-pages' #\n!Cible
  for racine in sorted(dict_racine):
    index = index + 1
    list_sub = dict_racine[racine]
    witxt = witxt +  u'\n|-\n|' + str(index) + '\n|' + unicode(racine) + '\n|' + str(len(list_sub)) #+ '\n|'  + unicode(cible)
  witxt = witxt + '\n|}'
  return witxt

witxt = ns_list_racine(dict_racine)
print witxt

title = title + 'Liste des pages'
comment = u'Ecrit la liste des pages racines de l\'espace de noms avec leur nombre sous-pages- youni_verciti_bot'
witxt = witxt + u'[[Catégorie:Laboratoire]]'
#print witxt # TEST
page = pywikibot.Page(site, title)
page.text = witxt
page.save(comment)  # ATTENTION
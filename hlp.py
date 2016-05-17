#!/usr/bin/env python
# -*- coding: utf-8  -*-

import pywikibot, re, sys
### Outil d'analyse et report de données sur l'espace de noms Aide de la Wikiversité francophone
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

# scan namespace return total, racines, sous-pages niveau 1 et 2,  
# scan pages prop redir, cible, 
def ns_prop(ns_id):
  gen_hlp = site.allpages(namespace=ns_id)
  c, c_redir, c_racine, c1, c2, c3= 0, 0, 0, 0, 0, 0
  resep = re.compile('/')
  dict_page = {}
  cible = ''
  for page in gen_hlp:
    cible = ''
    nb_sep = 0
    page_prop = []
    c=c+1
    redir = page.isRedirectPage()
    if redir == True:
	  cible= page.getRedirectTarget()
	  c_redir = c_redir +1
	  #print '###' + str(cible)
    regen = re.findall(resep, str(page))
    nb_sep = len(regen)
    if nb_sep<1 :
      c_racine = c_racine + 1      
    elif nb_sep==1:
      c1 = c1+1
    elif nb_sep>1:
      c2 = c2+1
    else:      
      c3 = c3 +1
    page_prop = [nb_sep, cible]
    dict_page[page] = page_prop
  verif = (c-c_racine-c1-c2-c3)
  prop=[c, c_redir, c_racine, c1,c2, c3, verif, dict_page]
  return prop
### ns_list_page() ettend un titre et un commentaire
#   retourne la page de titre indiqué contenant
#   un tableau triable des pages et leurs propriétés
### index, nom, nombre de separateur, cible si redirection SANS CATÉGORIE
def ns_list_page(title, comment):
  index = 0
  witxt = u'{{Titre| {{SUBPAGENAME}} }}\n'
  witxt = witxt + '{|class="wikitable sortable"\n!Index\n!Nom\n!Nombre de separateurs\n!Cible'
  for page in sorted(dict_page):
    index = index + 1
    [nb_sep, cible] = dict_page[page]
    #witxt = witxt + ''
    witxt = witxt +  u'\n|-\n|' + str(index) + '\n|' + unicode(page) + '\n|' + str(nb_sep) + '\n|' + unicode(cible)
  witxt = witxt + '\n|}'
  return witxt
prop = ns_prop(sys.argv[1])
print prop[0]
print prop[1]
print prop[2]
print prop[3]
print prop[4]
print prop[5]
print '-----'
print prop[6] 
dict_page = prop[7] #TUPLE
### LA fonction liste_page()
#   index, nom, cible, sp, (niv) niveau de profondeur de la sous-page
comment = u'Ecrit la liste des pages de l\'espace de noms Aide via hlp.py'
title = u' Projet:Laboratoire/Espaces de noms/Aide/Liste des pages ns'
title = title + sys.argv[1]

witxt = ns_list_page(title, comment)
witxt = witxt + u'[[Catégorie:Laboratoire]]'
#print witxt # TEST
page = pywikibot.Page(site, title)
page.text = witxt
page.save(comment)  # ATTENTION
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

dict_racine = get_root(dict_page)
witxt = write_list_root(dict_racine)
print witxt

title = title + 'Liste des pages'
comment = u'Ecrit la liste des pages racines de l\'espace de noms avec leur nombre sous-pages- youni_verciti_bot'
witxt = witxt + u'[[Catégorie:Laboratoire]]'
#print witxt # TEST
page = pywikibot.Page(site, title)
page.text = witxt
page.save(comment)  # ATTENTION
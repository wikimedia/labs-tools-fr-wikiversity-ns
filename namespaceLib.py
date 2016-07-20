#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Licence CeCill voir licence.txt

### Librairie de fonctions relatives aux espace de noms en général
### de la Wikiversité francophone en particulier
import pywikibot, re, sys
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

### This function wait the namespace id and do a quick namespace scan 
#   return total pages, redirections number, rootpages number, subpages numbers by level 1,2,more  
### scan pages properties: number of separators, redirection_target ; returned in a dict
def ns_prop(ns_id):
  allpages = site.allpages(namespace=ns_id) # , limit=250  #TEST # générateur de toutes les pages de l'espace
  Total, Redirection, Racine, sous_page= 0, 0, 0, 0 # initialise les prop de l'espace
  resep = re.compile('/')  # Regex pour le separateur de sous-pages
  dict_page = {}           # Initialise le dictionnaire principal des pages
  for page in allpages:       # Traitement de chaque page du generateur
    cible = ''                    # Initialise valeur pour cible de redirection
    nb_sep = 0                    # Initialise le nombre d eseparateur pour la page
    page_prop = []                # Initialise le LISTE des pages TRANFORMER EN TUPLE
    Total=Total+1                 # Compteur de page
    redir = page.isRedirectPage() # Test si la page est une redirection
    if redir == True:                # OUI
	  cible= page.getRedirectTarget()   # la cible devient la valeur redirigée
	  Redirection = Redirection +1      # compteur de redirections
    regen = re.findall(resep, str(page)) # Cherche tous les separateurs dans le nom de la page
    nb_sep = len(regen)                  # determine le nombre de separateurs
    if nb_sep<1 :   # Pas de separateur
      Racine = Racine + 1      # Compteur de pages racines
    else:           # Separateur
      sous_page = sous_page +1 # Compteur de sous-pages
    date = '' #TEST
    page_prop = [nb_sep, date, cible]  # TRANFORMER EN TUPLES
    dict_page[page] = page_prop  # LISTE contenant 2 LISTES
  verif = (Total-Racine-sous_page) # voir calc man dpt
  prop=[Total, Redirection, Racine, sous_page, verif, dict_page, ns_id]
  return prop

### write_module() écrit un module vide
#
def write_module(module_name, lua_code): # Compiler tout le code du module au préalabe
  title = u'Module:' # UNICODE
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
def write_t_prop(ns_id, prop):
  [Total, Redirection, Racine, sous_page, verif, dict_page, ns_id, ns_label, lang] = prop #Rev.5
  t = 'p.t_prop = {'   #  Ajouter LANG
  t = t + 'Identifiant = ' + str(ns_id) + ', '
  t = t + 'lang = \'' + lang + '\', '          # ATTENTION variables Lua
  t = t + 'Label = \'' + ns_label + '\', '
  t = t + 'Total = ' + str(Total)  + ', '
  t = t + 'Racine = ' + str(Racine) + ', '
  t = t + 'Sous_page = ' + str(sous_page) + ', '
  t = t + 'Redirection = ' + str(Redirection) + ', '
  t = t + '}\n'
  #t = unicode(t)
  return t

### write_t_pages() reçoit le dictionnaire des pages
#   pour le transformer en code Lua de la table t_pages
def write_t_pages(dict_page):
  t = 'p.t_pages = {\n'
  for page in dict_page:
    [nb_sep, date, cible] = dict_page[page]
    #t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', ' + str(cible) + '},\n'
    t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', date1 = \'' + str(date) + '\', ' + str(cible)  + '},\n'
    # cible en dernier
  t = t + '}\n'
  t = unicode(t, 'utf_8')
  return t

### cdate() attend un dictionnaire
#   retourne la date de creation de chaque page

############### VIEUX CODE
#### La fonction get_root() reçoit le dictionnaire des pages
##   Isole les pages racines dans dict_racine, les sous-pages dans dict_sub
#### Retourne un dictionnaire des pages root avec la liste des sous-pages associée
#### ATTENTION fonction à déplacer/transcrire dans le(s) module(s) "Namespace vues"
#dict_racine = {}
#dict_sub = {}
#def get_root(dict_page):
  #for page in dict_page:
    #page_prop = dict_page[page]
    #nb_sep = page_prop[0]
    #page = unicode(page)
    #if nb_sep == 0:
      #dict_racine[page] = page_prop
    #else:
      #dict_sub[page] = page_prop
  #for racine in dict_racine:
    #list_sub = []
    #prefix = racine[:-2] # retire les crochets ]]
    #for sub in dict_sub:
      #if prefix in sub:
        #list_sub.append(sub)
    #dict_racine[racine] = list_sub
  #for racine in dict_racine:
    #list_sub = dict_racine[racine]
    ##print len(list_sub)
    ##for sub in list_sub:
      ##print sub
  #return dict_racine

#### La fonction ecrit la liste des pages racines
##   nous avons besoin d'ecrire une page contenant un tableau pour les premières analyse
##   dans un second temps nous avons besoin d'ecrire une table sous forme de module Lua-Scribuntu
##   nous avons exclu le champs cible provisoirement (?)
#### L'ideal serait une fonction qui ecrit une table Lua par défaut mais qui soit capable d'ecrire une page si param.
#def write_list_root(dict_racine):
  #index = 0
  #witxt = '{|class="wikitable sortable"\n!Index\n!Nom\n!Nombre de sous-pages' #\n!Cible
  #for racine in sorted(dict_racine):
    #index = index + 1
    #list_sub = dict_racine[racine]
    #witxt = witxt +  u'\n|-\n|' + str(index) + '\n|' + unicode(racine) + '\n|' + str(len(list_sub)) #+ '\n|'  + unicode(cible)
  #witxt = witxt + '\n|}'
  #return witxt

#### ns_list_page() reçoit le dictionnaire des pages associé aux propriétés
##   retourne le wikitexte contenant un tableau triable des pages et leurs propriétés
#### index, nom, nombre de separateur, cible si redirection
#def ns_list_page(dict_page):
  #index = 0
  #witxt = '{|class="wikitable sortable"\n!Index\n!Nom\n!Nombre de separateurs\n!Cible'
  #for page in sorted(dict_page):
    #index = index + 1
    #[nb_sep, cible] = dict_page[page]
    #witxt = witxt +  u'\n|-\n|' + str(index) + '\n|' + unicode(page) + '\n|' + str(nb_sep) + '\n|' + unicode(cible)
  #witxt = witxt + '\n|}'
  #return witxt
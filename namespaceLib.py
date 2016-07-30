#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Licence CeCill voir licence.txt

### Librairie de fonctions relatives aux espace de noms en général
### de la Wikiversité francophone en particulier
import pywikibot, re   ###, sys
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family)  

### This function wait the namespace id and do a quick namespace scan 
#   return total pages, redirections number, rootpages number, subpages numbers ,  
### and the liste of pages including number of separators, redirection_target ; returned in a dict
def ns_prop(ns_id):
  allpages = site.allpages(namespace=ns_id) # , limit=250  #TEST # générateur de toutes les pages de l'espace
  Total, Redirection, Racine, sous_page= 0, 0, 0, 0 # initialise les prop de l'espace
  resep = re.compile('/')     # Regex pour le separateur de sous-pages
  dict_page = {}              # Initialise le dictionnaire principal des pages
  for page in allpages:       # Traitement de chaque page du generateur
    cible = '\'non\''             # Initialise valeur pour cible de redirection
    nb_sep = 0                    # Initialise le nombre d eseparateur pour la page
    page_prop = []                # Initialise le LISTE des pages TRANFORMER EN TUPLE
    Total=Total+1                 # Compteur de page
    redir = page.isRedirectPage()    # Test si la page est une redirection
    if redir == True:                # OUI
      cible= page.getRedirectTarget()    # la cible devient la valeur redirigée
      Redirection = Redirection +1       # compteur de redirections
    regen = re.findall(resep, str(page)) # Cherche tous les separateurs dans le nom de la page
    nb_sep = len(regen)                  # determine le nombre de separateurs
    if nb_sep<1 :              # Pas de separateur
      Racine = Racine + 1      # Compteur de pages racines
    else:                      # Separateur
      sous_page = sous_page +1 # Compteur de sous-pages
    date = '' #TEST 
    page_prop = [nb_sep, date, cible]  # TRANFORMER EN TUPLES
    dict_page[page] = page_prop        # LISTE contenant 2 LISTES
  verif = (Total-Racine-sous_page)     # voir calc man dpt
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
  return t

### write_t_pages() reçoit le dictionnaire des pages
#   pour le transformer en code Lua de la table t_pages
def write_t_pages(dict_page):
  t = 'p.t_pages = {\n'
  for page in dict_page:
    [nb_sep, date, cible] = dict_page[page]
    t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', date1 = \'' + str(date) + '\', cible = ' + str(cible)  + ',},\n'
  t = t + '}\n'
  t = unicode(t, 'utf_8')
  return t

def write_t_pages2(dict_page): # POUR NS FACULTES
  t = 'p.t_pages = {\n'
  for page in dict_page:
    [nb_sep, date, cible, list_dpt, n_dpt] = dict_page[page]
    code_dpt = list_to_lua(list_dpt)
    t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', date1 = \'' + str(date) + '\',  cible = ' + str(cible)  + ', n_dpt = ' + str(n_dpt) + ', ldpt = ' + str(code_dpt) +'},\n'
  t = t + '}\n'
  t = unicode(t, 'utf_8')
  return t

def write_tableau(dpt_fac): # POUR NS FACULTES inverted dict
  t = 'p.t_fac_dpt = {\n'
  for page in dpt_fac:
    [cible, l_fac] = dpt_fac[page]
    l_code = list_to_lua(l_fac)  
    t = t + '{page = ' + str(page) + ', nb_fac = ' + str(len(l_fac)) + ', cible = ' + str(cible)  + ', l_fac = ' + str(l_code) +'},\n'
  t = t + '}\n'
  t = unicode(t, 'utf_8')
  return t

def write_dpt(dict_page): # Table des departements
  t = 'p.t_pages = {\n'
  for page in dict_page:
    [nb_sep, date1, cible, lsp, d_lesson] = dict_page[page]
    t = t + '    {page = ' + str(page) + ', nsep =' + str(nb_sep) + ', date1 = \'' + str(date1) + '\',  cible = ' + str(cible)  + ', '
    l_code = ''
    l_code = l_code + list_to_lua(lsp)  # sous-fonction compile le code lua 
    t = t + 'lsp = ' + l_code 
    d_code = ''
    for k in d_lesson:
      v = d_lesson[k]
      d_code = d_code + k + ' = ' + list_to_lua(v)
    t = t + d_code + '},\n'  # ferme la table de la page
  t = t + '}\n'                           # ferme la table des departements
  t = unicode(t, 'utf_8')                 # converti Uicode
  return t
    
  
def prefix(p, lang, label):
  prefixed = lang + ':' + label + ':' + p
  return prefixed
  
def list_to_lua(l):
  code = '{'
  for i in l:
    code = code + str(i) + ', '
  code = code + '}, \n'
  return code

### get_root()
#   La fonction get_root() reçoit le dictionnaire des pages
#   Isole les pages racines dans dict_racine, les sous-pages dans dict_sub
#   Retourne un dictionnaire des pages root avec la liste des sous-pages associées
### ATTENTION fonction transcrite dans le(s) module(s) "Namespace vues"
### ATTENTION Vérifier la présence d'orphelines
def merge_sub(mydict):
  dict_racine = {}   # Dictionnaire des pages racines
  dict_sub = {}      # Dictionnaire des sous-pages
  for page in mydict:
    page_prop = mydict[page]
    nb_sep = page_prop[0]
    if nb_sep == 0:
      dict_racine[page] = page_prop
    else:
      dict_sub[page] = page_prop
  merged = [dict_racine, dict_sub]  # LISTE reçoit les deux dictionnaires précedents
  return merged 
    
def root_sub(merged):
  [dict_racine, dict_sub] = merged
  dict_root_sub = {}
  for racine in dict_racine:   # Pour chaque page du dictionnaire racine
    page_prop = dict_racine[racine]
    list_sub = []                  # liste des sous-pages pour chaque racine
    str_racine = str(racine)       # converti en string
    prefix = str_racine[:-2]       # retire les crochets ]] avant comparaison
    for sub in dict_sub:           # pour chaque sous-page
      str_sub = str(sub)           # converti en string
      if prefix in str_sub:        # si le prefixe est present
        list_sub.append(sub)       # ajoute la page à la liste
    page_prop.append(list_sub)     # ajoute la liste des sous-pages aux propriété
    dict_root_sub[racine] = page_prop  # ajoutes les propriétés à la page racine
  return dict_root_sub

def get_linked_p(source_p, ns): # collecte les pages liées vers ns sur la page source
  gen = source_p.linkedPages(namespaces=ns)   # génère la liste des dpt à patir de la page fac
  return gen                # retourne le générateur

def get_target(page):
  redir = page.isRedirectPage()
  cible = ''
  if redir == True:
      cible = page.getRedirectTarget()
  return cible
#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Licence CeCill voir licence.txt

### Librairie de fonctions relatives aux espace de noms en général
### de la Wikiversité francophone en particulier
import pywikibot, re   ###, sys
lang = 'fr'       
family = 'wikiversity'
site = pywikibot.Site(lang, family) 



## Determiner si la page est une sous-page documentation sinon determiner si la page dispose d'une documentation
def is_doc(dict_page) :
  for page in dict_page :
    page_prop = dict_page[page] # Chercher si existe variable locale pour '~/Documentation'
    motif = '/Documentation'    # Pour améliorer il faudrait importer re
    str_page = str(page)        # mais il reste le cas des documentations
    s = str_page[:-2]           # avec des noms différents
    is_doc = False
    if motif in s :             # mieux vaut s'en tenir au label exact
      is_doc = True # T majuscule
    page_prop['is_doc'] = is_doc 

def have_doc(dict_page) : # Determine si la page n'etant pas une documentation, dispose d'une sous-page /Documentation
  #c = 0 ·Debug
  motif = u'/Documentation'    # suivi du motif
  for page in dict_page :   # Itération du dictionnaire
    #c = c+1 #DEBUG
    u_page = unicode(page)  # format unicode
    u_page = u_page[:-2]    # chaine sans les 2 crochets
    have_doc = False        # déclaration booléen
    page_prop = dict_page[page] # Déclaration des propriétés de la page
    #print page_prop['nsep'] #Debug
    if not page_prop['is_doc'] : # Si la page n'est pas une documentation
      #print c    #Debug
      #print page #Debug
      for doc in dict_page :      # Itération du dictionnaire à la recherche de sp doc
	u_doc = unicode(doc)      # titre uicode pour page documentation
	doc_prop = dict_page[doc] # Propriétés de la page documentation
	if doc_prop['is_doc'] :   # Test si la page est une documentation
	  if u_page + motif == u_doc[:-2] : # Compare les titres 
	    #print u_doc #Debug
	    have_doc = True                 # La page dispose d'une /Documentation
	    own_doc  = doc                  # stock objet Page de la doc
    page_prop['have_doc'] = have_doc # Affecte la variable au dictoionnaire
    if page_prop['have_doc'] :       # Si la page dispose d'une documentation
      page_prop['own_doc'] = own_doc   # affecte la propriété own_doc

### Cherche les liens contenus dans la sous-page
#   Reçoit l'objet page, la chaine de la sous-page et le numero de l'espace de noms 
#   de destination des liens. Retourne une liste.
#   (0 principal, 104 Rch, 108 Dpt) fac.py - dpt.py - rch.py
def check_link_in_subpage(page, sub, nsid): # sub contient le nom de la sous-page
  title = str(page)                  # Convertit en sub
  title = title[2:-2] + sub          # ajoute les crochets
  title = unicode(title, 'utf-8')    # Convertit en unicode
  page  = pywikibot.Page(site, title) # Créé un objet page PWB 
  links = [] # il faut une liste même vide pour certains calculs
  exist = page.exists()              # Test si la page existe
  if exist:
    links = get_linked_p(page, nsid) # titre de la page et namespace id RECUPERER le numero en argument
    links = list(links)              # convertit le générateur en liste python
  return links # retourner une LISTE 
  
### Collecte les dates de 1ere revision
#   place le timestamp dans la clé 'date1'
def ns_get_date(dict_page, prefix_list, label):
  for page in dict_page:
    name = unicode(page)
    page_prop = dict_page[page]        # déclare la liste de propriétés de la page
  #[nb_sep, date, cible] = page_prop
  # La liste des pages dont on souhaite collecter la date de creation
    for groupe in prefix_list:               # Pour chaque prefix de pages à traiter
      groupe = prefix(groupe, lang, label)   # construit le prefixe à partir du nom du prefix
    for groupe in prefix_list:               # Pour chaque prefix de la liste
      if unicode(groupe) in name:
        first_rev = page.oldest_revision # genère un tuple contenant les info. de la première revision
        get_date = first_rev.timestamp   # copie la valeur date et heure de création
        page_prop['date1'] = get_date          # place la date dans la liste à l'indice correspondant

### NOUVELLE FONCTION (remplace ns_prop)
#   utilise un dictionnaire pour prop
#   utilise un dictionnaire pour page_prop
def ns_collect_data(ns_id):
  ns_label = site.namespace(ns_id) # Label local du namespace
  allpages = site.allpages(namespace=ns_id) #, limit=30)  #TEST # générateur de toutes les pages de l'espace
  total, redirection, racine, sous_page= 0, 0, 0, 0 # initialise les prop de l'espace
  resep = re.compile('/')     # Regex pour le separateur de sous-pages
  dict_page = {}              # Initialise le dictionnaire principal des pages
  for page in allpages:       # Traitement de chaque page du generateur
    #cible = '\'non\''             # Initialise valeur pour cible de redirection
    cible = '' #MAJ
    nb_sep = 0                    # Initialise le nombre de separateur pour la page
    #page_prop = {}                
    total=total+1                 # Compteur de page
    redir = page.isRedirectPage()    # Test si la page est une redirection
    if redir == True:                # OUI
      cible= page.getRedirectTarget()    # la cible devient la valeur redirigée
      redirection = redirection + 1       # compteur de redirections
    regen = re.findall(resep, str(page)) # Cherche tous les separateurs dans le nom de la page
    nb_sep = len(regen)                  # determine le nombre de separateurs
    if nb_sep<1 :              # Pas de separateur
      racine = racine + 1      # Compteur de pages racines
    else:                      # Separateur
      sous_page = sous_page +1 # Compteur de sous-pages
    date = '' #TEST MAUVAISE SOLUTION
    page_prop = {}  # # Initialise DICTIONNAIRE propriétés de pages
    page_prop['nsep'] = nb_sep
    page_prop['date1'] = date
    page_prop['cible'] = cible
    dict_page[page] = page_prop        # DICTIONARY
  verif = (total-racine-sous_page)     # voir calc man dpt
  prop = {}
  prop['id'] = ns_id
  prop['lang'] = lang
  prop['label'] = ns_label
  prop['total'] = total
  prop['redirection'] = redirection
  prop['racine'] = racine
  prop['sous_page'] = sous_page
  prop['dict_page'] = dict_page
  prop['verif'] = verif
  return prop

  
def prefix(p, lang, label): # DOCUMENTER AMELIORER
  prefixed = lang + ':' + label + ':' + p
  return prefixed

def get_linked_p(source_p, ns):              # collecte les pages liées vers ns sur la page source
  gen = source_p.linkedPages(namespaces=ns)  # génère la liste des dpt à patir de la page fac
  return gen                                 # retourne le générateur

def get_target(page):
  redir = page.isRedirectPage()
  cible = ''
  if redir == True:
      cible = page.getRedirectTarget()
  return cible

### AMELIORER spécifique lsp l_sp/n_sp pas collecté pour les facultés
### UNIQUEMENT POUR DPT:PY
#   Ajoute la liste des sous-pages aux propriétés des pages racines
def get_sub_list(splited_dicts):          # Reçoit les dictionnaires root et sub
  [dict_racine, dict_sub] = splited_dicts # Extrait les dictionnaires 
  dict_root_sub = {}               # Initialise root/sub dict
  for racine in dict_racine:       # Pour chaque page du dictionnaire racine
    page_prop = dict_racine[racine]# Extrait les propriétés
    list_sub = []                  # initialise liste des sous-pages pour chaque racine
    str_racine = str(racine)       # converti en string
    prefix = str_racine[:-2]       # retire les crochets ]] avant comparaison
    for sub in dict_sub:           # pour chaque sous-page
      str_sub = str(sub)           # converti en string
      if prefix in str_sub:        # si le prefixe est present
        list_sub.append(sub)       # ajoute la page à la liste
    page_prop['l_sub'] = list_sub      # ajoute la liste des sous-pages aux propriétés MAJ l_sub = lsp
    page_prop['n_sub'] = len(list_sub) # ajout nombre de sous-pages MAJ 
    dict_root_sub[racine] = page_prop  # ajoutes les propriétés à la page racine
  return dict_root_sub             # Retourne le dictionnaire root/sub

### MODIFIER voir dpt.py
#   Scinde les pages racine et sous pages
#   lit le dictionnaire des pages analyse le nombre de separateurs
def split_root(mydict): # RENOMMER SPLIT_ROOT(ns_dict, |sub)
  dict_racine = {}      # Dictionnaire des pages racines
  dict_sub = {}         # Dictionnaire des sous-pages
  for page in mydict:   # Pour chaque page
    page_prop = mydict[page] # Déclare les propriétés de la page
    # nsep = page_prop['nsep'] # Vérifier
    if page_prop['nsep'] == 0:
      dict_racine[page] = page_prop
    else:
      dict_sub[page] = page_prop
  # Retourner root par defaut ou sub si option=sub
  splited_dicts = [dict_racine, dict_sub]  # LISTE reçoit les deux dictionnaires précedents
  return splited_dicts # retourner 


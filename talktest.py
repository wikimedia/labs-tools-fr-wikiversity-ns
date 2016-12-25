### CODE POUR SUPERVISION ESPACES DE DISCUSSION
ns_talk_id = ns_id + 1 # Identifiant de l'espace de discussion
### Collect data DISCUSSIONS NAMESPACES
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de discussion
talk_dict = nstalk['dict_page']       # Dictionnaire des pages de discussion 
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(talk_dict, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code des tables
talk_module_name = u'ns_' + nstalk['label']  # Nom du module pour l'espace discussion relatif
#   Write
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion

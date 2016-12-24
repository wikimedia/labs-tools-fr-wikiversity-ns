### CODE POUR SUPERVISION ESPACES DE DISCUSSION
### Collect data DISCUSSIONS NAMESPACES
ns_talk_id = ns_id + 1
nstalk = ns_collect_data(ns_talk_id)  # Scan l'espace de noms VERSION 2
dict_page = nstalk['dict_page']       # 
#   Talk tables
talk_prop_code   = wlms_table_prop(ns_id, nstalk)     # la table des propriétés de l'espace discussion
talk_pages_code  = wlms_table(dict_page, 'talkpages') # la table des pages de discussion
lua_talk_code    = talk_prop_code + talk_pages_code   # Concatener le code Lua
talk_module_name = u'ns_' + nstalk['label']  # enregistre le module de l'espace discussion relatif
#   Write
write_module_lua(talk_module_name, lua_talk_code) # Ecriture des tables de l'espace discussion

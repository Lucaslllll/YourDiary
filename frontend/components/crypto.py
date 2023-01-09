from kivy.storage.jsonstore import JsonStore


store = JsonStore("config.json")
if store.exists('credential'):
    USERNAME = store.get('credential')['USERNAME'] 
    PASSWORD = store.get('credential')['PASSWORD']
else:
	USERNAME = None
	PASSWORD = None

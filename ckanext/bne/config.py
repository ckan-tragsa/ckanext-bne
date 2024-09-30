# Vars and configs for ckanext-bne

bne_base_url = "https://www.bne.es/"
bne_api_base_url = "http://172.17.9.151:3000/api/"
bne_api_tables = {'Geográfico': 'geo',
                'Persona': 'per',
                'Monografías modernas': 'mon',
                'Monografías antiguas': 'moa',
                'Entidades': 'ent',
                'Manuscritos': 'mss',
                'Prensa y Revista': 'ser'
                }
bne_api_pill_style = {'Geográfico': {'icon':'fas fa-atlas'},
                'Persona': {'icon':'fas fa-user'},
                'Monografías modernas': {'icon':'fas fa-book'},
                'Monografías antiguas': {'icon':'fas fa-book-open'},
                'Entidades': {'icon':'fas fa-university'},
                'Manuscritos': {'icon':'fas fa-feather-alt'},
                'Prensa y Revista': {'icon':'fas fa-newspaper'}
                }
bne_api_pill_style_auto = {'r':[0,128] ,'g':[0,128] ,'b':[0,128]}
bne_api_entries = 10
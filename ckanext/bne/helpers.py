import logging
import re
import json
from functools import lru_cache

from ckan import model
import ckan.logic as logic
import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import requests as req
from urllib.parse import urlparse, unquote

#import ckanext.bne.config as bne_config


log = logging.getLogger(__name__)

all_helpers = {}

def helper(fn):
    """Collect helper functions into the ckanext.schemingdcat.all_helpers dictionary.

    Args:
        fn (function): The helper function to add to the dictionary.

    Returns:
        function: The helper function.
    """
    all_helpers[fn.__name__] = fn
    return fn

@helper
def bne_get_api_entries():
    """
    Retrieves default number of entries to display from config
    """
    return p.toolkit.config.get('ckanext.bne.bne_api_entries')

@helper
def bne_get_bne_base_url():
    """
    Retrieves the BNE base URL.

    Returns:
        str: The URL.
    """
    return p.toolkit.config.get('ckanext.bne.bne_url')

@helper 
def bne_get_bne_api_base_url():
    """
    Retrieves the BNE base URL.

    Returns:
        str: The URL.
    """
    return p.toolkit.config.get('ckanext.bne.bne_api_base_url')

@helper
def get_number_entries_api():
    '''
    Returns:
        int: number of entries that should appear in api frontend
    '''
    return p.toolkit.config.get('ckanext.bne.bne_api_entries')

@helper
def get_googleanalytics():
    '''
    Returns:
        string: google analytics ID
    '''
    return p.toolkit.config.get('ckanext.bne.bne_googleanalytics')

@helper
def get_bne_placeholder():
    '''
    Returns:
        string: search bar placeholder
    '''
    return p.toolkit.config.get('ckanext.bne.bne_placeholder')
    
@helper 
def bne_get_pills():
    """
    gets table fields and sets up and gives it a color within a given range defined in config.py

    Returns:
        dict: dictionary with table name, title, and a pseudorandom asigned color 
    """
    pill_config = json.loads(p.toolkit.config.get('ckanext.bne.bne_api_mapping'))
    out = {}
    for key in pill_config:
        out[key] =  {'table':pill_config[key]['table'],
                     'icon':pill_config[key]['icon'],
                     'color':pill_config[key]['color']}
    return out

@helper
def bne_get_pages():
    """
    Retrieves visible pages in the database

    Returns:
        dict: pages
    """
    page_list = tk.get_action("ckanext_pages_list")(data_dict={'order':'true'})
    #log.warning(page_list)
    return page_list

@helper
def bne_get_blog():
    """
    Retrieves blog entries

    Returns:
        dict: blog
    """

    page_list = tk.get_action("ckanext_pages_list")(data_dict={'page_type':'blog'})
    #log.warning(page_list)
    return page_list[:5]


def _bne_humanize_field_name(field_name):
    """
    Converts a field name to a more human-readable format.
    Example: 'obras_relacionadas_en_el_catalogo_BNE' -> 'Obras relacionadas en el catalogo BNE'
    Example: 'id' -> 'ID'
    """
    # Replace underscores with spaces
    humanized = re.sub(r'_', ' ', field_name)
    # Capitalize the first word and keep the rest lowercase
    humanized = humanized.capitalize()
    # If the field name is two letters, make it uppercase
    if len(field_name) == 2:
        humanized = field_name.upper()
    return humanized

@helper
def bne_standarize_entry(entry):
    """
    Clean dataset and standardize the tables for display 

    Returns:
        dict: dictionary with title and content
    """
    entry_std = {}
    
    # Remove marc21 entries to make it easier to read and use
    entry_aux = entry.copy()
    for key in entry_aux:
        if key[0:2] == "t_":
            entry.pop(key)
    
    # Standardize field names
    entry_std['content'] = { _bne_humanize_field_name(k): v for k, v in entry.items() }

    return entry_std

@helper 
def generate_api_url(params, fields=False, rows=None, page=None):
    """
    Generates API URL from params.

    Args:
        params (dict): The parameters to be sent to the API.
        fields (bool): If True, returns table fields. Defaults to False.
        rows (int, optional): The number of rows to limit the query. Defaults to None.
        page (int, optional): The page number for pagination. Defaults to None.

    Returns:
        str: A URL.
    """
    params2 = params.copy()
    params2.pop('nentries', None)
    
    if fields:
        call_url = p.toolkit.config.get('ckanext.bne.bne_api_base_url') + "/api/"  + "fields/" + params2.pop('table') + "?"
    else:
        call_url = p.toolkit.config.get('ckanext.bne.bne_api_base_url') + "/api/"  + params2.pop('table') + "?"
    
    for key in params2:
        call_url += key + "=" + params2[key] + '&'
    
    if rows is not None and page is not None:
        call_url += f"rowid={rows}-{page}"
    
    return call_url

@lru_cache(maxsize=128)
@helper
def bne_call_api(params, fields=False):
    """
    Calls the BNE API and returns the requested elements.

    Args:
        params (dict): The parameters to be sent to the API.
        fields (bool): If True, returns table fields. Defaults to False.

    Returns:
        dict: The response from the API. If `fields` is False, the response
              includes standardized entries and all possible fields. If an
              error occurs, returns a dictionary with an empty 'data' list.
    """
    call_url = generate_api_url(params, fields)

    try:
        r = req.get(call_url)
        data = r.json()
        
        if not fields:
            # Recopilar todos los campos posibles
            all_fields = set()
            for entry in data.get('data', []):
                std = bne_standarize_entry(entry)
                all_fields.update(std['content'].keys())

            # Asegurarse de que cada entrada tenga todos los campos posibles
            for entry in data.get('data', []):
                std = bne_standarize_entry(entry)
                for field in all_fields:
                    if field not in std['content']:
                        std['content'][field] = ''
                entry['standardized'] = std

            # Añadir todos los campos posibles a los datos
            data['all_fields'] = [_bne_humanize_field_name(field) for field in all_fields]

        return data
    except Exception as e:
        log.warning('Bad API response: %s', e)
        return {'data': []}



@helper
def get_params():
    """
    Extracts query parameters from the current URL.

    Returns:
        dict: A dictionary containing the query parameters.
    """
    params = {}
    
    for entry in unquote(urlparse(h.current_url()).query).split('&'):
        try:
            log.warning(entry)
            key_pair = entry.split('=')
            if len(key_pair) == 2:
                params[key_pair[0]] = key_pair[1]
        except ValueError as e:
            log.error(f"ValueError while parsing entry '{entry}': {e}")
        except Exception as e:
            log.error(f"Unexpected error while parsing entry '{entry}': {e}")
    
    return params


@helper
def bne_get_params_api(default={'table':'geo'}, rows= get_number_entries_api()):
    '''
    Returns:
        dict: query param data, adapted for the usage with the api 
    '''
    params = get_params()

    #inject default values if needed 
    for key in default:
        if key not in params:
            params[key] = default[key]  
    return params



@helper 
def bne_url_for_static_or_external(url:str):
    """
    fix of url_for_static_or_external() for great_view
    adds '/uploads/showcase/' to the URL if it's internal
    """
    if 'https' == url[0:5] or 'http:' == url[0:5]:
        return h.url_for_static_or_external(url)
    else:
        return h.url_for_static_or_external('/uploads/showcase/' + url)

@helper
def bne_get_featured_datasets(count=5):
    """
    Retrieves a specified number of featured datasets from the CKAN instance.
    
    Parameters:
    count (int): Number of featured datasets to retrieve. Default is 5.
    
    Returns:
    list: A list of dictionaries, each representing a featured dataset.

    This function uses json.loads to parse JSON-encoded strings received from the API for fields such as 'title_translated' and 'notes_translated'.
    """
    fq = '+featured:true'
    search_dict = {
        'fq': fq,
        'sort': 'metadata_modified desc',
        'fl': 'name, extras_title_translated, extras_notes_translated, metadata_modified, extras_featured_image',
        'rows': count
    }
    context = {'model': model, 'session': model.Session}
    result = logic.get_action('package_search')(context, search_dict)

    datasets = result.get('results', [])
    for dataset in datasets:
        # Parse 'extras_title_translated' and 'extras_notes_translated' fields
        for field in ['title_translated', 'notes_translated']:
            value = dataset.get(field)
            dataset[field] = json.loads(value) if value else {}

    return datasets

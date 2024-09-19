import logging

import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import requests as req
import random 
from urllib.parse import urlparse, unquote

import ckanext.bne.config as bne_config


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
def bne_get_bne_base_url():
    """
    Retrieves the BNE base URL.

    Returns:
        str: The URL.
    """
    return bne_config.bne_base_url

@helper
def bne_get_showcase_datasets():
    """
    Retrieves showcase datasets in the database

    Returns:
        dict: datasets
    """
    showcase_list = tk.get_action("ckanext_showcase_list")()
    return showcase_list

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
def bne_shorten_text(text,n):
    """
    shortens text length to n characters

    Returns:
        str: length limited string
    """
    if len(text) > n:
        text = text[0:n]
        text += "..>>"
    return text

@helper
def bne_call_api(params, fields = False):
    """
    Calls the BNE api
    if fields = True it returns table fields

    Returns:
        dict: requested elements
    """
    if fields:
        call_url = bne_config.bne_api_base_url+"fields/"+params.pop('table')+"?"
    else:
        call_url = bne_config.bne_api_base_url+params.pop('table')+"?"
    for key in params:
        call_url += key +"="+params[key]+'&'

    try:
        r = req.get(call_url)
        return r.json()
    except:
        log.warning('Bad API response')


@helper
def get_params():
    '''
    Returns:
        get query param data
    '''
    params = {}
    
    for entry in unquote(urlparse(h.current_url()).query).split('&'):
        #catch and ignore any exception while parsing the query params
        #app should not crash after inputing a wrong format
        try:
            log.warning(entry)
            key_pair = entry.split('=')
            params[key_pair[0]] = (key_pair[1])
        except:
            pass
    return params

@helper
def get_number_entries_api():
    '''
    Returns:
        int: number of entries that should appear in api frontend
    '''
    return bne_config.bne_api_entries

@helper
def get_params_api(default={'table':'geo', 'page':'0'}, rows= get_number_entries_api()):
    '''
    Returns:
        dict: query param data, adapted for the usage with the api 
    '''
    params = get_params()

    #inject default values if needed 
    for key in default:
        if key not in params:
            params[key] = default[key]  
    page = params.pop('page')
    params['rowid'] = str(rows)+'-'+str(page)
    return params
    

@helper
def bne_standarize_entry(entry):

    """
    clean dataset and standarize the tables for display 

    Returns:
        dict: dictionary with title and content
        
    """
    entry_std = {}

    if 'nombre_de_persona' in entry:
        entry_std["title"] = entry.pop('nombre_de_persona')

    elif 'nombre_de_lugar' in entry:
        entry_std["title"] = entry.pop("nombre_de_lugar")
    
    #remove marc21 entries to make it easier to read and use
    entry_aux = entry.copy()
    for key in entry_aux:
        if key[0:2] == "t_":
            entry.pop(key)
        
    entry_std['content'] = entry

    return entry_std


@helper 
def bne_get_pills(r=[0,255],g=[0,255],b=[0,255]):
    """
    r = range for red
    g = range for green
    b = range for blue
    gets table fields and sets up and gives it a color within a given range

    Returns:
        dict: dictionary with table name, title, and a pseudorandom asigned color 
    """
    out = {}
    for key in bne_config.bne_api_tables:
        random.seed(key)
        color_int = [random.randint(r[0],r[1]),random.randint(g[0],g[1]),random.randint(b[0],b[1])]
        out[key] =  {'table':bne_config.bne_api_tables[key],
                     'color':'#'+ bytes(color_int).hex()}
    return out

## Helpers out of ckanext-surrey
# TODO test every helper to check if they work correctly in the newer ckan/python version
# currently unused, migth remove 


@helper
def get_group_list():
    """
    Retreives the group list 

    returns:
        list: List of groups
    """
    groups = tk.get_action('group_list')(
        data_dict={'all_fields': True})

    return groups


@helper
def get_summary_list(num_packages):    
    """
    Retreives a summary of n packages ordered by recently added

    returns:
        list: List of packages
    """
    list_without_summary = \
    tk.get_action('package_search')(data_dict={'rows': num_packages, 'sort': 'metadata_modified desc'})['results']
    list_with_summary = []
    for package in list_without_summary:
        list_with_summary.append(tk.get_action('package_show')(
            data_dict={'id': package['name'], 'include_tracking': True})
        )
    return list_with_summary

@helper
def get_visit_summary_list(num_packages):
    """
    Retreives a summary of packages ordered by times visited

    returns:
        list: List of packages
    """
    list_without_summary = tk.get_action('package_search')(data_dict={'rows':num_packages,'sort':'views_recent desc'})['results']
    list_with_summary = []
    for package in list_without_summary:
        list_with_summary.append(tk.get_action('package_show')(
        data_dict={'id':package['name'],'include_tracking':True})
        )
    return list_with_summary
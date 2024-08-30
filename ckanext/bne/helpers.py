import logging

import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk

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

## Helpers out of ckanext-surrey
# TODO test every helper to check if they work correctly in the newer ckan/python version 


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
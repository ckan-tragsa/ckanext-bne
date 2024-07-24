from ckan.lib.plugins import DefaultTranslation
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.bne.config as bne_config
from ckanext.bne import helpers, validators, blueprint

import logging

log = logging.getLogger(__name__)


class BnePlugin(plugins.SingletonPlugin,  DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'bne')
        
        toolkit.add_resource("assets", "ckanext-bne")
        
    # Blueprints
    def get_blueprint(self):
        return [blueprint.bne]

    # Helpers
    def get_helpers(self):
        all_helpers = dict(helpers.all_helpers)
        return all_helpers

    # Validators
    def get_validators(self):
        return dict(validators.all_validators)
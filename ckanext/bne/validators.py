
import logging

import ckanext.scheming.helpers as sh
import ckan.lib.helpers as h
from ckantoolkit import (
    config,
    get_validator,
    UnknownValidator,
    missing,
    Invalid,
    StopOnError,
    _,
    unicode_safe,
)

import ckanext.schemingdcat.helpers as sdct_helpers

log = logging.getLogger(__name__)

all_validators = {}


def validator(fn):
    """
    collect validator functions into ckanext.scheming.all_validators dict
    """
    all_validators[fn.__name__] = fn
    return fn

def scheming_validator(fn):
    """
    Decorate a validator that needs to have the scheming fields
    passed with this function. When generating navl validator lists
    the function decorated will be called passing the field
    and complete schema to produce the actual validator for each field.
    """
    fn.is_a_scheming_validator = True
    return fn
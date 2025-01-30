import ckan.model as model
import ckan.lib.base as base
import ckan.logic as logic
from flask import Blueprint, render_template

from logging import getLogger

logger = getLogger(__name__)
get_action = logic.get_action

bne = Blueprint(u'bne', __name__)
def base():
    return render_template('bne/base.html')

def api_view():
    return render_template('bne/api_view.html')

def api_info():
    return render_template('bne/api_info.html')

def informacion():
    return render_template('bne/informacion.html')

def resumen():
    return render_template('bne/resumen.html')

bne.add_url_rule('/bne/', view_func=base)
bne.add_url_rule('/bne/api_view/', view_func=api_view)
bne.add_url_rule('/bne/api_info/', view_func=api_info)
bne.add_url_rule('/bne/informacion/', view_func=informacion)
bne.add_url_rule('/bne/resumen/', view_func=resumen)

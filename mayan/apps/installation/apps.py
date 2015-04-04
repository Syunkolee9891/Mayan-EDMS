from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_tools
from common.utils import encapsulate
from navigation.api import register_model_list_columns

from .classes import Property, PropertyNamespace, PIPNotFound, VirtualEnv
from .links import link_menu_link, link_namespace_details, link_namespace_list


class InstallationApp(apps.AppConfig):
    name = 'installation'
    verbose_name = _('Installation')

    def ready(self):
        register_model_list_columns(PropertyNamespace, [
            {
                'name': _('Label'),
                'attribute': 'label'
            },
            {
                'name': _('Items'),
                'attribute': encapsulate(lambda entry: len(entry.get_properties()))
            }
        ])

        register_model_list_columns(Property, [
            {
                'name': _('Label'),
                'attribute': 'label'
            },
            {
                'name': _('Value'),
                'attribute': 'value'
            }
        ])

        # TODO: convert
        #register_links(PropertyNamespace, [link_namespace_details])
        #register_links(['installation:namespace_list', PropertyNamespace], [link_namespace_list], menu_name='secondary_menu')
        menu_tools.bind_links(links=[link_menu_link])

        # Virtualenv
        namespace = PropertyNamespace('venv', _('VirtualEnv'))
        try:
            venv = VirtualEnv()
        except PIPNotFound:
            namespace.add_property('pip', 'pip', _('pip not found.'), report=True)
        else:
            for item, version, result in venv.get_results():
                namespace.add_property(item, '%s (%s)' % (item, version), result, report=True)

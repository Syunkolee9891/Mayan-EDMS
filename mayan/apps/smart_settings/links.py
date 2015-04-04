from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_check_settings = Link(condition=is_superuser, icon='fa fa-gear', text=_('Settings'), view='settings:setting_list')

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings
from django.utils import timezone


from libnetid import network, parser
from libnetid.models import Inscription

User = get_user_model()


class NetidBackend(object):

    def authenticate(self, sid=None, uid=None, **kwargs):
        if not (sid and uid):
            return None

        xml = network.query_ulb(sid, uid)
        xml_user = parser.parse(xml)

        # Get or create the user corresponding to the data
        # recieved from the ULB api.
        try:
            user = User.objects.get(netid=xml_user.netid)
        except User.DoesNotExist:
            user = User.objects.create_user(
                netid=xml_user.netid,
                email=xml_user.mail,
                first_name=xml_user.first_name,
                last_name=xml_user.last_name,
                registration=xml_user.raw_matricule,
            )

        # In both cases we need to update the last_login value
        user.last_login = timezone.now()
        user.save()

        if settings.LIBNETID.get('store_inscriptions', True):
            self._store_inscriptions(user, xml_user.inscriptions)

    def _store_inscriptions(self, user, inscriptions):
        for inscription in inscriptions:
            try:
                Inscription.objects.create(
                    user=user,
                    faculty=inscription.faculty,
                    section=inscription.slug,
                    year=inscription.year,
                )
            except IntegrityError:
                # We already have this inscription in the database
                # so we don't give a fuck
                pass

    def get_user(self, user_id):
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None

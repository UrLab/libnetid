import xml.etree.ElementTree as ET
from datetime import datetime

from libnetid.user import User, Inscription
from libnetid.exceptions import IntranetError


def parse(xml):
    root = ET.fromstring(xml)

    if root.tag != 'intranet':
        raise IntranetError("Root tag must be <intranet>. (We got <%s>)" % root.tag)

    error_message = root.find('errMsgFr')
    if error_message is not None:
        raise IntranetError("Response was an error: %s" % error_message.text)

    session = _findOrRaise(root, 'session')
    xml_user = _findOrRaise(session, 'user')

    username = _findOrRaise(xml_user, 'username')
    netid = username.text.strip()

    user = User(netid)

    for identity in xml_user.findall('identity'):
        raw_matricule = _findOrDefault(identity, 'matricule').lower()
        matricule = raw_matricule.split(':')[-1].strip()
        if not matricule.isdigit():
            matricule = ''
        user.update(matricule=matricule, raw_matricule=raw_matricule)

        if raw_matricule.split(":")[0].strip() == 'ulb':
            user.update(university='ULB')
        elif len(raw_matricule.split(":")) > 1 and raw_matricule.split(":")[1] == 'vub'.strip():
            user.update(university='VUB')

        last_name = _findOrDefault(identity, 'nom').title()
        first_name = _findOrDefault(identity, 'prenom')
        user.update(first_name=first_name, last_name=last_name)

        birthday = _findOrDefault(identity, 'dateNaissance')
        if birthday != '':
            birthday = datetime.strptime(birthday, '%d/%m/%Y').date()
        user.update(birthday=birthday)

        mail = _findOrDefault(identity, 'email').lower()
        user.update(mail=mail)

        library = _findOrDefault(identity, 'biblio')
        if not library.isdigit():
            library = ''
        user.update(library=library)

        inscriptions = identity.find('inscriptions')
        if inscriptions is None:
            inscriptions = []
        else:
            inscriptions = inscriptions.findall('inscription')

        for inscription in inscriptions:
            year = _findOrDefault(inscription, 'anac')
            slug = _findOrDefault(inscription, 'anet')
            faculty = _findOrDefault(inscription, 'facid')

            if year.isdigit():
                obj = Inscription(year, slug, faculty)
                user.update(inscriptions=[obj])

    user.update(mail=netid + '@ulb.ac.be')

    return user


def _findOrRaise(element, search):
    ret = element.find(search)
    if ret is None:
        raise IntranetError("<%s> has no <%s> tag." % (element.tag, search))
    return ret


def _findOrDefault(element, search, default=''):
    ret = element.find(search)
    if ret is None:
        return default
    else:
        text = ret.text
        if text is None:
            return ''
        else:
            return text.strip()

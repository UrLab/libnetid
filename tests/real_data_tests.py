# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import pytest

import sys
sys.path.append("../libnetid")

from glob import glob
from libnetid.parser import parse


def test_does_parse():
    for file in glob("tests/fixtures/private/*.xml"):
        with open(file) as fp:
            xml = fp.read()
        ret = parse(xml)

        assert isinstance(ret.netid, str)
        assert ret.mail.endswith('@ulb.ac.be') or ret.mail.endswith('@vub.ac.be')
        assert ret.last_name and ret.first_name

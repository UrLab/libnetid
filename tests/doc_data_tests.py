# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import pytest

import sys
sys.path.append("../libnetid")

import datetime
from libnetid.parser import parse


def test_example_simple():
    xml = open("tests/fixtures/doc_example.xml").read()
    ret = parse(xml)

    assert ret.netid == 'llibert'
    assert ret.mail == 'luc.libert@ulb.ac.be'
    assert ret.matricule == '14889'
    assert ret.birthday == datetime.date(1991, 10, 31)


def test_example_all():
    xml = open("tests/fixtures/doc_example_all.xml").read()
    ret = parse(xml)

    assert ret.netid == 'llibert'
    assert ret.mail == 'luc.libert@ulb.ac.be'
    assert ret.matricule == '14889'
    assert ret.birthday == datetime.date(1991, 10, 31)

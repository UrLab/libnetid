# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import pytest

import sys
sys.path.append("../libnetid")

from libnetid.parser import parse


def test_minimal():
    xml = open("tests/fixtures/minimal.xml").read()
    ret = parse(xml)

    assert ret.netid == 'blabevue'
    assert ret.mail == 'blabevue@ulb.ac.be'


def test_minimal_identity():
    xml = open("tests/fixtures/minimal_identity.xml").read()
    ret = parse(xml)

    assert ret.netid == 'blabevue'
    assert ret.mail == 'blabevue@ulb.ac.be'


def test_sparse_identity():
    xml = open("tests/fixtures/sparse_identity.xml").read()
    ret = parse(xml)

    assert ret.netid == 'blabevue'
    assert ret.mail == 'bertrand.labevue@ulb.ac.be'
    assert ret.matricule == '000123456'
    assert ret.last_name == 'Labevue'


def test_unknown_raw_matricule():
    xml = open("tests/fixtures/unknown_raw_matricule.xml").read()
    ret = parse(xml)

    assert ret.matricule == '000123456'
    assert ret.university is None


def test_invalid_matricule():
    xml = open("tests/fixtures/invalid_matricule.xml").read()
    ret = parse(xml)

    assert ret.raw_matricule == 'no-shit000123456'
    assert ret.matricule == ''
    assert ret.university is None

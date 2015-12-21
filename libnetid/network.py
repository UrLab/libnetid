import requests
import furl

ULB_AUTH = 'https://www.ulb.ac.be/commons/check?_type=normal&_sid={}&_uid={}'


def query_ulb(sid, uid):
    resp = requests.get(ULB_AUTH.format(sid, uid))
    # force utf-8 because the ULB does not send the right header
    resp.encoding = 'utf-8'

    return resp.text


def login_url(return_url, realm="ulb:gehol"):
    ulb_url = furl("https://www.ulb.ac.be/commons/intranet")
    ulb_url.args["_prt"] = realm
    ulb_url.args["_ssl"] = "on"
    ulb_url.args["_prtm"] = "redirect"
    ulb_url.args["_appl"] = return_url

    return ulb_url

import requests
import furl


def query_ulb(sid, uid):
    '''
    Gets back (from ULB) the result of a user authentication and handles
    text decoding to unicode.
        - sid and uid (str) are two tokens given as GET parameters by the user
        that is returning from a successful authentication on the ULB side.
    Returns a unicode string most likely conataining some xml.

    Note: you may only get a valid response if you are requesting the data
    from the same ip that the one associated with the domain name in 'return_url'
    given to the client (see login_url). It will thus not work if you don't have
    a public IP. Yay.
    '''
    if not sid.isalnum() or not uid.isalnum():
        raise ValueError("sid and uid must be alphanumeric values")

    url = 'https://www.ulb.ac.be/commons/check?_type=normal&_sid=%s&_uid=%s'
    response = requests.get(url % (sid, uid))
    # force utf-8 because the ULB does not send the right encoding header (WTF)
    response.encoding = 'utf-8'

    return response.text


def login_url(return_url, realm="ulb:gehol"):
    '''
    Crafts a url to give the the user's browser to initiate the autentication.
        - return_url (str): url where the user will be redirected
        by ULB after a successfull auth
        - realm (str): identifier used by the other side to filter users and
        deny those with insufficient privileges (eg: filter users from a faculty, ...)

    ULB side filtering is not very useful and is not flexible at all, we suggest to
    let every valid netid pass trough (use realm="ulb:gehol") and filter on your side.

    There is no check on the ULB side to see if you (developper) have permission to
    use the realm you specify. "ulb:gehol" is one of the most open ones so we
    set it as a default but you may also use any other one in the wild.

    Returns a url.
    '''
    ulb_url = furl("https://www.ulb.ac.be/commons/intranet")
    ulb_url.args["_prt"] = realm
    ulb_url.args["_ssl"] = "on"
    ulb_url.args["_prtm"] = "redirect"
    ulb_url.args["_appl"] = return_url

    return ulb_url

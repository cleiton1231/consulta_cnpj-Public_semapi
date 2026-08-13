from curl_cffi import requests as curl_requests

def nova_sessao():
    return curl_requests.Session(impersonate="chrome")

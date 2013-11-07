from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Url,
    Hit
    )
import transaction
import string, random

from pyramid.httpexceptions import HTTPFound


@view_config(route_name='new', renderer='json')
def new(request):
    # Get the URL to map from the POST
    url = request.POST['url']

    # Build the shortned URL
    s_url = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

    # Write to the SQL DB
    with transaction.manager:
        url = Url(url_link=url, url_short=s_url)
        DBSession.add(url)

    return {
        's_url': s_url,
    }

@view_config(route_name='short', renderer='json')
def short(request):
    print('************')
    print('************')
    print('************ in short')
    print('short link: ' + request.matchdict['s_url'])

    # DB lookup for the url to that shortlink
    s_url = request.matchdict['s_url']
    f_url = DBSession.query(Url).filter(Url.url_short == s_url).first()

    # Get the IP of the request
    req_ip = request.remote_addr

    # Get the referer IP
    ref_ip = request.referer

    # print('f_url: ' + f_url.url_link)
    print('in /short')

    #Write to the SQL DB
    with transaction.manager:
        hit = Hit(ip=req_ip, referer=ref_ip, url_id=f_url.id)
        DBSession.add(hit)

    # Redirect to the mapped URL
    return HTTPFound(location=f_url.url_link)

    # return {
    #     'f_url': f_url.url_link,
    #     'ip': req_ip,
    #     'referer': ref_ip
    # }

@view_config(route_name='stats', renderer='json')
def stats(request):
    print('************')
    print('************')
    print('************ in stats')

    # DB lookup of the hits table
    hits = DBSession.query(Hit).all()
    # hits = DBSession.query(Hit).filter(Hit.id=='1').all()

    return_string = ''

    for hit in hits:
        print('################ found a hit')
        return_string += 'ip: ' + hit.ip
        return_string += '  referer: ' + str(hit.referer)
        return_string += '  url_id: ' + str(hit.url_id)
        return_string += '  visited at: ' + str(hit.time_visited)
        return_string += '\n'
        print(hit)

    return {
        '': return_string
    }


from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('new', '/new')
    config.add_route('stats', '/stats') # displays the hits table to show the stats
    config.add_route('favicon', '/favicon.ico')
    config.add_route('short', '/{s_url}')
    config.scan()
    return config.make_wsgi_app()

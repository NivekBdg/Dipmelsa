# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu = [
        (T('Home'), False, URL('default', 'index'), []),
        (T('Cotizaciones'), False, URL('default', 'index'),[
            (T('Ingresar cotización'), False, URL('admin', 'crearCotizacion'))
            ])
    ]

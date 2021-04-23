# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

db.define_table('rh_puesto',
               Field('descripcion', 'text'),
               Field('salario_dia', 'double'),
               Field('fecha_alta','date'),
               Field('fecha_baja','date'),
               Field('fecha_modifica','date'),
               Field('usuario_alta', 'text'),
               Field('usuario_baja', 'text'),
               Field('usuario_modifica', 'text'),
               Field('ind_cotizacion', 'integer'),
               Field('estado', 'integer'))

db.define_table('rh_empleado',
               Field('nombres', 'text'),
               Field('apellidos', 'text'),
               Field('dpi', 'text'),
               Field('nit', 'text'),
               Field('no_igss', 'text'),
               Field('no_irtra', 'text'),
               Field('sexo', 'integer'),
               Field('cod_puesto','reference rh_puesto'),
               Field('fecha_nacimiento','date'),
               Field('fecha_baja','date'),
               Field('fecha_alta','date'),
               Field('usuario_alta', 'text'),
               Field('usuario_baja', 'text'),
               Field('usuario_modifica', 'text'),
               Field('estado', 'integer'),
               Field('cantidad_hijos', 'integer'),
               Field('salario', 'double'),
               Field('bonificacion', 'double'))

db.define_table('op_porcentaje_material',
               Field('descripcion', 'text'),
               Field('valor', 'double'))

db.define_table('op_porcentaje_impuesto',
               Field('descripcion', 'text'),
               Field('valor', 'double'))

db.define_table('op_porcentaje_utilidad',
               Field('descripcion', 'text'),
               Field('valor', 'double'))

db.define_table('op_tipo_transporte',
               Field('descripcion', 'text'),
               Field('valor_kilo', 'double'))

db.define_table('op_material',
               Field('descripcion','text'),
               Field('precio_unitario','double'),
               Field('marca', 'text'))

db.define_table('op_mat_cotizacion',
               Field('material','reference op_material'),
               Field('cantidad','double'))

db.define_table('op_cotizacion',
               Field('nombre_proyecto', 'text'),
               Field('fecha_crea', 'date'),
               Field('usuario_modifica', 'text'),
               Field('fecha_modifica', 'date'),
               Field('total_mano_obra', 'double'),
               Field('fianzas', 'integer'),
               Field('materiales', 'reference op_mat_cotizacion'),
               Field('tipo_transporte', 'reference op_tipo_transporte'))


db.define_table('op_per_cotizacion',
               Field('descripcion', 'text'),
               Field('cod_cotizacion', 'reference op_cotizacion'),
               Field('salario_dia', 'double'),
               Field('fecha_modifica', 'date'),
               Field('total_mano_obra', 'double'),
               Field('fianzas', 'integer'))

db.define_table('op_tipo_hora',
               Field('descripcion','text'))

db.define_table('op_horex_cotizacion',
                Field('descripcion','text'),
               Field('cod_cotizacion','reference op_cotizacion'),
               Field('costo_unitario','double'),
               Field('cantidad_personas','integer'),
               Field('cantidad_dias','integer'),
               Field('cantidad_horas','double'),
               Field('cod_tipo_hora','reference op_tipo_hora'))

db.define_table('op_viatico_cotizacion',
               Field('descripcion','text'),
               Field('geo_lugar','text'),
               Field('cod_cotizacion','reference op_cotizacion'),
               Field('costo_unitario','double'),
               Field('cantidad_personas','integer'),
               Field('cantidad_dias','integer'),
               Field('cantidad_tiempos','double'),
               Field('cod_empleado', 'reference rh_empleado'))




# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from admin.py")

def crearCotizacion():
    puestos = db((db.rh_puesto.ind_cotizacion == 1)).select()
    transporte = db(db.op_tipo_transporte.id>0).select()
    utilidad = db(db.op_porcentaje_utilidad.id>0).select()
    impuesto = db(db.op_porcentaje_impuesto.id>0).select()
    material = db(db.op_porcentaje_material.id>0).select()
    return dict(puestos = puestos, transporte = transporte, utilidad = utilidad, impuesto = impuesto, material = material)

def ingresarProductos():
    nombreMaterial = request.vars.get('nombreMaterial')
    precio = request.vars.get('precio')
    marca = request.vars.get('marca')
    enviar = request.vars.get('Guardar')
    if enviar:
        idregistro = db.op_material.insert(descripcion = nombreMaterial, precio_unitario = precio, marca = marca)
    materiales = db((db.op_material.id > 0)).select()
    return dict(materiales = materiales)

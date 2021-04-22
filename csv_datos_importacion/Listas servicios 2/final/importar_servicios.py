ruta = '../raw/servicios.csv'
def get_object_if_exists(external_id=False):
	try:
		tiene_modulo_id=False
		if '.' in external_id:
			tiene_modulo_id=True

		objecto = self.env.ref(external_id if tiene_modulo_id else '__import__.'+external_id)
		return objecto
	except ValueError:
		return False

archivo = open(ruta).read()

archivo_lista = archivo.split('\n')

for linea in archivo_lista:
	
	linea_separada = linea.split(',') if linea and linea not in ['id,name,determinacion,list_price,lst_price,organismo_id/id,unidad_id/id,departamento_id/id,coordinacion_id/id,laboratorio_id/id,verificacion_insitu,active,type',',,,,,,,,,,,,'] else False
	if linea_separada:
		try:
			tiene_modulo_id = False
			if '.' in linea_separada[0]:
				tiene_modulo_id=True
			objeto_existente = get_object_if_exists(linea_separada[0])
			if objeto_existente:
				objeto_existente.update({
					'name':linea_separada[1],
					'determinacion':linea_separada[2],
					'list_price':linea_separada[3],
					'lst_price':linea_separada[4],
					'organismo_id':get_object_if_exists(linea_separada[5]).id,
					'unidad_id':get_object_if_exists(linea_separada[6]).id,
					'departamento_id':get_object_if_exists(linea_separada[7]).id,
					'coordinacion_id':get_object_if_exists(linea_separada[8]).id,
					'laboratorio_id':get_object_if_exists(linea_separada[9]).id,
					'verificacion_insitu':True if linea_separada[10].upper() == 'TRUE' else False,
					'active':True if linea_separada[11].upper() == 'TRUE' else False,
					'type':'consu',
					})
			else:
				data_objeto_creado={
					'name':linea_separada[1],
					'determinacion':linea_separada[2],
					'list_price':linea_separada[3],
					'lst_price':linea_separada[4],
					'organismo_id':get_object_if_exists(linea_separada[5]).id,
					'unidad_id':get_object_if_exists(linea_separada[6]).id,
					'departamento_id':get_object_if_exists(linea_separada[7]).id,
					'coordinacion_id':get_object_if_exists(linea_separada[8]).id,
					'laboratorio_id':get_object_if_exists(linea_separada[9]).id,
					'verificacion_insitu':True if linea_separada[10].upper() == 'TRUE' else False,
					'active':True if linea_separada[11].upper() == 'TRUE' else False,
					'type':'consu',
					}
				data_objeto_creado
				objeto_creado = self.env['product.template'].create(data_objeto_creado)
				data = {
					'module': linea_separada[0].split('.')[0] if tiene_modulo_id else '__import__',
					'name': linea_separada[0] if not tiene_modulo_id else '.'.join([linea_separada[0].split('.')[i] for i in range(1,len(linea_separada[0].split('.')))]),
					'display_name':linea_separada[1],
					'model':objeto_creado._name,'res_id':objeto_creado.id,
					}
				self.env['ir.model.data'].create(data)
		except AttributeError:
			print('LINEA FALLIDA')
			lineas_fallidas = open('servicios_fallidos.csv','a')
			lineas_fallidas.write(linea+'\n')
			lineas_fallidas.close()


self._cr.commit()

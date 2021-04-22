ruta = 'departamentos_uniq.csv'
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
	
	linea_separada = linea.split(',') if linea and linea not in ['id,name,unidad_id/id',',,'] else False
	if linea_separada:
		try:
			tiene_modulo_id = False
			if '.' in linea_separada[0]:
				tiene_modulo_id=True
			objeto_existente = get_object_if_exists(linea_separada[0])
			if not objeto_existente:
				data_objeto_creado={
					'name':linea_separada[1],
					'unidad_id':get_object_if_exists(linea_separada[2]).id if get_object_if_exists(linea_separada[2]) else False,
					}
				data_objeto_creado
				objeto_creado = self.env['intn.departamentos'].create(data_objeto_creado)
				data = {
					'module': linea_separada[0].split('.')[0] if tiene_modulo_id else '__import__',
					'name': linea_separada[0] if not tiene_modulo_id else '.'.join([linea_separada[0].split('.')[i] for i in range(1,len(linea_separada[0].split('.')))]),
					'display_name':linea_separada[1],
					'model':objeto_creado._name,'res_id':objeto_creado.id,
					}
				self.env['ir.model.data'].create(data)
		except AttributeError:
			print('LINEA FALLIDA')
			lineas_fallidas = open('departamentos_fallidos.csv','a')
			lineas_fallidas.write(linea+'\n')
			lineas_fallidas.close()


self._cr.commit()

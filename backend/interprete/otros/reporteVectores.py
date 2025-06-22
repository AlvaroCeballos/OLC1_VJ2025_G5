class ReporteVectores:
    vectores = []  # Lista de vectores reportados
    
    def __init__(self):
        pass
    
    @classmethod
    def addVector(cls, id_vector, tipo, dimensiones, datos_lineales, tamanio_total, ambito):
        """Agregar un vector al reporte"""
        vector_info = {
            'id': id_vector,
            'tipo': tipo,
            'dimensiones': dimensiones,
            'datos_lineales': datos_lineales,
            'tamanio_total': tamanio_total,
            'ambito': ambito,
            'estrategia': cls._generar_estrategia(dimensiones, datos_lineales)
        }
        cls.vectores.append(vector_info)
        print(f"DEBUG: Vector {id_vector} agregado al reporte")
    
    @classmethod
    def _generar_estrategia(cls, dimensiones, datos):
        """Genera la explicación de la estrategia de almacenamiento"""
        if len(dimensiones) == 1:
            # Vector unidimensional
            estrategia = f"Vector 1D: almacenamiento directo lineal\n"
            estrategia += f"Tamaño: {dimensiones[0]} elementos\n"
            estrategia += f"Acceso: vector[i] = posición i\n"
            estrategia += f"Datos: {datos}"
            return estrategia
        
        elif len(dimensiones) == 2:
            # Matriz 2D
            filas, columnas = dimensiones[0], dimensiones[1]
            estrategia = f"Matriz 2D: almacenamiento por filas (row-major)\n"
            estrategia += f"Dimensiones: {filas}x{columnas}\n"
            estrategia += f"Mapeo de índices:\n"
            
            # Mostrar mapeo de índices
            for i in range(filas):
                for j in range(columnas):
                    pos_lineal = i * columnas + j
                    if pos_lineal < len(datos):
                        estrategia += f"  [{i}][{j}] → pos {pos_lineal} = {datos[pos_lineal]}\n"
            
            estrategia += f"Datos lineales: {datos}"
            return estrategia
        
        elif len(dimensiones) == 3:
            # Tensor 3D
            dim1, dim2, dim3 = dimensiones[0], dimensiones[1], dimensiones[2]
            estrategia = f"Tensor 3D: almacenamiento por capas\n"
            estrategia += f"Dimensiones: {dim1}x{dim2}x{dim3}\n"
            estrategia += f"Datos lineales: {datos}"
            return estrategia
        
        else:
            # N dimensiones
            estrategia = f"Vector {len(dimensiones)}D: almacenamiento multidimensional\n"
            estrategia += f"Dimensiones: {' x '.join(map(str, dimensiones))}\n"
            estrategia += f"Datos lineales: {datos}"
            return estrategia
    
    @classmethod
    def serializarVectores(cls):
        """Serializar vectores para envío al frontend"""
        vectores_serializados = []
        for vector in cls.vectores:
            vectores_serializados.append({
                'id': vector['id'],
                'tipo': vector['tipo'],
                'dimensiones': f"{' x '.join(map(str, vector['dimensiones']))}",
                'tamanio_total': vector['tamanio_total'],
                'ambito': vector['ambito'],
                'estrategia': vector['estrategia'],
                'datos': str(vector['datos_lineales'])
            })
        return vectores_serializados
    
    @classmethod
    def cleanReporteVectores(cls):
        """Limpiar la lista de vectores"""
        cls.vectores = []
        print("DEBUG: Reporte de vectores limpiado")
    
    @classmethod
    def getVectores(cls):
        """Obtener lista de vectores"""
        return cls.vectores
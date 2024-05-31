class Proyecto:
    def __init__(self, nombre_usuario, repositorio, fecha_actualizacion, lenguaje, likes, tags, url):
        self.nombre_usuario = nombre_usuario
        self.repositorio = repositorio
        self.fecha_actualizacion = fecha_actualizacion
        self.lenguaje = lenguaje
        self.likes = likes
        self.tags = tags
        self.url = url

    def __str__(self):
        return f'| Nombre del usuario: {self.nombre_usuario} | Repositorio: {self.repositorio} | Fecha de actualizacion:' \
               f' {self.fecha_actualizacion} | Lenguaje: {self.lenguaje} | Likes: {str(self.likes)}k | ' \
               f'Tags: {self.tags} | Url: {self.url} |'

class Matriz:
    def __init__(self, mes, estrellas, cantidad):
        self.mes = mes
        self.estrellas = estrellas
        self.cantidad = cantidad

    def __str__(self):
        return f'| Mes {self.mes} | Estrellas: {self.estrellas} | Cantidad en la celda: {self.cantidad} |'

import pilas
pilas.iniciar() 
#Escena del menu donde defino el fondo,acceso al juego o salir,titulo.
class EscenaDeMenu(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        pilas.fondos.Fondo("GT-22-1.jpg")
        self.crear_titulo_del_juego()
        
    def crear_titulo_del_juego(self):
        logotipo=pilas.actores.Actor("pac.png")
        logotipo.y= 300
        logotipo.y=[200]

        opciones = [('Comenzar a jugar', self.comenzar),('Salir', self.salir)]
        self.menu = pilas.actores.Menu(opciones)

    def comenzar(self):
        pilas.cambiar_escena(EscenaJuego())

    def salir(self):
        import sys
        sys.exit(0)
#Clase del juego esta la clase del Pacman y de los Fantasmas
class EscenaJuego(pilas.escena.Base):
	def __init__(self):
		pilas.escena.Base.__init__(self)
		
	def iniciar(self):
		#Clase del Pacman se mueve con las flechas
		class Pacman(pilas.actores.Pacman):

			def __init__(self, mapa):
				self.mapa = mapa
				pilas.actores.Pacman.__init__(self, -12, -12)
			#funcion en la cual segun el control se define el numero de cuadro de la grilla del Pacman
			def actualizar(self):
				if self.control.izquierda:
					self.posicion = 0
					self.y = self.ajustar_coordenada_a_grilla(self.y)
				elif self.control.derecha:
					self.posicion = 1
					self.y = self.ajustar_coordenada_a_grilla(self.y)
				elif self.control.abajo:
					self.posicion = 3
					self.x = self.ajustar_coordenada_a_grilla(self.x)
				elif self.control.arriba:
					self.posicion = 2
					self.x = self.ajustar_coordenada_a_grilla(self.x)
				if self.posicion == 0:
					self.mover(-1, 0)
				elif self.posicion == 1:
					self.mover(1, 0)
				elif self.posicion == 2:
					self.mover(0, 1)
				elif self.posicion == 3:
					self.mover(0, -1)
			#Funcion para que colisione con el Mapa de Tiled
			def mover(self, x, y):
				if x and y:
					raise Exception("El pacman no se puede mover en diagonal")

				destino_x = self.x + self.velocidad * x
				destino_y = self.y + self.velocidad * y
				dx = 0
				dy = 0

				if x:
					if x > 0:
						dx = 12
					else:
						dx = -12

					va_a_pisar_solido = self.mapa.es_punto_solido(destino_x + dx, self.y)

				if y:
					if y > 0:
						dy = 12
					else:
						dy = -12

					va_a_pisar_solido = self.mapa.es_punto_solido(self.x, self.y + dy)

				if not va_a_pisar_solido:
					self._reproducir_animacion()
					self.x += self.velocidad * x
					self.y += self.velocidad * y
				else:
					self.x = self.ajustar_coordenada_a_grilla(self.x)
					self.y = self.ajustar_coordenada_a_grilla(self.y)


			def ajustar_coordenada_a_grilla(self, coordenada):
				return (int(coordenada / 24) * 24) + 12
			#Pierde Juego
			def perder(self):
				t=pilas.actores.Texto("PERDISTE....")
				t.escala=1
			#Gana Juego
			def ganar(self):
				e=pilas.actores.Texto("GANASTE")
				e.escala=1
		#Esta clase es igual al del Pacman solo que con el Actor Fantasma
		class Fantasma(pilas.actores.Fantasma):

			def __init__(self, mapa):
				self.mapa = mapa
				pilas.actores.Fantasma.__init__(self, -12, -12)

			def actualizar(self):
				if self.control.izquierda:
					self.posicion = 2
					self.y = self.ajustar_coordenada_a_grilla(self.y)
				elif self.control.derecha:
					self.posicion = 3
					self.y = self.ajustar_coordenada_a_grilla(self.y)
				elif self.control.abajo:
					self.posicion = 1
					self.x = self.ajustar_coordenada_a_grilla(self.x)
				elif self.control.arriba:
					self.posicion = 0
					self.x = self.ajustar_coordenada_a_grilla(self.x)
				if self.posicion == 0:
					self.mover(-1, 0)
				elif self.posicion == 1:
					self.mover(1, 0)
				elif self.posicion == 2:
					self.mover(0, 1)
				elif self.posicion == 3:
					self.mover(0, -1)

			def mover(self, x, y):
				if x and y:
					raise Exception("El pacman no se puede mover en diagonal")

				destino_x = self.x + self.velocidad * x
				destino_y = self.y + self.velocidad * y
				dx = 0
				dy = 0

				if x:
					if x > 0:
						dx = 12
					else:
						dx = -12

					va_a_pisar_solido = self.mapa.es_punto_solido(destino_x + dx, self.y)

				if y:
					if y > 0:
						dy = 12
					else:
						dy = -12

					va_a_pisar_solido = self.mapa.es_punto_solido(self.x, self.y + dy)

				if not va_a_pisar_solido:
					self._reproducir_animacion()
					self.x += self.velocidad * x
					self.y += self.velocidad * y
				else:
					self.x = self.ajustar_coordenada_a_grilla(self.x)
					self.y = self.ajustar_coordenada_a_grilla(self.y)


			def ajustar_coordenada_a_grilla(self, coordenada):
				return (int(coordenada / 24) * 24) + 12
			def perder(self):
				t=pilas.actores.Texto("GAME OVER")
				t.escala=1
		#Esta clase hace lo mismo que la clase Fantasma solo que se mueve de forma contraria al Pacman.
		class FantasmA(pilas.actores.Fantasma):
			def __init__(self, mapa):
				self.mapa = mapa
				pilas.actores.Fantasma.__init__(self, -12, -12)
			#Cambie los cuadros de la grilla del fantasma para que se moviera contrariamente al Pacman.
			def actualizar(self):
				if self.control.izquierda:
					self.posicion = 0
					self.y = self.ajustar_coordenada_a_grilla(self.y)
				elif self.control.derecha:
					self.posicion = 1
					self.y = self.ajustar_coordenada_a_grilla(self.y)
				elif self.control.abajo:
					self.posicion = 3
					self.x = self.ajustar_coordenada_a_grilla(self.x)
				elif self.control.arriba:
					self.posicion = 2
					self.x = self.ajustar_coordenada_a_grilla(self.x)
				if self.posicion == 0:
					self.mover(-1, 0)
				elif self.posicion == 1:
					self.mover(1, 0)
				elif self.posicion == 2:
					self.mover(0, 1)
				elif self.posicion == 3:
					self.mover(0, -1)

			def mover(self, x, y):
				if x and y:
					raise Exception("El pacman no se puede mover en diagonal")

				destino_x = self.x + self.velocidad * x
				destino_y = self.y + self.velocidad * y
				dx = 0
				dy = 0

				if x:
					if x > 0:
						dx = 12
					else:
						dx = -12

					va_a_pisar_solido = self.mapa.es_punto_solido(destino_x + dx, self.y)

				if y:
					if y > 0:
						dy = 12
					else:
						dy = -12

					va_a_pisar_solido = self.mapa.es_punto_solido(self.x, self.y + dy)

				if not va_a_pisar_solido:
					self._reproducir_animacion()
					self.x += self.velocidad * x
					self.y += self.velocidad * y
				else:
					self.x = self.ajustar_coordenada_a_grilla(self.x)
					self.y = self.ajustar_coordenada_a_grilla(self.y)

			def ajustar_coordenada_a_grilla(self, coordenada):
				return (int(coordenada / 24) * 24) + 12
			def perder(self):
				t=pilas.actores.Texto("GAME OVER")
				t.escala=1
#-----------------------------------------------------------------------------------------------
	#Aca fui definiendo el mapa de Tiled,el pacman,los fantasmas estan con clases diferentes en los cuales
	#defini posicion,radio de colision,escala,tambien defini los items(estrellas)y el actor puntos.
	#Funciones para colisionar con los fantasmas y los items.
		mapa = pilas.actores.MapaTiled('mapa_pacman.tmx')

		pacman = Pacman(mapa)
		pacman.radio_de_colision = 5
		pacman.escala = 2
		pacman.x=243
		pacman.y= -200
		fantasma = Fantasma(mapa)
		fantasma.radio_de_colision=5
		fantasma.escala=2
		fantasma.x= 222
		fan1=Fantasma(mapa)
		fan1.radio_de_colision=5
		fan1.escala=2
		fan1.x=-222
		fan1.y= -50
		fan2=FantasmA(mapa)
		fan2.radio_de_colision=5
		fan2.escala=2
		fan2.x=-100
		fan3=FantasmA(mapa)
		fan3.radio_de_colision=5
		fan3.escala=2
		fan3.x= 100  
		fan3.y=-150    
		fan4=FantasmA(mapa)
		fan4.radio_de_colision=5
		fan4.escala=2
		fan4.x= 100  
		fan4.y= 211 
		fan5=Fantasma(mapa)
		fan5.radio_de_colision=5
		fan5.escala=2
		fan5.x= 90  
		fan5.y= 150
		fan6=Fantasma(mapa)
		fan6.radio_de_colision=5
		fan6.escala=2
		fan6.x=200
		fan6.y=150
		fan7=Fantasma(mapa)
		fan7.radio_de_colision=5
		fan7.escala=2
		fan7.x=80
		fan7.y=-30
		FANTASMAS=[fantasma,fan1,fan3,fan4,fan2,fan5,fan6,fan7]
		puntos = pilas.actores.Puntaje(x=-290, y=210)
		item=pilas.actores.Estrella()
		item.escala=0.3
		item.x=120
		item.radio_de_colision=5
		item1=pilas.actores.Estrella()
		item1.escala=0.3
		item1.x=-280
		item1.y= 200
		item1.radio_de_colision=5
		item2=pilas.actores.Estrella()
		item2.escala=0.3
		item2.x=-100
		item2.y=210
		item2.radio_de_colision=5
		ITEMS=[item,item1,item2]
		def agarra_item(Pacman,Estrella):
			item.eliminar()
			puntos.aumentar(1)
		pilas.escena_actual().colisiones.agregar(pacman, item,agarra_item)
		def agarra_item(Pacman,Estrella):
			item1.eliminar()
			puntos.aumentar(1)
		pilas.escena_actual().colisiones.agregar(pacman, item1,agarra_item)
		def agarra_item(Pacman,Estrella):
			item2.eliminar()
			puntos.aumentar(1)
		pilas.escena_actual().colisiones.agregar(pacman, item2,agarra_item)
		def pacman_muere(Fantasma,Pacman):	
			Fantasma.eliminar()
			Pacman.perder()
		pilas.escena_actual().colisiones.agregar(pacman, FANTASMAS, pacman_muere)
		

pilas.cambiar_escena(EscenaDeMenu())
pilas.ejecutar()

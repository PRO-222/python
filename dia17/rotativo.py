import math
import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    AmbientLight,
    CardMaker,
    DirectionalLight,
    Vec3,
    Vec4,
)


class JuegoPatitoLaguna(ShowBase):

    def __init__(self):
        super().__init__()

        self.disableMouse()

        # Fondo del cielo
        self.win.setClearColor(Vec4(0.4, 0.65, 0.85, 1.0))

        # Cámara elevada enfocando el centro
        self.camera.setPos(0, -35, 12)
        self.camera.setP(-12)

        # Entorno
        self.configurar_escenario_y_luces()

        # Personaje principal (Patito)
        self.patito = self.crear_patito()
        self.patito.reparentTo(self.render)
        self.patito.setPos(0, 0, 2.0)

        # Variables de juego
        self.obstaculos = []
        self.rayos = []
        self.puntaje = 0
        self.game_over = False

        self.velocidad_patito = 16
        self.mov_patito = Vec3(0, 0, 0)

        self.setup_controles()

        # Tareas
        self.taskMgr.add(self.girar_personaje, "GirarPersonaje")
        self.taskMgr.add(self.mover_patito, "MoverPatito")
        self.taskMgr.add(self.generar_obstaculos, "GenerarObstaculos")
        self.taskMgr.add(self.actualizar_juego, "ActualizarJuego")

    def crear_esfera(self, nombre, escala, color):
        nodo = self.loader.loadModel("models/misc/sphere")
        nodo.setName(nombre)
        nodo.setScale(escala)
        nodo.setTextureOff(1)
        nodo.setColor(color)
        return nodo

    def configurar_escenario_y_luces(self):
        # Agua de la laguna
        cm = CardMaker("agua_laguna")
        cm.setFrame(-20, 20, -10, 50)
        laguna = self.render.attachNewNode(cm.generate())
        laguna.setP(-90)
        laguna.setZ(-0.5)
        laguna.setTextureOff(1)
        laguna.setColor(Vec4(0.1, 0.45, 0.75, 1.0))

        # Costa / Orillas
        for lado in [-16, 16]:
            cm_orilla = CardMaker("orilla")
            cm_orilla.setFrame(lado - 6, lado + 6, -10, 50)
            orilla = self.render.attachNewNode(cm_orilla.generate())
            orilla.setP(-90)
            orilla.setZ(-0.4)
            orilla.setTextureOff(1)
            orilla.setColor(Vec4(0.2, 0.55, 0.2, 1.0))

            # Bosque
            for y in range(-5, 45, 7):
                x_pos = lado + random.uniform(-2, 2)
                self.crear_arbol(Vec3(x_pos, y, -0.4))

        # Montañas
        for i in range(-4, 5):
            montana = self.crear_esfera(
                "Montana", Vec3(8, 8, 12), Vec4(0.3, 0.35, 0.4, 1.0)
            )
            montana.reparentTo(self.render)
            montana.setPos(i * 8, 45, 2)

            nieve = self.crear_esfera(
                "Nieve", Vec3(4, 4, 4), Vec4(0.95, 0.95, 1.0, 1.0)
            )
            nieve.reparentTo(montana)
            nieve.setPos(0, 0, 0.7)

        # Luces
        luz_ambiente = AmbientLight("luz_ambiente")
        luz_ambiente.setColor(Vec4(0.6, 0.6, 0.65, 1.0))
        nodo_ambiente = self.render.attachNewNode(luz_ambiente)
        self.render.setLight(nodo_ambiente)

        luz_dir = DirectionalLight("luz_dir")
        luz_dir.setColor(Vec4(0.9, 0.85, 0.75, 1.0))
        nodo_dir = self.render.attachNewNode(luz_dir)
        nodo_dir.setHpr(-30, -50, 0)
        self.render.setLight(nodo_dir)

    def crear_arbol(self, pos):
        nodo_arbol = self.render.attachNewNode("Arbol")
        nodo_arbol.setPos(pos)

        tronco = self.crear_esfera(
            "Tronco", Vec3(0.4, 0.4, 2.0), Vec4(0.35, 0.2, 0.1, 1.0)
        )
        tronco.reparentTo(nodo_arbol)
        tronco.setZ(1.0)

        copa = self.crear_esfera(
            "Copa", Vec3(1.5, 1.5, 3.0), Vec4(0.1, 0.45, 0.15, 1.0)
        )
        copa.reparentTo(nodo_arbol)
        copa.setZ(2.8)

    def crear_patito(self):
        nodo_patito = self.render.attachNewNode("Patito")

        # Cuerpo
        cuerpo = self.crear_esfera(
            "Cuerpo", Vec3(1.0, 1.0, 0.9), Vec4(1.0, 0.85, 0.0, 1.0)
        )
        cuerpo.reparentTo(nodo_patito)

        # Cabeza
        cabeza = self.crear_esfera(
            "Cabeza", Vec3(0.75, 0.75, 0.75), Vec4(1.0, 0.85, 0.0, 1.0)
        )
        cabeza.reparentTo(nodo_patito)
        cabeza.setPos(0, 0.2, 1.1)

        # Pico
        pico = self.crear_esfera(
            "Pico", Vec3(0.35, 0.45, 0.15), Vec4(1.0, 0.4, 0.0, 1.0)
        )
        pico.reparentTo(cabeza)
        pico.setPos(0, 0.7, -0.1)

        # Ojos limpios (sin gafas) con pestañas
        for lado, x in [("Izq", -0.3), ("Der", 0.3)]:
            ojo = self.crear_esfera(
                f"Ojo{lado}", Vec3(0.18, 0.15, 0.22), Vec4(1, 1, 1, 1)
            )
            ojo.reparentTo(cabeza)
            ojo.setPos(x, 0.65, 0.25)

            pupila = self.crear_esfera(
                f"Pupila{lado}",
                Vec3(0.1, 0.1, 0.12),
                Vec4(0.05, 0.05, 0.05, 1),
            )
            pupila.reparentTo(ojo)
            pupila.setPos(0, 0.1, 0)

            pestana = self.crear_esfera(
                f"Pestana{lado}",
                Vec3(0.04, 0.04, 0.18),
                Vec4(0.05, 0.05, 0.05, 1),
            )
            pestana.reparentTo(ojo)
            pestana.setPos(-0.08 if lado == "Izq" else 0.08, 0.05, 0.18)
            pestana.setR(25 if lado == "Izq" else -25)

        # Moño Rosa
        rosa = Vec4(1.0, 0.3, 0.6, 1.0)
        nodo_mono = self.render.attachNewNode("NodoMono")
        nodo_mono.reparentTo(cabeza)
        nodo_mono.setPos(0, 0.1, 0.85)

        nudo = self.crear_esfera("NudoMono", Vec3(0.2, 0.2, 0.2), rosa)
        nudo.reparentTo(nodo_mono)

        mono_izq = self.crear_esfera("MonoIzq", Vec3(0.35, 0.2, 0.25), rosa)
        mono_izq.reparentTo(nodo_mono)
        mono_izq.setPos(-0.3, 0, 0)

        mono_der = self.crear_esfera("MonoDer", Vec3(0.35, 0.2, 0.25), rosa)
        mono_der.reparentTo(nodo_mono)
        mono_der.setPos(0.3, 0, 0)

        return nodo_patito

    def crear_huevo_mutante(self):
        nodo_huevo = self.render.attachNewNode("HuevoMutante")

        # Huevo Base
        huevo = self.crear_esfera(
            "Huevo", Vec3(0.9, 0.9, 1.3), Vec4(0.2, 0.15, 0.15, 1.0)
        )
        huevo.reparentTo(nodo_huevo)

        # Fuego Recubriéndolo
        fuego = self.crear_esfera(
            "FuegoLlama", Vec3(1.2, 1.2, 1.6), Vec4(1.0, 0.3, 0.0, 0.8)
        )
        fuego.reparentTo(nodo_huevo)

        # Ojos
        for x_pos in [-0.3, 0.3]:
            ojo = self.crear_esfera(
                "OjoDiablo", Vec3(0.18, 0.1, 0.18), Vec4(1.0, 0.0, 0.0, 1.0)
            )
            ojo.reparentTo(nodo_huevo)
            ojo.setPos(x_pos, -0.7, 0.2)

        # Colmillos
        for x in [-0.2, 0.2]:
            colmillo = self.crear_esfera(
                "Colmillo", Vec3(0.08, 0.08, 0.35), Vec4(0.95, 0.95, 0.9, 1.0)
            )
            colmillo.reparentTo(nodo_huevo)
            colmillo.setPos(x, -0.7, -0.3)
            colmillo.setP(20)

        return nodo_huevo

    def setup_controles(self):
        self.accept("arrow_left", self.set_patito_x, [-1])
        self.accept("arrow_right", self.set_patito_x, [1])
        self.accept("arrow_left-up", self.set_patito_x, [0])
        self.accept("arrow_right-up", self.set_patito_x, [0])

        self.accept("arrow_up", self.set_patito_z, [1])
        self.accept("arrow_down", self.set_patito_z, [-1])
        self.accept("arrow_up-up", self.set_patito_z, [0])
        self.accept("arrow_down-up", self.set_patito_z, [0])

        self.accept("space", self.habilidad_disparar_rayo)
        self.accept("mouse1", self.habilidad_disparar_rayo)

    def set_patito_x(self, val):
        self.mov_patito.setX(val)

    def set_patito_z(self, val):
        self.mov_patito.setZ(val)

    def habilidad_disparar_rayo(self):
        if not self.game_over:
            rayo = self.crear_esfera(
                "Rayo", Vec3(0.25, 1.8, 0.25), Vec4(0.0, 1.0, 0.8, 1.0)
            )
            rayo.reparentTo(self.render)
            rayo.setPos(self.patito.getPos() + Vec3(0, 1.0, 0.2))
            self.rayos.append(rayo)

    def girar_personaje(self, tarea):
        dt = globalClock.getDt()
        self.patito.setH(self.patito.getH() + 35 * dt)
        return Task.cont

    def mover_patito(self, tarea):
        if not self.game_over:
            dt = globalClock.getDt()
            desplazamiento = Vec3(
                self.mov_patito.getX() * self.velocidad_patito * dt,
                0,
                self.mov_patito.getZ() * self.velocidad_patito * dt,
            )

            nueva_pos = self.patito.getPos() + desplazamiento
            nueva_pos.setX(max(-10.0, min(10.0, nueva_pos.getX())))
            nueva_pos.setZ(max(0.5, min(9.0, nueva_pos.getZ())))
            self.patito.setPos(nueva_pos)

        return Task.cont

    def generar_obstaculos(self, tarea):
        if not self.game_over and random.random() < 0.04:
            huevo = self.crear_huevo_mutante()
            huevo.reparentTo(self.render)
            huevo.setPos(random.uniform(-9, 9), 30, random.uniform(1.0, 8.0))
            self.obstaculos.append(huevo)
        return Task.cont

    def actualizar_juego(self, tarea):
        dt = globalClock.getDt()

        for rayo in self.rayos[:]:
            if rayo.isEmpty():
                if rayo in self.rayos:
                    self.rayos.remove(rayo)
                continue

            rayo.setY(rayo.getY() + 40 * dt)
            if rayo.getY() > 35:
                rayo.removeNode()
                if rayo in self.rayos:
                    self.rayos.remove(rayo)

        for huevo in self.obstaculos[:]:
            if huevo.isEmpty():
                if huevo in self.obstaculos:
                    self.obstaculos.remove(huevo)
                continue

            huevo.setY(huevo.getY() - (12 + self.puntaje * 0.2) * dt)

            fuego = huevo.find("**/FuegoLlama")
            if not fuego.isEmpty():
                escala = 1.2 + math.sin(globalClock.getFrameTime() * 10) * 0.15
                fuego.setScale(escala, escala, escala + 0.2)

            destruido = False

            for rayo in self.rayos[:]:
                if rayo.isEmpty():
                    continue

                distancia = (huevo.getPos() - rayo.getPos()).length()
                if distancia < 2.0:
                    huevo.removeNode()
                    if huevo in self.obstaculos:
                        self.obstaculos.remove(huevo)
                    rayo.removeNode()
                    if rayo in self.rayos:
                        self.rayos.remove(rayo)
                    self.puntaje += 1
                    print(f"¡Huevo reventado! Puntaje: {self.puntaje}")
                    destruido = True
                    break

            if destruido or huevo.isEmpty():
                continue

            if not self.game_over:
                distancia_patito = (
                    huevo.getPos() - self.patito.getPos()
                ).length()
                if distancia_patito < 2.0:
                    self.game_over = True
                    print(f"¡CHOQUE! Puntaje final: {self.puntaje}")

            if not huevo.isEmpty() and huevo.getY() < -10:
                huevo.removeNode()
                if huevo in self.obstaculos:
                    self.obstaculos.remove(huevo)

        return Task.cont


if __name__ == "__main__":
    app = JuegoPatitoLaguna()
    app.run()
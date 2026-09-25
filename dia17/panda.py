from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    AmbientLight,
    BitMask32,
    CollisionHandlerPusher,
    CollisionNode,
    CollisionSphere,
    CollisionTraverser,
    DirectionalLight,
    Vec3,
    Vec4,
)


class MiAplicacion(ShowBase):

    def __init__(self):
        super().__init__()

        self.disableMouse()

        # ----------------------------------------------------
        # CARGA DE MODELOS
        # ----------------------------------------------------
        self.entorno = self.loader.loadModel("models/environment")
        self.entorno.reparentTo(self.render)
        self.entorno.setScale(0.25, 0.25, 0.25)
        self.entorno.setPos(-8, 42, 0)

        self.personaje = self.loader.loadModel("models/panda-model")
        self.personaje.reparentTo(self.render)
        self.personaje.setScale(0.005, 0.005, 0.005)
        self.personaje.setPos(0, 10, 0)

        # ----------------------------------------------------
        # ILUMINACIÓN BÁSICA
        # ----------------------------------------------------
        self.configurar_luces()

        # ----------------------------------------------------
        # CÁMARA Y SUS CONTROLES (Flechas del teclado)
        # ----------------------------------------------------
        self.camera.setPos(0, -20, 15)
        self.camera.setP(-20)
        self.velocidad_camara = 20
        self.dir_camara = Vec3(0, 0, 0)

        self.accept("arrow_left", self.set_camara_x, [-1])
        self.accept("arrow_left-up", self.set_camara_x, [0])

        self.accept("arrow_right", self.set_camara_x, [1])
        self.accept("arrow_right-up", self.set_camara_x, [0])

        self.accept("arrow_up", self.set_camara_y, [1])
        self.accept("arrow_up-up", self.set_camara_y, [0])

        self.accept("arrow_down", self.set_camara_y, [-1])
        self.accept("arrow_down-up", self.set_camara_y, [0])

        # ----------------------------------------------------
        # MOVIMIENTO DEL PANDA (Teclas W, S, A, Z)
        # ----------------------------------------------------
        self.velocidad_panda = 12
        self.dir_panda = Vec3(0, 0, 0)

        self.accept("w", self.set_panda_y, [1])
        self.accept("w-up", self.set_panda_y, [0])

        self.accept("s", self.set_panda_y, [-1])
        self.accept("s-up", self.set_panda_y, [0])

        self.accept("a", self.set_panda_x, [-1])
        self.accept("a-up", self.set_panda_x, [0])

        self.accept("z", self.set_panda_x, [1])
        self.accept("z-up", self.set_panda_x, [0])

        # ----------------------------------------------------
        # SISTEMA DE COLISIONES
        # ----------------------------------------------------
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        # Esfera de colisión para el Panda
        nodo_col_panda = CollisionNode("panda_colisionador")
        nodo_col_panda.addSolid(CollisionSphere(0, 0, 300, 350))
        c_node_path = self.personaje.attachNewNode(nodo_col_panda)

        self.pusher.addCollider(c_node_path, self.personaje)
        self.cTrav.addCollider(c_node_path, self.pusher)

        # Máscara de colisión para las rocas / entorno
        self.entorno.setCollideMask(BitMask32.bit(0))

        # ----------------------------------------------------
        # TAREAS DEL BUCLE PRINCIPAL
        # ----------------------------------------------------
        self.taskMgr.add(self.mover_personaje, "MoverPersonaje")
        self.taskMgr.add(self.rotar_personaje_sobre_si_mismo, "RotarPersonaje")
        self.taskMgr.add(self.mover_camara, "MoverCamara")

    def configurar_luces(self):
        luz_ambiente = AmbientLight("luz_ambiente")
        luz_ambiente.setColor(Vec4(0.3, 0.3, 0.3, 1))
        nodo_ambiente = self.render.attachNewNode(luz_ambiente)
        self.render.setLight(nodo_ambiente)

        luz_direccional = DirectionalLight("luz_direccional")
        luz_direccional.setColor(Vec4(0.8, 0.8, 0.8, 1))
        nodo_direccional = self.render.attachNewNode(luz_direccional)
        nodo_direccional.setHpr(45, -45, 0)
        self.render.setLight(nodo_direccional)

    # Métodos de dirección para el Panda
    def set_panda_x(self, valor):
        self.dir_panda.setX(valor)

    def set_panda_y(self, valor):
        self.dir_panda.setY(valor)

    # Métodos de dirección para la Cámara
    def set_camara_x(self, valor):
        self.dir_camara.setX(valor)

    def set_camara_y(self, valor):
        self.dir_camara.setY(valor)

    def mover_personaje(self, tarea):
        dt = globalClock.getDt()
        if self.dir_panda.lengthSquared() > 0:
            desplazamiento = self.dir_panda * self.velocidad_panda * dt
            nueva_pos = self.personaje.getPos() + desplazamiento
            self.personaje.setPos(nueva_pos)
        return Task.cont

    def rotar_personaje_sobre_si_mismo(self, tarea):
        dt = globalClock.getDt()
        # Rota de forma continua sobre su eje Z
        self.personaje.setH(self.personaje.getH() + 45 * dt)
        return Task.cont

    def mover_camara(self, tarea):
        dt = globalClock.getDt()
        if self.dir_camara.lengthSquared() > 0:
            desplazamiento = self.dir_camara * self.velocidad_camara * dt
            nueva_pos = self.camera.getPos() + self.camera.getRelativeVector(
                self.camera, desplazamiento
            )
            self.camera.setPos(nueva_pos)
        return Task.cont


app = MiAplicacion()
app.run()
import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Patito vs Huevos de Fuego")
reloj = pygame.time.Clock()

# Colores
NEGRO = (20, 20, 30)
BLANCO = (255, 255, 255)
AMARILLO_PATITO = (255, 220, 30)
NARANJA_PICO = (255, 120, 0)
HUEVO_COLOR = (240, 230, 210)
FUEGO_AMARILLO = (255, 230, 0)
FUEGO_NARANJA = (255, 100, 0)
ROJO_TEXTO = (240, 60, 60)

# Fuente del sistema integrada
fuente = pygame.font.Font(None, 36)

# ----------------------------------------------------
# CLASE JUGADOR (El Patito Amarillo)
# ----------------------------------------------------
class Patito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.velocidad = 8
        self.dibujar_patito()

    def dibujar_patito(self):
        # Cuerpo del patito
        pygame.draw.circle(self.image, AMARILLO_PATITO, (25, 30), 18)
        # Cabeza del patito
        pygame.draw.circle(self.image, AMARILLO_PATITO, (25, 15), 12)
        # Ojo negro
        pygame.draw.circle(self.image, (0, 0, 0), (29, 12), 2)
        # Pico naranja
        pygame.draw.polygon(self.image, NARANJA_PICO, [(33, 14), (43, 17), (33, 20)])

    def actualizar(self, teclas):
        # Movimiento exclusivamente horizontal (izquierda / derecha)
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

# ----------------------------------------------------
# CLASE OBSTÁCULO (Huevo con Fuego)
# ----------------------------------------------------
class HuevoFuego(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 60), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - 45)
        self.rect.y = random.randint(-100, -40)
        self.velocidad = random.randint(4, 9)
        self.dibujar_huevo_fuego()

    def dibujar_huevo_fuego(self):
        # Llamas de fuego al fondo (amarillo y naranja)
        pygame.draw.ellipse(self.image, FUEGO_NARANJA, (5, 0, 35, 55))
        pygame.draw.ellipse(self.image, FUEGO_AMARILLO, (10, 8, 25, 45))
        # Huevo en el centro
        pygame.draw.ellipse(self.image, HUEVO_COLOR, (12, 18, 21, 30))

    def update(self):
        self.rect.y += self.velocidad
        # Eliminar al salir de la pantalla
        if self.rect.top > ALTO:
            self.kill()

# ----------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO
# ----------------------------------------------------
patito = Patito()
grupo_jugador = pygame.sprite.GroupSingle(patito)
obstaculos = pygame.sprite.Group()

puntaje = 0
game_over = False
contador_spawn = 0
frecuencia_spawn = 30  # Controla la velocidad de aparición inicial

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if not game_over:
        patito.actualizar(teclas)

        # Aumento progresivo de dificultad (caen más huevos con el tiempo)
        contador_spawn += 1
        if contador_spawn >= frecuencia_spawn:
            obstaculos.add(HuevoFuego())
            contador_spawn = 0
            if frecuencia_spawn > 8:
                frecuencia_spawn -= 0.1

        obstaculos.update()

        # Detección de colisiones
        if pygame.sprite.spritecollide(patito, obstaculos, False):
            game_over = True

        puntaje += 1
    else:
        # Reiniciar partida con la tecla ESPACIO
        if teclas[pygame.K_SPACE]:
            patito = Patito()
            grupo_jugador = pygame.sprite.GroupSingle(patito)
            obstaculos.empty()
            puntaje = 0
            frecuencia_spawn = 30
            game_over = False

    # Renderizado en pantalla
    pantalla.fill(NEGRO)
    grupo_jugador.draw(pantalla)
    obstaculos.draw(pantalla)

    # Marcador de Puntaje
    txt_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(txt_puntaje, (15, 15))

    # Pantalla de Game Over
    if game_over:
        txt_go = fuente.render("¡PATITO FRITO! Presioná [ESPACIO]", True, ROJO_TEXTO)
        rect_go = txt_go.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(txt_go, rect_go)

    pygame.display.flip()
    reloj.tick(60)
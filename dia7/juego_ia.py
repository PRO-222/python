import pygame
import random
import math

# 1. Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 600, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los Obstáculos en Llamas")

reloj = pygame.time.Clock()

# Colores principales
NEGRO = (10, 10, 20)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)
VERDE = (46, 204, 113)

# 2. Fondo espacial con estrellas
estrellas = []
for _ in range(80):
    ex = random.randint(0, ANCHO)
    ey = random.randint(0, ALTO)
    tamano = random.randint(1, 3)
    brillo = random.randint(100, 255)
    estrellas.append([ex, ey, tamano, brillo])

# 3. Configuración del jugador
radio_jugador = 18
velocidad_jugador = 5

def reiniciar_jugador():
    global x_jugador, y_jugador
    x_jugador = ANCHO // 2
    y_jugador = ALTO - radio_jugador - 15

reiniciar_jugador()

# 4. Configuración de Obstáculos
ancho_obstaculo_inicial = 80
alto_obstaculo = 22
velocidad_obstaculo_inicial = 3
num_obstaculos = 5
distancia_entre_obstaculos = (ALTO - 100) // num_obstaculos

obstaculos = []

def crear_obstaculo(y, nivel):
    ancho = ancho_obstaculo_inicial + (nivel - 1) * 10
    velocidad = velocidad_obstaculo_inicial + (nivel - 1) * 0.5
    if random.random() < 0.5:
        velocidad *= -1
    x = random.randint(0, ANCHO - ancho)
    return {"rect": pygame.Rect(x, y, ancho, alto_obstaculo), "velocidad": velocidad}

def inicializar_obstaculos(nivel):
    global obstaculos
    obstaculos = []
    for i in range(num_obstaculos):
        y = 50 + i * distancia_entre_obstaculos
        obstaculos.append(crear_obstaculo(y, nivel))

nivel_actual = 1
inicializar_obstaculos(nivel_actual)

# 5. Meta
ancho_meta, alto_meta = 120, 30
meta_rect = pygame.Rect(ANCHO // 2 - ancho_meta // 2, 8, ancho_meta, alto_meta)

# 6. Sistema de Explosión y Fuego
particulas_explosion = []
particulas_fuego = []

def generar_explosion(cx, cy):
    """Crea una ráfaga de chispas rojas, amarillas y naranjas al colisionar."""
    for _ in range(40):
        angulo = random.uniform(0, 2 * math.pi)
        vel = random.uniform(2, 7)
        vx = math.cos(angulo) * vel
        vy = math.sin(angulo) * vel
        radio_p = random.randint(3, 6)
        color = random.choice([(255, 50, 0), (255, 200, 0), (255, 100, 0), (255, 255, 200)])
        vida = random.randint(15, 30)
        particulas_explosion.append([cx, cy, vx, vy, radio_p, color, vida])

def generar_fuego_obstaculos():
    """Genera llamas pequeñas en los bordes de cada bloque."""
    for obs in obstaculos:
        r = obs["rect"]
        for _ in range(2):
            fx = random.randint(r.left, r.right)
            fy = r.bottom if obs["velocidad"] > 0 else r.top
            vy = random.uniform(1, 3) if obs["velocidad"] > 0 else random.uniform(-3, -1)
            vx = random.uniform(-0.8, 0.8)
            tamano = random.randint(3, 6)
            color = random.choice([(255, 60, 0), (255, 150, 0), (255, 220, 0)])
            vida = random.randint(10, 20)
            particulas_fuego.append([fx, fy, vx, vy, tamano, color, vida])

# Variables de control
jugando = True
en_explosion = False
tiempo_inicio_explosion = 0

# --- Bucle Principal ---
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()

    # Movimiento del jugador (solo si no explotó)
    if not en_explosion:
        if teclas[pygame.K_UP] and y_jugador - radio_jugador > 0:
            y_jugador -= velocidad_jugador
        if teclas[pygame.K_DOWN] and y_jugador + radio_jugador < ALTO:
            y_jugador += velocidad_jugador
        if teclas[pygame.K_LEFT] and x_jugador - radio_jugador > 0:
            x_jugador -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and x_jugador + radio_jugador < ANCHO:
            x_jugador += velocidad_jugador

    # Movimiento y CORRECCIÓN DE REBOTE en los obstáculos
    for obs in obstaculos:
        obs["rect"].x += obs["velocidad"]

        # Rebote corregido para evitar que queden pegados fuera de la ventana
        if obs["rect"].right >= ANCHO:
            obs["rect"].right = ANCHO
            obs["velocidad"] = -abs(obs["velocidad"])  # Forzar dirección hacia la izquierda
        elif obs["rect"].left <= 0:
            obs["rect"].left = 0
            obs["velocidad"] = abs(obs["velocidad"])   # Forzar dirección hacia la derecha

    # Partículas de fuego en bloques
    generar_fuego_obstaculos()

    # Detección de colisiones
    rect_jugador = pygame.Rect(x_jugador - radio_jugador, y_jugador - radio_jugador, radio_jugador * 2, radio_jugador * 2)

    if not en_explosion:
        for obs in obstaculos:
            if rect_jugador.colliderect(obs["rect"]):
                generar_explosion(x_jugador, y_jugador)
                en_explosion = True
                tiempo_inicio_explosion = pygame.time.get_ticks()
                break

    # Pausa tras explotar
    if en_explosion and pygame.time.get_ticks() - tiempo_inicio_explosion > 500:
        en_explosion = False
        reiniciar_jugador()

    # Avance de nivel al llegar a la meta
    if not en_explosion and rect_jugador.colliderect(meta_rect):
        nivel_actual += 1
        reiniciar_jugador()
        inicializar_obstaculos(nivel_actual)

    # --- DIBUJADO EN PANTALLA ---
    ventana.fill(NEGRO)
    for est in estrellas:
        pygame.draw.circle(ventana, (est[3], est[3], est[3]), (est[0], est[1]), est[2])

    # Dibujar Meta
    pygame.draw.rect(ventana, VERDE, meta_rect, border_radius=6)
    fuente = pygame.font.SysFont("Arial", 18, bold=True)
    txt_meta = fuente.render("META", True, BLANCO)
    ventana.blit(txt_meta, (meta_rect.x + 35, meta_rect.y + 4))

    # Dibujar Fuego
    for pf in particulas_fuego[:]:
        pf[0] += pf[2]
        pf[1] += pf[3]
        pf[6] -= 1
        if pf[6] <= 0:
            particulas_fuego.remove(pf)
        else:
            pygame.draw.circle(ventana, pf[5], (int(pf[0]), int(pf[1])), int(pf[4]))

    # Dibujar Bloques
    for obs in obstaculos:
        r = obs["rect"]
        pygame.draw.rect(ventana, (180, 30, 10), r, border_radius=4)
        pygame.draw.rect(ventana, (255, 180, 0), r, width=2, border_radius=4)

    # Dibujar Jugador
    if not en_explosion:
        pygame.draw.circle(ventana, AZUL, (x_jugador, y_jugador), radio_jugador)
        pygame.draw.circle(ventana, (180, 220, 255), (x_jugador - 5, y_jugador - 5), 5)

    # Dibujar Explosión
    for p in particulas_explosion[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[6] -= 1
        if p[6] <= 0:
            particulas_explosion.remove(p)
        else:
            pygame.draw.circle(ventana, p[5], (int(p[0]), int(p[1])), int(p[4]))

    # Texto del Nivel
    txt_nivel = fuente.render(f"Nivel: {nivel_actual}", True, BLANCO)
    ventana.blit(txt_nivel, (10, ALTO - 30))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
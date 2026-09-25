import pygame

pygame.init()
ANCHO, ALTO = 600, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

x, y = 300, 200
velocidad = 5
radio = 20

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()

    # Movimiento en las 4 direcciones
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_UP]:
        y -= velocidad
    if teclas[pygame.K_DOWN]:
        y += velocidad

    # Límites para que el círculo no salga de la pantalla
    if x - radio < 0:
        x = radio
    if x + radio > ANCHO:
        x = ANCHO - radio
    if y - radio < 0:
        y = radio
    if y + radio > ALTO:
        y = ALTO - radio

    ventana.fill((255, 255, 255))
    pygame.draw.circle(ventana, (30, 60, 200), (x, y), radio)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# 1. Inicializar aplicación
app = Ursina()

# 2. Variable global para la textura actual
block_texture = 'grass' 

# Diccionario de optimización para comprobar posiciones en O(1)
voxels_en_mundo = {}

class Voxel(Entity): 
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = block_texture, 
            color = color.color(0, 0, random.uniform(0.9, 1)),
            scale = 1,
            collider = 'box' 
        )
        # Registramos este bloque en nuestro diccionario global
        voxels_en_mundo[position] = self

# 3. Entrada de teclado y mouse unificada (Mapeo rápido)
TEXTURAS = {
    '1': 'stone', '2': 'grass', '3': 'glass', '4': 'brick', '5': 'box',
    '6': 'glowstone', '7': 'wood', '8': 'leaves', '9': 'terminal', '0': 'happy'
}

def input(key):
    global block_texture
    
    # Cambiar de bloque con los números
    if key in TEXTURAS:
        block_texture = TEXTURAS[key]
        
    # Detectar interacciones del mouse usando el sistema de Raycast nativo
    if key == 'left mouse down':
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
            bloque = mouse.hovered_entity
            pos = bloque.position
            if pos in voxels_en_mundo:
                del voxels_en_mundo[pos] # Lo eliminamos del registro
            destroy(bloque)
            
    if key == 'right mouse down':
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
            nueva_pos = mouse.hovered_entity.position + mouse.normal
            # Redondeamos la posición para evitar errores decimales en el diccionario
            nueva_pos = Vec3(round(nueva_pos.x), round(nueva_pos.y), round(nueva_pos.z))
            
            if nueva_pos not in voxels_en_mundo:
                Voxel(position = nueva_pos)

# 4. Bucle de actualización (Anti-caídas optimizado)
def update():
    if jugador.y < -20:
        jugador.position = (17, 10, 17)
        
        # Comprobación instantánea en el diccionario sin bucles for lentos
        if (17, 0, 17) not in voxels_en_mundo:
            for x in range(16, 19):
                for z in range(16, 19):
                    pos_plataforma = Vec3(x, 0, z)
                    if pos_plataforma not in voxels_en_mundo:
                        Voxel(position=pos_plataforma)

# 5. Generar el suelo inicial (35x35)
for z in range(35):
    for x in range(35):
        Voxel(position=(x, 0, z))

# 6. Añadir el jugador
jugador = FirstPersonController()
jugador.position = (17, 2, 17)

# Ejecutar el juego
app.run()


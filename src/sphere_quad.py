################################# Vision por Computador ###############################################
# @author Miguel Angel                                                                                #
# 23 de marzo/20                                                                                      #
########################################## Imports ####################################################
import pygame                                                                                         #
from pygame.locals import *                                                                           #
from OpenGL.GL import *                                                                               #
from OpenGL.GLUT import *                                                                             #
from OpenGL.GLU import *                                                                              #
from math import *                                                                                    #
#######################################################################################################

# Last time when sphere was re-displayed
last_time = 0

# Number of latitudes in sphere
lats = 4

# Number of longitudes in sphere
longs = 4

# Direction of light
direction = [0.0, 2.0, -1.0, 1.0]

# Intensity of light
intensity = [0.7, 0.7, 0.7, 1.0]

# Intensity of ambient light
ambient_intensity = [0.3, 0.3, 0.3, 1.0]

# The surface type(Flat or Smooth)
surface = GL_FLAT


def Sphere():
    for i in range(0, lats + 1):
        lat0 = pi * (-0.5 + float(float(i - 1) / float(lats)))
        z0 = sin(lat0)
        zr0 = cos(lat0)

        lat1 = pi * (-0.5 + float(float(i) / float(lats)))
        z1 = sin(lat1)
        zr1 = cos(lat1)

        # Use GL_STRIPS to draw the sphere
        glBegin(GL_QUAD_STRIP)

        for j in range(0, longs + 1):
            lng = 2 * pi * float(float(j - 1) / float(longs))
            x = cos(lng)
            y = sin(lng)
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)

        glEnd()


def main():
    
    global lats
    global longs
    
    count = 0
    
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGLBLIT|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    ############################## Light Setup ##########################################
    # Set OpenGL parameters
    glEnable(GL_DEPTH_TEST)
    
    # Set color to white
    glColor3f(1.0, 1.0, 1.0)

    # Set shade model
    glShadeModel(surface)
    
    # Enable lighting
    glEnable(GL_LIGHTING)

    # Set light model
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_intensity)

    # Enable light number 0
    glEnable(GL_LIGHT0)

    # Set position and intensity of light
    glLightfv(GL_LIGHT0, GL_POSITION, direction)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, intensity)    
    
    # Setup the material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    #####################################################################################

    glTranslatef(0.0,0.0, -5)

    while True:
        
        count = count + 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(2, 0, 2, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # Ejecute Sphere rendering
        Sphere()
        pygame.display.flip()
        pygame.time.wait(10)
        
        
        if count%100==0:
            lats = lats + 2
            longs = longs + 2


main() 












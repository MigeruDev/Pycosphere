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

# Number of longitudes in sphere
longs = 0

# Direction of light
direction = [0.0, 2.0, -1.0, 1.0]

# Intensity of light
intensity = [0.7, 0.7, 0.7, 1.0]

# Intensity of ambient light
ambient_intensity = [0.3, 0.3, 0.3, 1.0]

# The surface type(Flat or Smooth)
surface = GL_FLAT


phi = (sqrt(5) + 1) / 2
size = sqrt( 1.0 / ( 1 + phi * phi ) )
verts = [
    ( phi * size,        size,         0.0), #0
    ( phi * size,       -size,         0.0), #1
    (-phi * size,       -size,         0.0), #2
    (-phi * size,        size,         0.0), #3
    (      -size,         0.0,  phi * size), #4
    (       size,         0.0,  phi * size), #5
    (       size,         0.0, -phi * size), #6
    (      -size,         0.0, -phi * size), #7
    (        0.0,  phi * size,        size), #8
    (        0.0,  phi * size,       -size), #9
    (        0.0, -phi * size,       -size), #10
    (        0.0, -phi * size,        size), #11
]

# 20 equiangular triangles
edges = [
    [  5,  4, 11,],
    [  5, 11,  1,],
    [  5,  1,  0,],
    [  0,  8,  5,],
    [  5,  8,  4,],
    [  6,  7,  9,],
    [  9,  7,  3,],
    [  3,  7,  2,],
    [  2,  7, 10,],
    [ 10,  7,  6,],
    [  9,  3,  8,],
    [  9,  8,  0,],
    [  9,  0,  6,],
    [  6,  0,  1,],
    [  6,  1, 10,],
    [ 10,  1, 11,],
    [ 10, 11,  2,],
    [  2, 11,  4,],
    [  2,  4,  3,],
    [  3,  4,  8,]
]


middle_point_cache = {} 

def vertex(x, y, z): 
    """ Return vertex coordinates fixed to the unit sphere """ 
    length = sqrt(x**2 + y**2 + z**2) 
    return [(i * 1) / length for i in (x,y,z)]



def middle_point(point_1, point_2):
    """ Find a middle point and project to the unit sphere """
    # We check if we have already cut this edge first 
    # # to avoid duplicated verts 
    smaller_index = min(point_1, point_2) 
    greater_index = max(point_1, point_2)
    
    key = '{0}-{1}'.format(smaller_index, greater_index)
    
    if key in middle_point_cache:
        return middle_point_cache[key]
    
    # If it's not in cache, then we can cut it
    vert_1 = verts[point_1] 
    vert_2 = verts[point_2]
    middle = [sum(i)/2 for i in zip(vert_1, vert_2)]
    
    verts.append(vertex(*middle))
    
    index = len(verts) - 1 
    middle_point_cache[key] = index 
    return index
    
    
def Icosphere_Subdiv(subdivs):
    global edges
    for i in range(subdivs):
        edges_subdiv = []
        
        for tri in edges: 
            v1 = middle_point(tri[0], tri[1]) 
            v2 = middle_point(tri[1], tri[2]) 
            v3 = middle_point(tri[2], tri[0])
            
            edges_subdiv.append([tri[0], v1, v3]) 
            edges_subdiv.append([tri[1], v2, v1]) 
            edges_subdiv.append([tri[2], v3, v2]) 
            edges_subdiv.append([v1, v2, v3])
        
        edges = edges_subdiv

def Icosphere(screen):
            
    glBegin(GL_TRIANGLE_STRIP)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verts[vertex])
            glNormal3fv(verts[vertex])
            
    glEnd()


def main():
    
    global longs
    
    count = 0
    
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|OPENGLBLIT)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
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
        Icosphere(screen)
        
        pygame.display.flip()
        pygame.time.wait(10)
        
        if count%100==0 and longs<2:
            longs = longs + 1
            Icosphere_Subdiv(longs)


main() 












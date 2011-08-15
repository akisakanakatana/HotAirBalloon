import sys

from math import *
from array import array

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


x = 0
y = 0
z = 0

def prepare_gl ():
    """ Reinitialize GL at first of every loop. """
    # set screen size
    glViewport (0, 0, 640, 480)

    # set background
    glClearColor (0.8, 0.8, 0.9, 0)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable (GL_DEPTH_TEST)
    glDisable (GL_LIGHTING)
    glEnable (GL_LIGHTING)
    glEnable (GL_NORMALIZE)
    glShadeModel (GL_FLAT)

    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (45, 1.3333, 0.2, 20)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity ()

    # light origin setting
    glLightfv (GL_LIGHT0, GL_POSITION, [0,0,1,0])
    glLightfv (GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLightfv (GL_LIGHT0, GL_SPECULAR, [1,1,1,1])
    glEnable (GL_LIGHT0)

    # camera setting
    gluLookAt (2.4, 3.6, 4.8, 0.5, 0.5, 0, 0, 1, 0)

def draw_body ():
    global x, y, z
    green = [0.0, 1.0, 0.0, 1.0]
    glMaterialfv (GL_FRONT_AND_BACK, GL_DIFFUSE, green)
    R = array ('f', [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
    glPushMatrix ()
    glMultMatrixd (rot)
    sx, sy, sz = 1.0, 1.0, 1.0
    glScale (sx, sy, sz)
    glutSolidCube (1)
    glPopMatrix ()

def init_gl ():
    """ Initialize GL only once time. """
    glutInit ([])
    glutInitDisplayMode (GLUT_RGB | GLUT_DOUBLE)

    x, y = 0, 0
    w, h = 640, 480
    
    glutInitWindowPosition (x, y)
    glutInitWindowSize (w, h)
    glutCreateWindow ("test")

    glEnable (GL_CULL_FACE)
    glCullFace (GL_BACK)

def _keyfunc (c, x, y):
    """ Keyboard event. """
    sys.exit (0)

def _drawfunc ():
    """ Draw event. """
    prepare_gl ()
    draw_body ()
    glutSwapBuffers ()

def _idlefunc ():
    """ Loop body. """
    global x, y, z
    x += 0.01
    glutPostRedisplay ()

def main ():
    init_gl ()
    glutKeyboardFunc (_keyfunc)
    glutDisplayFunc (_drawfunc)
    glutIdleFunc (_idlefunc)

    glutMainLoop ()

if __name__ == "__main__":
    main ()


           

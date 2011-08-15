
import sys

sys.path.append (".")

#import time
import Image

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#import Atom
import String
import Plot
import Formula
import input

width = 800
height = 400
# mssg_file = "mssg.bmp"
# bld_file = "bld.bmp"
chars_file = "chars.png"
# spf = 1.0 / 30
# wait = 1
# fps_format = "%2.2f"
# drawskip_threshold = 1.4
param = {
    "T0": {"type": float, "value": 15.0},
    "H":  {"type": float, "value": 6000.0},
    "P0": {"type": float, "value": 1013.25},
}

# atoms = None
chars = None
# bld_texture = None
chars_texture = None
disp_list = None
input_buffer = []

# loop
# last_time = 0

# fps
# last_fps = 0
# curr_fps = 0
# lastsec_time = 0.0

class Texture2D:
    def __init__ (self, tex, bits, width, height, component):
        self.texture = tex
        self.bits = bits
        self.width = width
        self.height = height
        self.component_size = component
        if component == 3:
            self.component = GL_RGB
        else:
            self.component = GL_RGBA

    def bindTexture (self):
        glBindTexture (GL_TEXTURE_2D, self.texture)

    def bind (self):
        self.bindTexture ()
        glTexImage2D (
            GL_TEXTURE_2D, 0, self.component_size,
            self.width, self.height, 0,
            self.component, GL_UNSIGNED_BYTE, self.bits)

# def init_atoms (file, disp):
#     global atoms

#     im = Image.open (file)
#     width, height = im.size
#     atoms = [[Atom.atom (x, y) for x in range (0, width)
#                                if im.getpixel ((x,y)) < 128]
#              for y in range (0, height)]
#     atoms = Atom.atomManager (atoms, disp)

def init_etc ():
    global input_buffer
    input_buffer = input.Input ()
    
def init_chars (disp):
    global chars
    chars = String.string (disp)

def prepare_gl ():
    """ Reinitialize GL at first of every loop. """

    # set background
    glClearColor (0.0, 0.0, 0.0, 0)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glDisable (GL_LIGHTING)
    glDisable (GL_NORMALIZE)

    glEnable (GL_LIGHTING)
    glEnable (GL_NORMALIZE)

    glShadeModel (GL_FLAT)

    glEnable (GL_LIGHT0)

def drawLoadchart (P0, T0, H):
    H = Formula.ftToM (H)
    
    # loadchart
    plot = Plot.DiscreteGraph (-50, 40, 0.15, 0.40)

    # calculation
    def toAndDrho (tz, h):
        to = Formula.temperature (tz, h)
        ap = Formula.atmosPressure (P0, tz, h)
        f = lambda t:Formula.densOfDryAir (t, ap)
        return (to, f (to) - f (100.0))

    for i in range (0, 8):
        h = Formula.ftToM (i * 3000.0)
        line = [toAndDrho (ot, h)
                for ot in map (lambda t:t*10.0, range (-1, 5))]
        plot.append (Plot.Line (line, [1.0, i*0.08, i*0.08]))

    for ot in map (lambda t:15.0+t*10.0, range (-2, 3)):
        line = [toAndDrho (ot, h)
                for h in map (
                    lambda i:Formula.ftToM (i * 3000.0), range (0, 8))]
        plot.append (Plot.Line (line, [0.3, 0.3, 0.8]))

    end_t, end_rho = toAndDrho (T0, H)
    line = [(T0, 0.15)] + \
           [toAndDrho (T0, H)
            for h in map (
                lambda i:Formula.ftToM (i * 3000.0),
                range (0, int (h / 3000.0) + 1))] + \
                [(end_t, end_rho), (-50.0, end_rho)]
    plot.append (Plot.Line (line, [0.3, 1.0, 0.5]))

    # draw
    graph = plot.make ()

    glLineWidth (0.1)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPushMatrix ()

    glEnable (GL_TEXTURE_2D)
    chars_texture.bind ()
    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glColor3f (0.8, 0.8, 0.8)
#    graph.drawTitle (chars, "LOAD CHART", 0.1)
    graph.drawLabel (chars, 0.05,
                     "OUTER TEMPERATURE", "BUOYANT FORCE")
    graph.drawAxis2 (chars, 0.05, 10.0, "%.0f", 0.05, "%.2f")
    glDisable (GL_TEXTURE_2D)

    graph.draw ()
    glColor3f (0.2, 0.2, 0.2)
    graph.drawGrid2 (10.0, 0.05)

    glPopMatrix ()

def draw_body ():

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity ()
    gluLookAt (0.0,  0.0, -0.5,
               0.0,  0.0,  1.0,
               0.0, -1.0,  0.0)

    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()

    glOrtho (-2.4, 2.4, -1.2, 1.2, 0.1, 2.0)

    glScalef (2.0, 2.0, 1.0)

    P0 = param["P0"]["value"]
    T0 = param["T0"]["value"]
    H  = param["H"]["value"]

    # loadchart
    drawLoadchart (P0, T0, H)

    glEnable (GL_TEXTURE_2D)
    chars_texture.bind ()
    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glColor3f (1.0, 1.0, 1.0)
    
    # parameter
    glPushMatrix ()
    glTranslatef (0.8, 0.5, 0.0)
    glScalef (0.05, 0.05, 1.0)
    p = [str(k)+":"+str(v["value"]) for k,v in param.items ()]
    chars.drawLines (p, fix=True)
    glPopMatrix ()

    # buffer
    glPushMatrix ()
    glTranslatef (-1.0, -0.55, 0.0)
    glScalef (0.05, 0.05, 1.0)
    chars.draw (input_buffer.text (), fix=True)
    glPopMatrix ()

    glDisable (GL_TEXTURE_2D)
    
    glPushMatrix ()
    glTranslatef (-1.0125 + 0.025 * input_buffer.position (), -0.55, 0.0)
    glScalef (0.01, 0.05, 1.0)
    glBegin (GL_LINES)
    glVertex3f (0.0, -0.5, -0.1)
    glVertex3f (0.0,  0.5, -0.1)
    glEnd ()
    glPopMatrix ()
    
#     # number
#     glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
#     chars_texture.bind ()
#     glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#     glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

#     glPushMatrix ()

#     glColor3f (0.0, 0.0, 0.0)
#     glTranslatef (0.7, -0.9, 0.8)
#     glScalef (0.08, 0.08, 1.0)

#     chars.draw (fps_format % last_fps)

#     glPopMatrix ()

#     # set perspective
#     glMatrixMode (GL_PROJECTION)
#     glLoadIdentity ()

#     gluPerspective (120, width/height, 0.1, 2.0)

def mouse_callback (button, state, x, y):
    """ Mouse event callback. """
    sys.exit (0)
    
def key_callback (c, x, y):
    """ Keyboard event callback. """
    global input_buffer
    ch = "%c" % c
    m = glutGetModifiers ()
#    print (ch, m)
    if m == GLUT_ACTIVE_CTRL:
        if ch == "\x11": sys.exit (0) # q
        elif ch == "\x02": input_buffer.before () # b
        elif ch == "\x06": input_buffer.fore () # f
        elif ch == "\x04": input_buffer.delete () # d
        elif ch == "\x08": input_buffer.backspace () # h
        elif ch == "\x01": input_buffer.begin () # a
        elif ch == "\x05": input_buffer.end () # e
        elif ch == "\x0b": input_buffer.kill () # k
        elif ch == "\x10": input_buffer.pre () # p
        elif ch == "\x0e": input_buffer.nex () # n
        elif ch == "\x0d": interpret (input_buffer.submit ()) # m
    else:
        if ch == "\x08": input_buffer.backspace () # backspace
        elif ch == "\r": interpret (input_buffer.submit ()) # enter
        else:
            input_buffer.insert (ch)
        #    print ("%c was pushed at (%d, %d)" % (c, x, y))
    glutPostRedisplay ()

def specialkey_callback (c, x, y):
    """ Special key event callback. """
    global input_buffer
    if c == GLUT_KEY_LEFT:
        input_buffer.before ()
    elif c == GLUT_KEY_RIGHT:
        input_buffer.fore ()
    glutPostRedisplay ()

def readWhile (cond, s, res):
    if not s: return (str.join ("", res), "")
    c = s.pop (0)
    if cond (c):
        res.append (c)
        return readWhile (cond, s, res)
    else:
        return (str.join ("", res), s)

def tokenize (s):
    token, rest = readWhile (lambda c:c!=" ", s, [])
    if not token:
        return []
    else:
        return [token] + tokenize (rest)

def evalFun (f, a, n):
    if len (a) < n: return None
    a = [a.pop (0) for i in range (0, n)]
    f (*a)
    
def evaluate (sl):
    if not sl: return None
    op = sl.pop (0)
    if op == "set":
        def f (n,v):
            if param.has_key (n):
                param[n].update ([("value", param[n]["type"](v))])
        evalFun (f, sl, 2)
    elif op == "exit":
        evalFun (lambda: sys.exit (0), sl, 0)
    else:
        print ("Undefined function "+ op)

def interpret (i):
    i = [c for c in i]
    tokens = tokenize (i)
    evaluate (tokens)

def draw ():
    """ Draw event callback. """
    prepare_gl ()
    draw_body ()
    glutSwapBuffers ()

def loop ():
    """ Loop body. """
    pass

#     global atoms, last_fps, curr_fps, last_time, lastsec_time

#     now1_time = time.time ()

#     # wait for fps
#     if last_time + spf > now1_time:
#         glutTimerFunc (wait, loop, 0)
#         return

#     atoms.update ()

#     # skip when process is heavy
#     now2_time = time.time ()
#     if last_time + spf * drawskip_threshold > now2_time:
#         glutPostRedisplay ()
# #    else:
# #        print ("display skipped")

#     last_time = now1_time

#     # update fps counter
#     if int (now1_time) != int (lastsec_time):
#         last_fps = curr_fps / (now1_time - lastsec_time)
#         curr_fps = 2
#         lastsec_time = now1_time
#     else:
#         curr_fps += 1

#     glutTimerFunc (wait, loop, 0)

def init_texture ():
#    global bld_texture, bld_file, chars_texture, chars_file
    global chars_texture, chars_file

    tex = glGenTextures (2)

#     bld = Image.open (bld_file)
#     width, height = bld.size
#     data = bld.tostring ()
#     bld_texture = Texture2D (tex[0], data, width, height, 3)
#     bld_texture.bind ()

    chars = Image.open (chars_file)
    width, height = chars.size
    data = chars.tostring ()
    chars_texture = Texture2D (tex[0], data, width, height, 4)
    
def init_gl ():
    global width, height, disp_list
    """ Initialize GL only once time. """
    
    glutInit ([])
    glutInitDisplayMode (GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowPosition (0, 0)
    glutInitWindowSize (width, height)
    glutCreateWindow ("Bld. Tokio marine Nichido in Aomori")

    # set screen size
    glViewport (0, 0, width, height)

    # light origin setting
    glLightfv (GL_LIGHT0, GL_POSITION, [-20.0, 20.0, -10.0, 0.0])
    glLightfv (GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 1.0, 1.0])
    glLightfv (GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightfv (GL_LIGHT0, GL_AMBIENT,  [0.8, 0.8, 0.8, 1.0])

    # draw only one side of polygon
    glEnable (GL_CULL_FACE)
    glCullFace (GL_FRONT)

    # depth test
    glEnable (GL_DEPTH_TEST)

    # alpha blend
    glEnable (GL_BLEND)

    # anti alias
    glEnable (GL_LINE_SMOOTH)

    # texture
    glEnable (GL_TEXTURE_2D)

    # material
    glEnable (GL_COLOR_MATERIAL)

    # normalize
    glEnable (GL_NORMALIZE)

    # display list
    tno_disp = 95
    disp = glGenLists (tno_disp)
    if disp == 0: raise Error
    disp_list = range (disp, disp + tno_disp)

def init_callback ():
    """ Initialize GL event callback functions. """
    glutMouseFunc (mouse_callback)
#    glutMotionFunc (_motionfunc)
    glutKeyboardFunc (key_callback)
    glutSpecialFunc (specialkey_callback)
    glutDisplayFunc (draw)
#    glutTimerFunc (wait, loop, 0)
    glutIdleFunc (loop)

def main ():
    init_gl ()
    init_callback ()
    init_texture ()
#     init_atoms (mssg_file, disp_list[0])
    init_chars (disp_list[0:95+0])
    init_etc ()

    glutMainLoop ()

if __name__ == "__main__":
    main ()


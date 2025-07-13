import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

normalized_mouse_coords = [0.5,0.5]

class mouse_coordinates():
    def __init__(self):
        self._x = 0
        self._y = 0

    def x(self):
        return self._x
    
    def y(self):
        return self._y
    
    def set_coords(self, x,y):
        self._x = x 
        self._y = y
    
def createShaderProgram():

    vertex_shader = """
    #version 330 core

    void main() {
        float x = -1.0 + float((gl_VertexID & 1) << 2);
        float y = -1.0 + float((gl_VertexID & 2) << 1);
        gl_Position = vec4(x, y, 0.0, 1.0);
    }
    """

    fragment_shader = """
    #version 330 core
    out vec4 FragColor;

    uniform vec2 u_resolution;
    uniform vec2 u_mouse;
    uniform float u_time;

    void main(){

        vec2 st = gl_FragCoord.xy/u_resolution.xy;
        st.x *= u_resolution.x/u_resolution.y;

        vec3 color = vec3(.0);
    
        vec2 point[5];
        point[0] = vec2(0.83,0.75);
        point[1] = vec2(0.60,0.07);
        point[2] = vec2(0.28,0.64);
        point[3] = vec2(0.31,0.26);
        point[0] = u_mouse;

        float m_dist = 1.;

        for(int i = 0; i < 5; i++){
            float dist = distance(st, point[i]);

            m_dist = min(m_dist, dist);
        }
        
        color += m_dist;

        //color -= step(.7,abs(sin(50.0*m_dist)))*.3;

        //color = vec3(1.0,1.0,1.0);

        FragColor = vec4(color,1.0);
    }
    """

    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    return shaderProgram

mouse_coords = mouse_coordinates()

def mouse_callback(window, xpos, ypos):

    height, width = glfw.get_window_size(window)

    mouse_coords.set_coords(xpos/width, 1 - ypos/height)

 
if __name__ == "__main__":

    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    width, height = 800, 800
    window = glfw.create_window(width, height, "Test", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)

    shaderProgram = createShaderProgram()
    glUseProgram(shaderProgram)

    glfw.set_cursor_pos_callback(window, mouse_callback)

    u_resolution_loc = glGetUniformLocation(shaderProgram, "u_resolution")
    u_mouse_loc = glGetUniformLocation(shaderProgram, "u_mouse")

    glClearColor(0.0, 0.0, 0.0, 1.0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT)


        glUniform2f(u_resolution_loc, width, height)
        glUniform2f(u_mouse_loc, mouse_coords.x(), mouse_coords.y())

        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)

    glfw.terminate()


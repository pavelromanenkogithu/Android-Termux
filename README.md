import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image
import glfw

VERTEX_SHADER = """
#version 330 core
in vec2 position;
in vec2 texCoords;
out vec2 vTexCoords;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    vTexCoords = texCoords;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 vTexCoords;
out vec4 fragColor;
uniform sampler2D myImage;
uniform float flipY;
void main()
{
    vec2 coords = vec2(vTexCoords.x, flipY - vTexCoords.y);
    fragColor = texture(myImage, coords);
}
"""

if not glfw.init():
    sys.exit()

window = glfw.create_window(800, 600, "Shader Playground", None, None)
glfw.make_context_current(window)

shader = compileProgram(
    compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
    compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
)

vertices = np.array([
    -1, -1, 0, 0,
     1, -1, 1, 0,
     1,  1, 1, 1,
    -1,  1, 0, 1
], dtype=np.float32)

indices = np.array([0,1,2, 2,3,0], dtype=np.uint32)

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
EBO = glGenBuffers(1)
glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(8))

image = Image.open("jeep.jpg").convert("RGBA")
img_data = np.array(image)
tex = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, tex)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
glGenerateMipmap(GL_TEXTURE_2D)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

flipY = 1.0
glUseProgram(shader)
flipY_loc = glGetUniformLocation(shader, "flipY")
glUniform1f(flipY_loc, flipY)
glUseProgram(0)

while not glfw.window_should_close(window):
    glfw.poll_events()
    keys = glfw.get_key(window, glfw.KEY_SPACE)
    if keys == glfw.PRESS:
        flipY = 1.0 - flipY
        glUseProgram(shader)
        glUniform1f(flipY_loc, flipY)
        glUseProgram(0)

    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader)
    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, tex)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    glfw.swap_buffers(window)

glfw.terminate()

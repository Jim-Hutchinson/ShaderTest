import sys
import numpy as np
import glfw
import OpenGL.GL.shaders as shaders
from OpenGL.GL import *
from OpenGL.GLU import *
import glm

def load_obj(file_path):
    """Load standard OBJ file with vertices and normals."""
    vertices = []
    normals = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    # Vertex line
                    vertices.append([float(x) for x in line.split()[1:4]])
                elif line.startswith('vn '):
                    # Normal line
                    normal = [float(x) for x in line.split()[1:4]]
                    norm = np.linalg.norm(normal)
                    normals.append(normal / norm if norm != 0 else [0, 0, 0])
                elif line.startswith('f '):
                    # Face line (if needed for triangulation)
                    pass

        # Convert to numpy arrays for rendering
        vertices_array = np.array(vertices, dtype=np.float32).flatten()
        normals_array = np.array(normals, dtype=np.float32).flatten()

        print(f"Total vertices: {len(vertices_array)//3}")
        print(f"Total normals: {len(normals_array)//3}")
        print(f"Vertex range: [{vertices_array.min()}, {vertices_array.max()}]")
        
        return vertices_array, normals_array

    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None

def main():
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "3D Model Viewer", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        return

    glfw.make_context_current(window)

    if len(sys.argv) < 2:
        print("Usage: python render.py <path_to_obj_file>")
        return

    # Load vertices and normals
    vertices, normals = load_obj(sys.argv[1])

    if vertices is None or normals is None:
        print("Failed to load model")
        glfw.terminate()
        return

    # Create VAO and VBOs
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # Vertex buffer
    vbo_vertices = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Normal buffer
    vbo_normals = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)

    # Load shaders
    with open('vertex_shader.glsl', 'r') as f:
        vertex_shader_source = f.read()

    with open('fragment_shader.glsl', 'r') as f:
        fragment_shader_source = f.read()

    # Compile shaders
    vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
    glUseProgram(shader_program)

    # Position attribute
    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
    position_loc = glGetAttribLocation(shader_program, 'aPosition')
    glEnableVertexAttribArray(position_loc)
    glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

    # Normal attribute
    glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
    normal_loc = glGetAttribLocation(shader_program, 'aNormal')
    glEnableVertexAttribArray(normal_loc)
    glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

    # Matrices with adjusted camera
    model = glm.rotate(glm.mat4(1.0), glm.radians(45.0), glm.vec3(1.0, 1.0, 0.0))
    view = glm.lookAt(
        glm.vec3(0.0, 0.0, 5.0),  # Move camera back
        glm.vec3(0.0, 0.0, 0.0),  
        glm.vec3(0.0, 1.0, 0.0)
    )
    projection = glm.perspective(glm.radians(45.0), 800.0/600.0, 0.1, 10.0)

    # Main loop
    while not glfw.window_should_close(window):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # Set uniform matrices
        glUniformMatrix4fv(glGetUniformLocation(shader_program, 'model'), 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(glGetUniformLocation(shader_program, 'view'), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(shader_program, 'projection'), 1, GL_FALSE, glm.value_ptr(projection))

        # Set uniform values
        glUniform3f(glGetUniformLocation(shader_program, 'lightPos'), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(shader_program, 'viewPos'), 0.0, 0.0, 5.0)
        glUniform3f(glGetUniformLocation(shader_program, 'lightColor'), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(shader_program, 'objectColor'), 0.8, 0.5, 0.2)

        # Draw the model
        glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
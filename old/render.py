import sys
import numpy as np
import glfw
import OpenGL.GL.shaders as shaders
from OpenGL.GL import *
from OpenGL.GLU import *
import glm

def compile_shader(source, shader_type):
    """Compile shader with error checking."""
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    # Check compilation status
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if status == GL_FALSE:
        error_log = glGetShaderInfoLog(shader)
        print(f"Shader compilation failed: {error_log.decode('utf-8')}")
        return None
    return shader

def load_obj(file_path):
    """Load standard OBJ file with vertices and normals, ensuring triangulation."""
    vertices = []
    normals = []
    faces = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertices.append([float(x) for x in line.split()[1:4]])
                elif line.startswith('vn '):
                    normal = [float(x) for x in line.split()[1:4]]
                    norm = np.linalg.norm(normal)
                    normals.append(normal / norm if norm != 0 else [0, 0, 0])
                elif line.startswith('f '):
                    # Triangulate faces, handling different OBJ formats
                    parts = [v.split('/') for v in line.split()[1:]]
                    
                    # Convert to zero-indexed vertices
                    face_vertices = [int(v[0])-1 for v in parts]
                    
                    # Triangulate polygon into multiple triangles
                    for i in range(1, len(face_vertices)-1):
                        faces.extend([
                            face_vertices[0],
                            face_vertices[i],
                            face_vertices[i+1]
                        ])

        # Reorder vertices and normals based on faces
        triangulated_vertices = np.array([vertices[i] for i in faces], dtype=np.float32)
        
        # Handle case where no normals are provided
        if normals:
            triangulated_normals = np.array([normals[i % len(normals)] for i in faces], dtype=np.float32)
        else:
            # Generate basic normals if not provided
            triangulated_normals = np.zeros_like(triangulated_vertices)

        print(f"Total triangulated vertices: {len(triangulated_vertices)}")
        print(f"Vertex range: [{triangulated_vertices.min()}, {triangulated_vertices.max()}]")
        
        return triangulated_vertices.flatten(), triangulated_normals.flatten(), triangulated_vertices

    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None, None

def calculate_model_bounds(vertices):
    """Calculate the bounding box and center of the model."""
    vertices_array = np.array(vertices)
    min_bounds = np.min(vertices_array, axis=0)
    max_bounds = np.max(vertices_array, axis=0)
    center = (min_bounds + max_bounds) / 2
    size = max_bounds - min_bounds
    max_dimension = max(size)
    
    return center, max_dimension

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
    vertices, normals, raw_vertices = load_obj(sys.argv[1])

    if vertices is None or normals is None:
        print("Failed to load model")
        glfw.terminate()
        return

    # Calculate model bounds
    model_center, model_size = calculate_model_bounds(raw_vertices)

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

    # Compile shaders with error checking
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    
    if not vertex_shader or not fragment_shader:
        print("Shader compilation failed")
        glfw.terminate()
        return

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    # Check program linking status
    link_status = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if link_status == GL_FALSE:
        error_log = glGetProgramInfoLog(shader_program)
        print(f"Shader program linking failed: {error_log.decode('utf-8')}")
        glfw.terminate()
        return

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

    # Dynamically adjust camera based on model size
    camera_distance = model_size * 2  # Adjust distance based on model size
    view = glm.lookAt(
        glm.vec3(0.0, 0.0, camera_distance),  # Dynamically set camera distance
        glm.vec3(model_center[0], model_center[1], model_center[2]),  # Look at model center  
        glm.vec3(0.0, 1.0, 0.0)
    )

    # Adjust perspective to ensure full model visibility
    aspect_ratio = 800.0 / 600.0
    fov = glm.radians(60.0)  # Increased FOV for wider view
    projection = glm.perspective(fov, aspect_ratio, 0.1, camera_distance * 2)

    # Rotation matrix to view model from a good angle
    model = glm.rotate(glm.mat4(1.0), glm.radians(45.0), glm.vec3(1.0, 1.0, 0.0))

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
        glUniform3f(glGetUniformLocation(shader_program, 'viewPos'), 0.0, 0.0, camera_distance)
        glUniform3f(glGetUniformLocation(shader_program, 'lightColor'), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(shader_program, 'objectColor'), 0.8, 0.5, 0.2)

        # Draw the model
        glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
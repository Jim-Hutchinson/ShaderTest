#version 330 core

layout(location = 0) in vec3 aPosition; // Position attribute
layout(location = 1) in vec3 aNormal;   // Normal attribute

uniform mat4 model;      // Model matrix
uniform mat4 view;       // View matrix
uniform mat4 projection; // Projection matrix

out vec3 fragNormal;     // Pass normal to the fragment shader
out vec3 fragPosition;   // Pass position to the fragment shader

void main() {
    // Normal transformation
    fragPosition = vec3(model * vec4(aPosition, 1.0));
    fragNormal = mat3(transpose(inverse(model))) * aNormal;
    // Final vertex position
    gl_Position = projection * view * vec4(fragPosition, 1.0);
}
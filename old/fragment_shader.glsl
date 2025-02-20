#version 330 core

in vec3 fragNormal;     // Interpolated normal from the vertex shader
in vec3 fragPosition;   // Interpolated position from the vertex shader

out vec4 fragColor;     // Output color

uniform vec3 lightPos;  // Light position
uniform vec3 viewPos;   // Camera/viewer position
uniform vec3 lightColor; // Light color
uniform vec3 objectColor; // Object color

void main() {
    // Ambient lighting
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse lighting
    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos - fragPosition);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Specular lighting
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - fragPosition);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = specularStrength * spec * lightColor;

    // Combine lighting components
    vec3 result = (ambient + diffuse + specular) * objectColor;
    fragColor = vec4(result, 1.0);
}
#version 450

struct Sphere {
    vec3 center;
    float radius;
    vec3 color;
};

struct Camera {
    vec3 position;
    vec3 forwards;
    vec3 right;
    vec3 up;
};

struct Ray {
    vec3 origin;
    vec3 direction;
};

// input/output
layout(local_size_x = 8, local_size_y = 8) in;
layout(rgba32f, binding = 0) uniform writeonly image2D img_output;

void main() {

    ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
    ivec2 screen_size = imageSize(img_output);
    float aspectRatio = float(screen_size.x) / float(screen_size.y);
    float horizontalCoefficient = (float(pixel_coords.x) / screen_size.x) * 2.0 - 1.0;
    float verticalCoefficient = (float(pixel_coords.y) / screen_size.y) * 2.0 - 1.0;

    vec3 pixel = vec3(0.0);

    Camera camera;
    camera.position = vec3(0.0);
    camera.forwards = vec3(1.0, 0.0, 0.0);
    camera.right = vec3(0.0, aspectRatio, 0.0);
    camera.up = vec3(0.0, 0.0, 1.0);

    Sphere sphere;
    sphere.center = vec3(3.0, 0.0, 0.0);
    sphere.radius = 1.0;
    sphere.color = vec3(1.0, 0.3, 0.7);

    Ray ray;
    ray.origin = camera.position;
    ray.direction = normalize(camera.forwards + horizontalCoefficient * camera.right + verticalCoefficient * camera.up);

    float a = dot(ray.direction, ray.direction);
    float b = 2.0 * dot(ray.direction, ray.origin - sphere.center);
    float c = dot(ray.origin - sphere.center, ray.origin - sphere.center) - sphere.radius * sphere.radius;
    float discriminant = b * b - 4.0 * a * c;

    if (discriminant > 0) {
        pixel += sphere.color;
    }

    imageStore(img_output, pixel_coords, vec4(pixel, 1.0));
}
# Ray Tracer Project

  I've done minecraft shaders in the past, but never fully understood what went on behind the scenes to prepare a scene to be rendered by ray tracing. This project is intended for me to learn how to take a scene from raw data and textures and put it on the screen. The basic functionality is here, but more is yet to come.

  This project uses an OpenGL compute shader to perform all ray tracing calculations, so doesn't need hardware RT support found in modern GPUs. As far as I can tell, the GTX 400 series is the oldest generation to support enough OpenGL features with a modern driver, along with AMD's Radeon HD7500 generation. I am unable to test on hardware this old, but anything supporting OpenGL version 4.3 or newer should work. The default resolution of 640x480 should be easy enough to run in ligher scenes than the included benchmark.

### To use:
  1. Check to make sure your GPU supports Open GL version 4.3 or higher.
  2. Ensure python 3.11.9 is installed on your computer. Newer versions should work, but I know this one does.
  3. Download the "ray tracer" folder and unzip it to a location you will remember.
  4. Make sure textures are all present in the texture folder. There should be 9 texture folders with 8 images each. Each image should be 1024 pixels square.
  5. Navigate to inside the "ray tracer" folder.
  6. Install dependencies from the requirements.txt file using "pip install -r requirements.txt"
  7. Set the desired resolution using the W and H variables for the screen width and height respectively. Aspect ratios should be 4:3 to avoid distortion for now. Setting the height to 0 or -1 will automatically force a 4:3 aspect ratio.
  8. Set the USE_FXAA varable to True to add anti-aliasing to the render. A debug version is included in the same shader file to visualize which pixels are being affected by FXAA.
  9. Save and run "runnner.py" to run the ray tracer.

### Editing Scenes:

  All scenes need all elements and functions in the scene.py file, so it's best to just copy and modify this file to make new scenes. All 3 geometry matrices must be the same size. The current default is 16x16, but smaller and larger are both possible. Note that larger scenes quickly consume more memory and run slower.

  Scenes are represented as a grid of cubes with the same texture on all sides. The number in a grid space corresponds to the texture of that cube. 0 means an empty or "air" cube.

  Spheres are defined by their center and radius. Spheres also have material properties such as their color and roughness. The sphere's axis determines how they will rotate. The motion radius determines how far from the axis the sphere is, and the velocity determines how quickly the sphere orbits that axis.

  Lights are also defined by their position in space. The radius determines the length of the path the light can move on. They move in a straight line, and I need to rename this. The axis value defines the direction the light can move in, and the velocity determines how quickly the light can travel along it.

  Doors connect rooms within a scene are are placed in the scene with the string "d" in the wall geometry matrix. The room and door system is not currently fully implemented and you can recreate this it with a hallway within a larger scene for now. Performance will be worse, but it works.

  Planes are used to construct the cubes with textures to make the walls, floor, and ceiling. Vertices and vertex count serve similar internal functionality.





### Known Issues
  * Player rotation can be extremely slow at times.
  * Camera collider feels inconsistent.
  * Spheres are invisible but cast shadows.
  * The player encounter an index out of bounds error while still inside the level when on a very low frame rate.
  * Window becomes fullscreen when height is close to or exceeds the monitor height on some systems.
  * Engine only supports 9 textures at the current resolution.

### Future additions
  * Performance optimizations for large scenes
  * Reflections via ray bounces
  * Aspect ratios beyond 4:3
  * Frame Rate Limit or Vsync option
  * Better scene file format

### Performance Metrics

|System|Resolution|Frame Rate|
|------|----------|----------|
|Ryzen 7840U Laptop|600x450|31 fps|
|Ryzen 7840U Laptop|800x600|17 fps|
|Ryzen 7840U Laptop|960x720|12 fps|
|8700 + 3050 6GB|960x720|7 fps|
|8700 + 3050 6GB|1200x900|4 fps|
|14700K + 7900XTX|1200x900|84 fps|
|14700K + 7900XTX|1920x1440|34 fps|

  Tests were performed in the default scene by watching the yellow light sweep across all 9 textures. Frame rates averaged over a 10-second test. Frame rates will initially be lower as the level loads in the first few seconds.
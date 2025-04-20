# Ray Tracer Project

  I've done minecraft shaders in the past, but never fully understood what went on behind the scenes to prepare a scene to be rendered by ray tracing. This project is intended for me to learn how to take a scene from raw data and textures and put it on the screen. The basic functionality is here, but more is yet to come.

  This project uses an OpenGL compute shader to perform all ray tracing calculations, so doesn't need hardware RT support found in modern GPUs. Your RX5000 or GTX1000-series or older graphics card is probably fine as long as it supports OpenGL version 4.3 or newer. The default resolution of 640x480 should be easy enough to run for even older integrated graphics.

### To use:
  1. Download the Ray Tracer folder and unzip it to a location you will remember.
  2. Make sure textures are all present in the texture folder. There should be 9 texture folders with 8 images each. Each image should be 1024 pixels square.
  3. Install dependencies from the requirements.txt file using "pip install -r requirements.txt"
  4. Set the desired resolution using the W and H variables for the screen width and height respectively. Aspect ratios should be 4:3 to avoid distortion for now. Setting the height to 0 or -1 will automatically force a 4:3 aspect ratio.
  5. Set the USE_FXAA varable to True to add anti-aliasing to the render. A debug version is included in the same shader file to visualize which pixels are being affected by FXAA.
  6. Save and run "runnner.py" to run the ray tracer.

### Editing Scenes:

  All scenes need all elements and functions in the scene.py file, so it's best to just copy and modify this file to make new scenes. All 3 geometry matrices must be the same size. The current default is 16x16, but smaller and larger are both possible. Note that larger scenes quickly consume more memory and run slower.

  Scenes are represented as a grid of cubes with the same texture on all sides. The number in a grid space corresponds to the texture of that cube. 0 means an empty or "air" cube.

  Spheres are defined by their center and radius. Spheres also have material properties such as their color and roughness. The sphere's axis determines how they will rotate. The motion radius determines how far from the axis the sphere is, and the velocity determines how quickly the sphere orbits that axis.

  Lights are also defined by their position in space. The radius is currently unused, but will in the future define the size of the emmissive sphere for calculating soft shadows. Set this to 0 for now. The axis value defines the direction the light can move in, and the velocity determines how quickly the light can travel along it.

  Doors connect rooms within a scene are are placed in the scene with the string "d" in the wall geometry matrix. The room and door system is not currently fully implemented and you can recreate this it with a hallway within a larger scene for now.

  Planes are used to construct the cubes with textures to make the walls, floor, and ceiling. Vertices and vertex count serve similar internal functionality.





### Known Issues
  * Player rotation can be extremely slow at times
  * Spheres are invisible but cast shadows
  * Doors have an incorrect texture
  * One textrure is not interacting with light sources correctly
  * Window becomes fullscreen when height is close to or exceeds the monitor height.

### Future additions

  * BVH acceleration structure building
  * Reflections via ray bounces
  * Aspect ratios beyond 4:3
  * Frame Rate Limit or Vsync option
  * Better scene file format

### Performance Metrics

|System|Resolution|Frame Rate|
|------|----------|----------|
|Ryzen 7840U Laptop|640x480|140 fps|
|Ryzen 7840U Laptop|800x600|84 fps|
|Ryzen 7840U Laptop|1200x900|51 fps|
|8700 + 3050 6GB|800x600|N fps|
|8700 + 3050 6GB|1200x900|N fps|
|8700 + 3050 6GB|1600x1200|N fps|
|14700K + 7900XTX|1200x900|N fps|
|14700K + 7900XTX|1600x1200|N fps|
|14700K + 7900XTX|1920x1440|N fps|

  Tests were performed in the default scene by moving the camera along the length of the hallway spinning 180 degrees, and then moving back and rotating again. This was repeated for 10 seconds and the frame rate averaged over that period. Frame rates will initially be lower when the scene first loads, but should quickly stabilize.

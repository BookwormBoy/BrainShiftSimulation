// create_mesh.geo - Gmsh script to create a brain-tumor mesh

// 1. Merge the STL files that define the surfaces
Merge "brain_surface.stl";
Merge "tumor_surface.stl";

// 2. Create discrete surfaces from the merged STL data.
// Gmsh automatically tags the first merged file as Surface(1), the second as Surface(2), etc.
Surface(1) = {1}; // Create a surface from the brain STL triangles
Surface(2) = {2}; // Create a surface from the tumor STL triangles

// 3. Define the surface loops that enclose the volumes.
// A surface loop is just a list of surfaces that form a closed boundary.
Surface Loop(1) = {1, 2}; // Boundary for the brain parenchyma (outer brain + inner tumor)
Surface Loop(2) = {2};    // Boundary for the tumor (just the tumor surface)

// 4. Define the volumes based on the surface loops.
Volume(1) = {1}; // The brain parenchyma volume is enclosed by Surface Loop 1
Volume(2) = {2}; // The tumor volume is enclosed by Surface Loop 2

// 5. Assign physical labels to the volumes. This is what FreeFem reads as 'region'.
// Physical Volume("Name", tag_number) = {list_of_volumes};
Physical Volume("Brain", 1) = {1};  // Assign label 1 to Volume 1
Physical Volume("Tumor", 2) = {2};  // Assign label 2 to Volume 2

// 6. Set mesh options (optional)
// For example, to set a characteristic length (element size) of 4 units:
// Mesh.CharacteristicLengthMax = 4;

// 7. Generate the 3D mesh
Mesh 3;

// 8. Save the mesh file in a FreeFem-compatible format
// It's best to explicitly set the version to 2.
Mesh.MshFileVersion = 2.2;
Save "brain_and_tumor.msh";

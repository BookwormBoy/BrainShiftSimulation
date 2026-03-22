Mesh.MshFileVersion = 2.2;

// Merge the STL surface files
Merge "TumourCoarse.stl";  // This usually becomes Surface 1
Merge "BrainCoarse.stl";  // This usually becomes Surface 2

// Create surface loops from the imported STLs
// Note: If your STLs contain multiple patches, you may need 
// to inspect tags in the Gmsh GUI first.
Surface Loop(1) = {1}; // Tumor boundary
Surface Loop(2) = {2}; // Brain boundary

// Define the Volumes
Volume(1) = {1};       // Volume 1: The Tumor
Volume(2) = {2, 1};    // Volume 2: The Brain (outer loop 2, inner hole 1)

// Define Physical Groups for FreeFem++
// These tags are what you will use in FreeFem++ to identify regions
Physical Volume("Tumour", 10) = {1};
Physical Volume("Brain", 20) = {2};


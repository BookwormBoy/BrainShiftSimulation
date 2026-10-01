Mesh.MshFileVersion = 2.2;
Mesh.SaveAll = 0;
Mesh.AngleSmoothNormals = 30;
Mesh.StlRemoveDuplicateTriangles = 1;
Merge "../models/TumourCoarse_fixed.stl";
Merge "../models/VentriclesCoarse_fixed.stl";
Merge "../models/BrainCoarse_fixed.stl";

// Surface indices after merging: Tumour=1, Ventricles=2, Brain=3

// Tumour region (innermost, standalone)
Surface Loop(1) = {1};
Volume(1) = {1};

// Ventricles region (innermost, standalone)
Surface Loop(2) = {2};
Volume(2) = {2};

// Brain region: outer brain surface minus tumour and ventricle cavities
Surface Loop(3) = {3, 1, 2};
Volume(3) = {3};

Physical Volume("Tumour",     10) = {1};
Physical Volume("Ventricles", 30) = {2};
Physical Volume("Brain",      20) = {3};
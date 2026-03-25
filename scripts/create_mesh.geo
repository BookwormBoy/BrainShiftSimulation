Mesh.MshFileVersion = 2.2;
Mesh.SaveAll = 0;

Merge "TumourCoarse.stl";
Merge "BrainCoarse.stl";

Surface Loop(1) = {1};
Surface Loop(2) = {2, 1};

Volume(1) = {1};
Volume(2) = {2};

Physical Volume("Tumour", 10) = {1};
Physical Volume("Brain",  20) = {2};
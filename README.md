# procedural_voronoi

lien objet3D: https://www.thingiverse.com/shapeforge/collections/voronoi-foams

lien presentation : https://docs.google.com/presentation/d/1Qvi6oxT6lVkppdV_g9MJXBOVw84Do3dTdGSU9LfqaMI/edit#slide=id.p

paraview:
 -> Download: https://www.paraview.org/download/

 Pour charger un modele .mhd/.raw:

    -> decompresser le zip

    -> ouvrir le .mhd avec paraview

    -> changer Representation : -> Volume

    -> mettre shade

Pour charger un modele .stl:

    -> ouvrir .stl avec paraview

Doc:

    model/volume.py #Script permettant d'ouvrir le volume sous forme de Numpy array 3D
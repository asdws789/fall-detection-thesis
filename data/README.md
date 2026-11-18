# Adathalmazok (Datasets)

Ez a könyvtár tartalmazza a kutatáshoz felhasznált nyers és előfeldolgozott vázadatokat.

## Mappastruktúra:
* `raw/`: A letöltött referencia-adatbázisok (UR Fall Detection, Le2i Fall) videói vagy csomagjai. (A `.gitignore` miatt nem kerülnek fel a Git repóba).
* `processed/`: A YOLOv8-Pose által kinyert, normalizált `.npy` és `.pkl` váz- és gráfkoordináták.

## Adathalmaz források:
1. **UR Fall Detection Dataset (URFD):** http://fenix.ur.edu.pl/~mkepski/ds/uf.html
2. **Le2i Fall Detection Dataset:** http://le2i.cnrs.fr/Fall-detection-Dataset

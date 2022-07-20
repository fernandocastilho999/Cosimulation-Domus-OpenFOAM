#!/bin/bash

# run Mesh
./salome -t salomeMeshGen.py
echo "Finished Mesh!"

# Activate OpenFOAM
#FoamExtend
#source $HOME/foam/foam-extend-4.1/etc/bashrc
# Openfoam9
source /opt/openfoam9/etc/bashrc
# Paraview
# export PATH=/opt/ParaView-5.9.1-MPI-Linux-Python3.8-64bit/bin:$PATH

python3 settingFoam.py

# Go to case directory
casedir=../foam/laplacianFoam/
cd $casedir

# Symbolic linking the mesh
ln -sf ../scripts/clean clean
ln -sf ../../scripts/test/mesh01.unv mesh01.unv
# ln -sf ../../salome/mesh01.unv mesh01.unv

ideasUnvToFoam mesh01.unv

checkMesh
# touch case.foam

laplacianFoam

# paraFoam -touchAll
paraFoam
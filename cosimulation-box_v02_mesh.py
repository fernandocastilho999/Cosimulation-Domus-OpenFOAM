##############################################################
# 1) IMPORTAR GEOMETRIA


# 1.1) Libraries
import SMESH
from salome.smesh import smeshBuilder
import SALOMEDS
import math
from salome.geom import geomBuilder
import GEOM
import salome_notebook
import salome
import sys
from pyidf.idf import IDF
import logging
import codecs

# 1.2) Change codification
##############################################################
# CHANGE FILE CODIFICATION
dirGeom = '/media/hdd3/vboxFiles/pucpr/research/energy/domus/ap04/'
dirPj = '/home/fernando/workspace/research/phd/seminar/ap04/'
fn = 'box_exported'

with codecs.open(dirGeom+fn+'.idf', 'r', encoding='latin-1') as file:
    lines = file.read()
# write output file
fnu = dirPj+fn+'_utf8'+'.idf'
with codecs.open(fnu, 'w', encoding='utf-8') as file:
    file.write(lines)

# 1.3 More libraries
logging.info("start")
idf = IDF(fnu)

##############################################################
# 2)  SALOME GEOMETRY
##############################################################

#!/usr/bin/env python

###
# This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

dirSalome = '/home/fernando/workspace/research/phd/seminar/ap04/salome/'
salome.salome_init()
notebook = salome_notebook.NoteBook()
sys.path.insert(0, dirSalome)

###
# GEOM component
###


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy(O, 'O')
geompy.addToStudy(OX, 'OX')
geompy.addToStudy(OY, 'OY')
geompy.addToStudy(OZ, 'OZ')
##############################################################


##############################################################
# READ FILE
j = 0
faces = []
znmax = 0


dzfloor = 0
xmin = 0
xmax = 0
ymin = 0
ymax = 0
zmin = 0
zmax = 0

for surfaces in idf['BuildingSurface:Detailed']:
    zone = surfaces['Zone Name'].replace(" ", "")
    zonenum = zone[4:len(zone)].zfill(2)
    if int(zonenum) > znmax:
        znmax = int(zonenum)
    # print(zonenum)

    nome = surfaces.name.replace(" ", "")
    # print( nome )

    vx = surfaces.extensibles

    vtx = []
    vty = []
    vtz = []
    for i in range(len(vx)):
        vtx.append(vx[i][0])
        vty.append(vx[i][1])
        vtz.append(vx[i][2])

    if dzfloor < max(vtz) and zonenum == '01':
        dzfloor = max(vtz)

    if xmin > min(vtx) and zonenum != '01':
        xmin = min(vtx)
    if xmax < max(vtx) and zonenum != '01':
        xmax = max(vtx)
    if ymin > min(vty) and zonenum != '01':
        ymin = min(vty)
    if ymax < max(vty) and zonenum != '01':
        ymax = max(vty)
    if zmin > min(vtz) and zonenum != '01':
        zmin = min(vtz)
    if zmax < max(vtz) and zonenum != '01':
        zmax = max(vtz)

    if min(vtz) == max(vtz):
        # print('xy')
        exec('p1 = geompy.MakeVertex('+str(min(vtx)) +
             ','+str(min(vty))+','+str(vtz[0])+')')
        exec('p2 = geompy.MakeVertex('+str(min(vtx)) +
             ','+str(max(vty))+','+str(vtz[0])+')')
        exec('p3 = geompy.MakeVertex('+str(max(vtx)) +
             ','+str(max(vty))+','+str(vtz[0])+')')
        exec('p4 = geompy.MakeVertex('+str(max(vtx)) +
             ','+str(min(vty))+','+str(vtz[0])+')')
    elif min(vty) == max(vty):
        # print('xz')
        exec('p1 = geompy.MakeVertex('+str(min(vtx)) +
             ','+str(vty[0])+','+str(min(vtz))+')')
        exec('p2 = geompy.MakeVertex('+str(min(vtx)) +
             ','+str(vty[0])+','+str(max(vtz))+')')
        exec('p3 = geompy.MakeVertex('+str(max(vtx)) +
             ','+str(vty[0])+','+str(max(vtz))+')')
        exec('p4 = geompy.MakeVertex('+str(max(vtx)) +
             ','+str(vty[0])+','+str(min(vtz))+')')
    elif min(vtx) == max(vtx):
        # print('yz')
        exec('p1 = geompy.MakeVertex(' +
             str(vtx[0])+','+str(min(vty))+','+str(min(vtz))+')')
        exec('p2 = geompy.MakeVertex(' +
             str(vtx[0])+','+str(min(vty))+','+str(max(vtz))+')')
        exec('p3 = geompy.MakeVertex(' +
             str(vtx[0])+','+str(max(vty))+','+str(max(vtz))+')')
        exec('p4 = geompy.MakeVertex(' +
             str(vtx[0])+','+str(max(vty))+','+str(min(vtz))+')')
    else:
        print('err')

    wireName = 'zn'+zonenum+'_wire'+str(j)
    exec(wireName+' = geompy.MakePolyline([p1,p2,p3,p4], True)')
    # exec("geompy.addToStudy( "+wireName+", '"+wireName+"')")

    faceName = 'zn'+zonenum+'_face'+str(j)
    exec(faceName+' = geompy.MakeFaceWires(['+wireName+'], 1)')
    # exec("geompy.addToStudy( "+faceName+", '"+faceName+"')")

    faces.append(faceName)
    j = j+1


clb = ''
for j in range(znmax):
    solid_list = [x for x in faces if 'zn'+str(j+1).zfill(2) in x]

    obj = ""
    for i in range(len(solid_list)):
        obj += str(solid_list[i])
        if i < len(solid_list)-1:
            obj += ','

    solidName = 'zone'+str(j+1).zfill(2)
    cmd = solidName+' = geompy.MakeSolidFromConnectedFaces(['+obj+'],True)'
    exec(cmd)
    # exec("geompy.addToStudy( "+solidName+", '"+solidName+"')")

    clb += str(solidName)
    if j < znmax-1:
        clb += ','


building1 = 'predio1'
exec(building1+' = geompy.MakeCompound(['+clb+'])')
# exec("geompy.addToStudy( "+building1+", '"+building1+"')")

bb1 = geompy.BoundingBox(predio1, True)
Lx = bb1[1]-bb1[0]
Ly = bb1[3]-bb1[2]
Lz = bb1[5]-bb1[4]

plane1 = geompy.MakePlane2Vec(OX, OZ, 2*max([Lx, Ly, Lz]))
plane2 = geompy.MakeTranslation(plane1, 0, 0, Lz)

plane3a = geompy.MakePlane2Vec(OY, OX, 2*max([Lx, Ly, Lz]))
plane3b = geompy.MakeTranslation(plane3a, -Lx/2, 0, 0)
plane3c = geompy.MakeTranslation(plane3a, Lx/2, 0, 0)
# geompy.addToStudy(plane3b, 'plane3b')
# geompy.addToStudy(plane3c, 'plane3c')

plane4a = geompy.MakePlane2Vec(OX, OY, 2*max([Lx, Ly, Lz]))
plane4b = geompy.MakeTranslation(plane4a, 0, -Ly/2, 0)
plane4c = geompy.MakeTranslation(plane4a, 0, Ly/2, 0)
# geompy.addToStudy(plane4b, 'plane4b')
# geompy.addToStudy(plane4c, 'plane4c')


th = 0.3

centerSolid = geompy.MakeTranslation(O, 0, 0, Lz/2)
predio_thick = geompy.MakeScaleAlongAxes(
    predio1, centerSolid, (Lx+th)/Lx, (Ly+th)/Ly, (Lz+th)/Lz)
# geompy.addToStudy(predio_thick, 'predio_thick')

predioWalls = geompy.MakeCutList(predio_thick, [predio1], True)
# geompy.addToStudy(predioWalls, 'predioWalls')


building1 = geompy.ProcessShape(predioWalls, ["FixShape", "FixFaceSize", "DropSmallEdges", "SameParameter"], [
                                "FixShape.Tolerance3d", "FixShape.MaxTolerance3d", "FixFaceSize.Tolerance", "DropSmallEdges.Tolerance3d", "SameParameter.Tolerance3d"], ["1e-07", "1", "0.05", "0.05", "1e-07"])


partition1 = geompy.MakePartition([building1], [plane1, plane2], [], [
], geompy.ShapeType["SOLID"], 0, [], 0)

[floor, walls, roof] = geompy.ExtractShapes(
    partition1, geompy.ShapeType["SOLID"], True)


wall1 = geompy.MakePartition([walls], [plane3b, plane3c, plane4b, plane4c], [
], [], geompy.ShapeType["SOLID"], 0, [], 0)
floor1 = geompy.MakePartition(
    [floor], [wall1], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
roof1 = geompy.MakePartition(
    [roof], [wall1], [], [], geompy.ShapeType["SOLID"], 0, [], 0)


wall = geompy.ProcessShape(wall1, ["FixShape", "FixFaceSize", "DropSmallEdges", "SameParameter"], ["FixShape.Tolerance3d", "FixShape.MaxTolerance3d",
                           "FixFaceSize.Tolerance", "DropSmallEdges.Tolerance3d", "SameParameter.Tolerance3d"], ["1e-07", "1", "0.05", "0.05", "1e-07"])

floor = geompy.ProcessShape(floor1, ["FixShape", "FixFaceSize", "DropSmallEdges", "SameParameter"], ["FixShape.Tolerance3d", "FixShape.MaxTolerance3d",
                            "FixFaceSize.Tolerance", "DropSmallEdges.Tolerance3d", "SameParameter.Tolerance3d"], ["1e-07", "1", "0.05", "0.05", "1e-07"])

roof = geompy.ProcessShape(roof1, ["FixShape", "FixFaceSize", "DropSmallEdges", "SameParameter"], ["FixShape.Tolerance3d", "FixShape.MaxTolerance3d",
                           "FixFaceSize.Tolerance", "DropSmallEdges.Tolerance3d", "SameParameter.Tolerance3d"], ["1e-07", "1", "0.05", "0.05", "1e-07"])


building = geompy.MakeCompound([floor, wall, roof])
geompy.addToStudy(building, 'building')
geompy.addToStudyInFather(building, floor, 'floor')
geompy.addToStudyInFather(building, wall, 'wall')
geompy.addToStudyInFather(building, roof, 'roof')


##############################################################
##############################################################
floor_ext = geompy.CreateGroup(floor, geompy.ShapeType["FACE"])
geompy.UnionIDs(floor_ext, [17])
floor_int = geompy.CreateGroup(floor, geompy.ShapeType["FACE"])
geompy.UnionIDs(floor_int, [81])
roof_ext = geompy.CreateGroup(roof, geompy.ShapeType["FACE"])
geompy.UnionIDs(roof_ext, [3])
roof_int = geompy.CreateGroup(roof, geompy.ShapeType["FACE"])
geompy.UnionIDs(roof_int, [81])
wall_int_E = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_int_E, [82])
wall_int_W = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_int_W, [134])
wall_int_N = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_int_N, [58])
wall_int_S = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_int_S, [158])
wall_ext_E = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_ext_E, [62])
wall_ext_W = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_ext_W, [154])
wall_ext_N = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_ext_N, [38])
wall_ext_S = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_ext_S, [175])
geompy.addToStudyInFather(floor, floor_ext, 'floor_ext')
geompy.addToStudyInFather(floor, floor_int, 'floor_int')
geompy.addToStudyInFather(roof, roof_ext, 'roof_ext')
geompy.addToStudyInFather(roof, roof_int, 'roof_int')
geompy.addToStudyInFather(wall, wall_int_E, 'wall_int_E')
geompy.addToStudyInFather(wall, wall_int_W, 'wall_int_W')
geompy.addToStudyInFather(wall, wall_int_N, 'wall_int_N')
geompy.addToStudyInFather(wall, wall_int_S, 'wall_int_S')
geompy.addToStudyInFather(wall, wall_ext_E, 'wall_ext_E')
geompy.addToStudyInFather(wall, wall_ext_W, 'wall_ext_W')
geompy.addToStudyInFather(wall, wall_ext_N, 'wall_ext_N')
geompy.addToStudyInFather(wall, wall_ext_S, 'wall_ext_S')


##############################################################

floor_interface = geompy.CreateGroup(floor, geompy.ShapeType["FACE"])
geompy.UnionIDs(floor_interface, [53, 58, 43, 65, 71, 33, 38, 48])
floor_external = geompy.CreateGroup(floor, geompy.ShapeType["FACE"])
geompy.UnionIDs(floor_external, [24, 3, 79, 76])
wall_interface = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_interface, [189, 21, 79, 169, 141, 127, 45, 93, 151,
                117, 179, 69, 31, 103, 55, 172, 74, 146, 162, 106, 130, 50, 34, 26])
wall_external = geompy.CreateGroup(wall, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall_external, [192, 4, 98, 14, 122, 110, 86, 184])
roof_interface = geompy.CreateGroup(roof, geompy.ShapeType["FACE"])
geompy.UnionIDs(roof_interface, [67, 59, 70, 49, 54, 79, 75, 64])
roof_external = geompy.CreateGroup(roof, geompy.ShapeType["FACE"])
geompy.UnionIDs(roof_external, [42, 33, 24, 13])
geompy.addToStudyInFather(floor, floor_interface, 'floor_interface')
geompy.addToStudyInFather(floor, floor_external, 'floor_external')
geompy.addToStudyInFather(wall, wall_interface, 'wall_interface')
geompy.addToStudyInFather(wall, wall_external, 'wall_external')
geompy.addToStudyInFather(roof, roof_interface, 'roof_interface')
geompy.addToStudyInFather(roof, roof_external, 'roof_external')


# ##############################################################
# [Edge_1, Edge_2, Edge_3, Edge_4, Edge_5, Edge_6, Edge_7, Edge_8, Edge_9, Edge_10, Edge_11, Edge_12, Edge_13, Edge_14, Edge_15, Edge_16, Edge_17, Edge_18, Edge_19, Edge_20, Edge_21, Edge_22, Edge_23, Edge_24, Edge_25, Edge_26, Edge_27, Edge_28, Edge_29, Edge_30, Edge_31, Edge_32, Edge_33, Edge_34, Edge_35, Edge_36,
#     Edge_37, Edge_38, Edge_39, Edge_40, Edge_41, Edge_42, Edge_43, Edge_44, Edge_45, Edge_46, Edge_47, Edge_48, Edge_49, Edge_50, Edge_51, Edge_52, Edge_53, Edge_54, Edge_55, Edge_56, Edge_57, Edge_58, Edge_59, Edge_60, Edge_61, Edge_62, Edge_63, Edge_64] = geompy.ExtractShapes(wall, geompy.ShapeType["EDGE"], True)

# edges_wall = geompy.MakeCompound([Edge_1, Edge_2, Edge_3, Edge_4, Edge_5, Edge_6, Edge_7, Edge_8, Edge_9, Edge_10, Edge_11, Edge_12, Edge_13, Edge_14, Edge_15, Edge_16, Edge_17, Edge_18, Edge_19, Edge_20, Edge_21, Edge_22, Edge_23, Edge_24, Edge_25, Edge_26, Edge_27, Edge_28, Edge_29, Edge_30, Edge_31,
#                                  Edge_32, Edge_33, Edge_34, Edge_35, Edge_36, Edge_37, Edge_38, Edge_39, Edge_40, Edge_41, Edge_42, Edge_43, Edge_44, Edge_45, Edge_46, Edge_47, Edge_48, Edge_49, Edge_50, Edge_51, Edge_52, Edge_53, Edge_54, Edge_55, Edge_56, Edge_57, Edge_58, Edge_59, Edge_60, Edge_61, Edge_62, Edge_63, Edge_64])

# geompy.addToStudyInFather(wall, edges_wall, 'edges_wall')


# [Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, Face_17, Face_18, Face_19, Face_20, Face_21, Face_22, Face_23, Face_24, Face_25, Face_26, Face_27, Face_28, Face_29, Face_30, Face_31, Face_32, Face_33, Face_34, Face_35, Face_36,
#     Face_37, Face_38, Face_39, Face_40] = geompy.ExtractShapes(wall, geompy.ShapeType["FACE"], True)

# faces_wall = geompy.MakeCompound([Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, Face_17, Face_18, Face_19, Face_20, Face_21, Face_22, Face_23, Face_24, Face_25, Face_26, Face_27, Face_28, Face_29, Face_30, Face_31,
#                                  Face_32, Face_33, Face_34, Face_35, Face_36, Face_37, Face_38, Face_39, Face_40])

# geompy.addToStudyInFather(wall, faces_wall, 'faces_wall')


# ##############################################################
# [Edge_1, Edge_2, Edge_3, Edge_4, Edge_5, Edge_6, Edge_7, Edge_8, Edge_9, Edge_10,
#     Edge_11, Edge_12, Edge_13, Edge_14, Edge_15, Edge_16, Edge_17, Edge_18, Edge_19, Edge_20, Edge_21, Edge_22, Edge_23, Edge_24, Edge_25, Edge_26, Edge_27, Edge_28, Edge_29, Edge_30, Edge_31, Edge_32] = geompy.ExtractShapes(floor, geompy.ShapeType["EDGE"], True)

# edges_floor = geompy.MakeCompound([Edge_1, Edge_2, Edge_3, Edge_4, Edge_5, Edge_6, Edge_7,
#                                    Edge_8, Edge_9, Edge_10, Edge_11, Edge_12, Edge_13, Edge_14, Edge_15, Edge_16, Edge_17, Edge_18, Edge_19, Edge_20, Edge_21, Edge_22, Edge_23, Edge_24, Edge_25, Edge_26, Edge_27, Edge_28, Edge_29, Edge_30, Edge_31, Edge_32])

# geompy.addToStudyInFather(floor, edges_floor, 'edges_floor')

# [Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9, Face_10,
#     Face_11, Face_12, Face_13, Face_14] = geompy.ExtractShapes(floor, geompy.ShapeType["FACE"], True)

# faces_floor = geompy.MakeCompound([Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7,
#                                    Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14])

# geompy.addToStudyInFather(floor, faces_floor, 'faces_floor')

# ##############################################################
# [Edge_1, Edge_2, Edge_3, Edge_4, Edge_5, Edge_6, Edge_7, Edge_8, Edge_9, Edge_10,
#     Edge_11, Edge_12, Edge_13, Edge_14, Edge_15, Edge_16, Edge_17, Edge_18, Edge_19, Edge_20, Edge_21, Edge_22, Edge_23, Edge_24, Edge_25, Edge_26, Edge_27, Edge_28, Edge_29, Edge_30, Edge_31, Edge_32] = geompy.ExtractShapes(roof, geompy.ShapeType["EDGE"], True)

# edges_roof = geompy.MakeCompound([Edge_1, Edge_2, Edge_3, Edge_4, Edge_5, Edge_6, Edge_7,
#                                   Edge_8, Edge_9, Edge_10, Edge_11, Edge_12, Edge_13, Edge_14, Edge_15, Edge_16, Edge_17, Edge_18, Edge_19, Edge_20, Edge_21, Edge_22, Edge_23, Edge_24, Edge_25, Edge_26, Edge_27, Edge_28, Edge_29, Edge_30, Edge_31, Edge_32])

# geompy.addToStudyInFather(roof, edges_roof, 'edges_roof')

# [Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9, Face_10,
#     Face_11, Face_12, Face_13, Face_14] = geompy.ExtractShapes(roof, geompy.ShapeType["FACE"], True)

# faces_roof = geompy.MakeCompound([Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7,
#                                   Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14])

# geompy.addToStudyInFather(roof, faces_roof, 'faces_roof')

##############################################################
##############################################################
##############################################################
###
# SMESH component
###


N = 5
ds = th/N/2

smesh = smeshBuilder.New()


mesh01 = smesh.Mesh(building)
Regular_1D = mesh01.Segment()
Local_Length_1 = Regular_1D.LocalLength(ds, None, 1e-07)
Quadrangle_2D = mesh01.Quadrangle(algo=smeshBuilder.QUADRANGLE)


# Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(Local_Length_1, 'Local Length_1')
smesh.SetName(mesh01.GetMesh(), 'mesh01')


isDone = mesh01.Compute()
##############################################################
##############################################################

floor_ext = mesh01.GroupOnGeom(floor_ext, 'floor_ext', SMESH.FACE)
floor_int = mesh01.GroupOnGeom(floor_int, 'floor_int', SMESH.FACE)
roof_ext = mesh01.GroupOnGeom(roof_ext, 'roof_ext', SMESH.FACE)
roof_int = mesh01.GroupOnGeom(roof_int, 'roof_int', SMESH.FACE)
wall_int_E = mesh01.GroupOnGeom(wall_int_E, 'wall_int_E', SMESH.FACE)
wall_int_W = mesh01.GroupOnGeom(wall_int_W, 'wall_int_W', SMESH.FACE)
wall_int_N = mesh01.GroupOnGeom(wall_int_N, 'wall_int_N', SMESH.FACE)
wall_int_S = mesh01.GroupOnGeom(wall_int_S, 'wall_int_S', SMESH.FACE)
wall_ext_E = mesh01.GroupOnGeom(wall_ext_E, 'wall_ext_E', SMESH.FACE)
wall_ext_W = mesh01.GroupOnGeom(wall_ext_W, 'wall_ext_W', SMESH.FACE)
wall_ext_N = mesh01.GroupOnGeom(wall_ext_N, 'wall_ext_N', SMESH.FACE)
wall_ext_S = mesh01.GroupOnGeom(wall_ext_S, 'wall_ext_S', SMESH.FACE)
##############################################################
floor_interface = mesh01.GroupOnGeom(
    floor_interface, 'floor_interface', SMESH.FACE)
floor_external = mesh01.GroupOnGeom(
    floor_external, 'floor_external', SMESH.FACE)
wall_interface = mesh01.GroupOnGeom(
    wall_interface, 'wall_interface', SMESH.FACE)
wall_external = mesh01.GroupOnGeom(wall_external, 'wall_external', SMESH.FACE)
roof_interface = mesh01.GroupOnGeom(
    roof_interface, 'roof_interface', SMESH.FACE)
roof_external = mesh01.GroupOnGeom(roof_external, 'roof_external', SMESH.FACE)


##############################################################
# diSalome = r'/home/fernando/workspace/research/phd/seminar/ap04/salomeDir/'
filename = '/home/fernando/workspace/research/phd/seminar/ap04/salomeDir/mesh01.unv'
# print(dirSalome+filename)
mesh01.ExportUNV(filename)


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()

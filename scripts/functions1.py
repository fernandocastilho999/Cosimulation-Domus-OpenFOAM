
import shutil
import os
import pandas as pd


def rel(x):
    return os.path.join(os.path.dirname(__file__), x)


dirshared = '/media/hdd3/vboxFiles/pucpr/research/energy/domus/ap04/'
odsfile = rel('../variables02.ods')


def create_df(df):
    df_bc = pd.DataFrame()
    df_prop = pd.DataFrame()
    df_ctl = pd.DataFrame()
    for i in range(len(df)):
        if df.typevar[i] == 'bc':
            df_bc = df_bc.append(
                {'name': df.name[i], 'd1': df.d1[i], 'd2': df.d2[i], 'd3': df.d3[i]}, ignore_index=True)
        elif df.typevar[i] == 'prop':
            df_prop = df_prop.append(
                {'name': df.name[i], 'd1': df.d1[i], 'd2': df.d2[i], 'd3': df.d3[i]}, ignore_index=True)
        elif df.typevar[i] == 'control':
            df_ctl = df_ctl.append(
                {'name': df.name[i], 'd1': df.d1[i], 'd2': df.d2[i], 'd3': df.d3[i]}, ignore_index=True)
        else:
            pass
    return df_bc, df_prop, df_ctl


def cleanFolder(x):
    if os.path.exists(x):
        try:
            shutil.rmtree(x)
        except OSError as e:
            print("Error: %s : %s" % (x, e.strerror))


def createDirs(casedir):
    cleanFolder(casedir)
    os.mkdir(casedir)
    os.mkdir(casedir+'/0')
    os.mkdir(casedir+'/constant')
    os.mkdir(casedir+'/system')


def w(f, x):
    f.write(x)
    f.write('\n')


def w_header(f):
    w(f, '/*--------------------------------*- C++ -*----------------------------------*\\')
    w(f, '| =========                 |                                                 |')
    w(f, '  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox')
    w(f, '   \\\\    /   O peration     | Website:  https://openfoam.org')
    w(f, '    \\\\  /    A nd           | Version:  9')
    w(f, '|    \\\\/     M anipulation  |                                                 |')
    w(f, '\\*---------------------------------------------------------------------------*/')


def w_bc(f, name, d1, d2, d3):
    w(f, '    '+name)
    w(f, '    {')
    w(f, '        type            '+d1+';')

    if d1 == 'fixedValue':
        w(f, '        value           '+d2+' '+str(d3)+';')

    w(f, '    }')
    w(f, '')


def create_0_T(casedir, df):
    with open(casedir+'/0/T', 'w') as f:
        w_header(f)
        w(f, 'FoamFile')
        w(f, '{')
        w(f, '    version     2.0;')
        w(f, '    format      ascii;')
        w(f, '    class       volScalarField;')
        w(f, '    object      T;')
        w(f, '}')
        w(f, '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //')
        w(f, '')
        w(f, 'dimensions      [0 0 0 1 0 0 0];')
        w(f, '')
        w(f, 'internalField   uniform 273;')
        w(f, '')
        w(f, 'boundaryField')
        w(f, '{')

        for i in range(len(df)):
            w_bc(f, df.name[i], df.d1[i], df.d2[i], df.d3[i])

        w(f, '}')
        w(f, '\n')
        w(f, '// ************************************************************************* //')
        # w(f, '')


def create_transProp(casedir, df):
    with open(casedir+'/constant/transportProperties', 'w') as f:
        w_header(f)
        w(f, 'FoamFile')
        w(f, '{')
        w(f, '    version     2.0;')
        w(f, '    format      ascii;')
        w(f, '    class       dictionary;')
        w(f, '    location    "constant";')
        w(f, '    object      transportProperties;')
        w(f, '}')
        w(f, '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //')
        w(f, '')
        w(f, df.name[0]+'              '+df.name[0] +
          ' [ 0 2 -1 0 0 0 0 ] '+str(df.d1[0])+';')
        w(f, '\n')
        w(f, '// ************************************************************************* //')


def create_fvSch(casedir):
    with open(casedir+'/system/fvSchemes', 'w') as f:
        w_header(f)
        w(f, 'FoamFile')
        w(f, '{')
        w(f, '    version     2.0;')
        w(f, '    format      ascii;')
        w(f, '    class       dictionary;')
        w(f, '    location    "system";')
        w(f, '    object      fvSchemes;')
        w(f, '}')
        w(f, '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //')
        w(f, '')
        w(f, 'ddtSchemes')
        w(f, '{')
        w(f, '    default         Euler;')
        w(f, '}')
        w(f, '')
        w(f, 'gradSchemes')
        w(f, '{')
        w(f, '    default         Gauss linear;')
        w(f, '    grad(T)         Gauss linear;')
        w(f, '}')
        w(f, '')
        w(f, 'divSchemes')
        w(f, '{')
        w(f, '    default         none;')
        w(f, '}')
        w(f, '')
        w(f, 'laplacianSchemes')
        w(f, '{')
        w(f, '    default         none;')
        w(f, '    laplacian(DT,T) Gauss linear corrected;')
        w(f, '}')
        w(f, '')
        w(f, 'interpolationSchemes')
        w(f, '{')
        w(f, '    default         linear;')
        w(f, '}')
        w(f, '')
        w(f, 'snGradSchemes')
        w(f, '{')
        w(f, '    default         corrected;')
        w(f, '}')
        w(f, '\n')
        w(f, '// ************************************************************************* //')


def create_fvSol(casedir):
    with open(casedir+'/system/fvSolution', 'w') as f:
        w_header(f)
        w(f, 'FoamFile')
        w(f, '{')
        w(f, '    version     2.0;')
        w(f, '    format      ascii;')
        w(f, '    class       dictionary;')
        w(f, '    location    "system";')
        w(f, '    object      fvSolution;')
        w(f, '}')
        w(f, '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //')
        w(f, '')
        w(f, 'solvers')
        w(f, '{')
        w(f, '    T')
        w(f, '    {')
        w(f, '        solver          PCG;')
        w(f, '        preconditioner  DIC;')
        w(f, '        tolerance       1e-06;')
        w(f, '        relTol          0;')
        w(f, '    }')
        w(f, '}')
        w(f, '')
        w(f, 'SIMPLE')
        w(f, '{')
        w(f, '    nNonOrthogonalCorrectors 2;')
        w(f, '}')
        w(f, '\n')
        w(f, '// ************************************************************************* //')


def create_ctlDict(casedir, df):
    with open(casedir+'/system/controlDict', 'w') as f:

        for i in range(len(df)):
            if df.name[i] == 'endTime':
                endTime = df.d1[i]
            elif df.name[i] == 'deltaT':
                deltaT = df.d1[i]
            elif df.name[i] == 'writeInterval':
                writeInterval = df.d1[i]

        w_header(f)
        w(f, 'FoamFile')
        w(f, '{')
        w(f, '    version     2.0;')
        w(f, '    format      ascii;')
        w(f, '    class       dictionary;')
        w(f, '    location    "system";')
        w(f, '    object      controlDict;')
        w(f, '}')
        w(f, '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //')
        w(f, 'application     laplacianFoam;\n')
        w(f, 'startFrom       latestTime;\n')
        w(f, 'stopAt          endTime;\n')
        w(f, 'endTime         '+str(endTime)+';\n')
        w(f, 'deltaT          '+str(deltaT)+';\n')
        w(f, 'writeControl    runTime;\n')
        w(f, 'writeInterval   '+str(writeInterval)+';\n')
        w(f, 'purgeWrite      0;\n')
        w(f, 'writeFormat     ascii;\n')
        w(f, 'writePrecision  6;\n')
        w(f, 'writeCompression uncompressed;\n')
        w(f, 'timeFormat      general;\n')
        w(f, 'timePrecision   6;\n')
        w(f, 'runTimeModifiable yes;')
        w(f, '\n')
        w(f, '// ************************************************************************* //')


def create_clean(casedir):
    with open(casedir+'/clean', 'w') as f:
        w(f, '#!/bin/sh')
        w(f, '')
        w(f, '. $WM_PROJECT_DIR/bin/tools/CleanFunctions')
        w(f, 'cleanCase')


def createDirsAndFiles(casedir, df_bc, df_prop, df_ctl):
    createDirs(casedir)
    create_0_T(casedir, df_bc)
    create_transProp(casedir, df_prop)
    create_fvSch(casedir)
    create_fvSol(casedir)
    create_ctlDict(casedir, df_ctl)
    # create_clean(casedir)

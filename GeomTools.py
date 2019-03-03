# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 19:20:30 2019

@author: gelbj
"""

import shapely
from shapely import geometry,wkt

"""
Ensemble de fonction de geometrie basee sur shapely
"""
##################################################
##Definitions des erreurs
##################################################
class TopologyError(Exception):
    """
    Raise me when their is something wrong with topology
    """
    pass


##################################################
##fonctions utilitaires liees a l'entendue d'objet
##################################################

def InExtent(Point,Extent) : 
    """
    Extent must be defined as : (minX,minY,MaxX,MaxY)
    """
    X,Y = Point.coords[0]
    if Extent[2]>=X and Extent[0]<=X and Extent[3]>=Y and Extent[1]<=Y : 
        return True
    else :
        return False
    
    
    
##################################################
##fonctions utilitaires appliquee a des lignes
##################################################
def GetExtremites(Line,Tolerance=0.01) : 
    Coords = Line.coords
    C1,C2 = shapely.geometry.Point(Coords[0]),shapely.geometry.Point(Coords[-1])
    return (C1,C2)

def GetPartsOfLine(Line) : 
    """
    Permet de recuperer toutes les lignes composant une line string
    """
    Coords = list(Line.coords)
    return [shapely.geometry.LineString([Coords[e],Coords[e+1]]) for e in range(len(Coords)-1)]

def ReverseLine(Line) : 
    """
    Fonction permettant de renverser l'ordre d'une ligne
    """
    Coords = list(Line.coords)
    Coords.reverse()
    return shapely.geometry.LineString(Coords)
    

def AppendLine(L1,L2,Tolerance=0.01) : 
    """
    Fonction permettant de combiner deux lignes devant se toucher (L2 est ajoutee a la fin de L1)
    """
    if LineTouches(L1,L2,Tolerance=Tolerance)==False : 
        raise TopologyError("The two line are not touching : "+shapely.wkt.dumps(L1)+"  \n"+shapely.wkt.dumps(L2))
    else : 
        A,B = GetExtremites(L1)
        C,D = GetExtremites(L2)
        if min([A.distance(C),A.distance(D)]) < min([B.distance(C),B.distance(D)]) : 
            L1 = ReverseLine(L1)
        if min([C.distance(A),C.distance(B)]) > min([D.distance(A),D.distance(B)]) :
            L2 = ReverseLine(L2)
        Coords = list(L1.coords)+list(L2.coords)
        return shapely.geometry.LineString(Coords)
            
    
def LineTouches(L1,L2,Tolerance=0.01):
    """
    Fonction permettant de determiner si deux lignes se touchent a leur extremites
    """
    A,B = GetExtremites(L1)
    C,D = GetExtremites(L2)
    if A.distance(C)<Tolerance or A.distance(D)<Tolerance or B.distance(C)<Tolerance or B.distance(D)<Tolerance : 
        return True
    else : 
        return False



def SplitLineByDist(Line,Distance) : 
    """
    Fonction permettant de decouper une ligne en repetant une certaine distance
    """
    if Line.length < Distance : 
        return [Line]
    else : 
        CumulDist = Distance
        CutPts = []
        ## recuperation des points de decoupage
        while CumulDist<Line.length : 
            CutPts.append((Line.interpolate(CumulDist),CumulDist,True))
            CumulDist+=Distance
        #recuperation des vrais points
        Coords = list(Line.coords)
        RealPts = [(shapely.geometry.Point(Coords.pop(0)),0,False)]
        CumulDist = 0
        for Coord in Coords : 
            P1 = RealPts[-1][0]
            P2 = shapely.geometry.Point(Coord)
            Ecart = P1.distance(P2)
            CumulDist+=Ecart
            RealPts.append((P2,CumulDist,False))
        #generation des segments
        AllPts = RealPts+CutPts
        AllPts.sort(key=lambda x : x[1])
        Segments = []
        Pts = []
        for Pt,Dist,IsCut in AllPts : 
            if IsCut==False : 
                Pts.append(Pt)
            else : 
                Pts.append(Pt)
                Segments.append(shapely.geometry.LineString([(P.x,P.y) for P in Pts]))
                Pts = [Pt]
        return Segments
                
            
        
        
            
    
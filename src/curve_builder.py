import numpy as np
from OCP.Geom import Geom_BSplineCurve
from OCP.TColgp import TColgp_Array1OfPnt
from OCP.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCP.gp import gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire

def build_periodic_curve(ctrl_pts_xyz, degree=4):
    unique_pts = ctrl_pts_xyz[:-1] 
    n = len(unique_pts)
    
    poles = TColgp_Array1OfPnt(1, n)
    for i, (x, y, z) in enumerate(unique_pts, start=1):
        poles.SetValue(i, gp_Pnt(x, y, z))
        
    n_knots = n + 1
    knots = TColStd_Array1OfReal(1, n_knots)
    for i in range(n_knots):
        knots.SetValue(i + 1, float(i))
        
    mults = TColStd_Array1OfInteger(1, n_knots)
    for i in range(1, n_knots + 1):
        mults.SetValue(i, 1) 
        
    curve = Geom_BSplineCurve(poles, knots, mults, degree, True)
    tmin = curve.FirstParameter()
    tmax = curve.LastParameter()
    
    return curve, tmin, tmax

def create_wire_from_curve(curve, tmin, tmax):
    maker = BRepBuilderAPI_MakeEdge(curve, tmin, tmax)
    if not maker.IsDone():
        raise RuntimeError("Edge creation failed")
    
    wire_maker = BRepBuilderAPI_MakeWire(maker.Edge())
    if not wire_maker.IsDone():
        raise RuntimeError("Wire creation failed")
        
    return wire_maker.Wire()
import numpy as np
from OCP.gp import gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.BRepTools import BRepTools

def build_rect_wire(p, T, N, w, h):
    B = np.cross(T, N)
    c1 = p + (w/2)*N + (h/2)*B
    c2 = p - (w/2)*N + (h/2)*B
    c3 = p - (w/2)*N - (h/2)*B
    c4 = p + (w/2)*N - (h/2)*B
    
    e1 = BRepBuilderAPI_MakeEdge(gp_Pnt(*c1), gp_Pnt(*c2)).Edge()
    e2 = BRepBuilderAPI_MakeEdge(gp_Pnt(*c2), gp_Pnt(*c3)).Edge()
    e3 = BRepBuilderAPI_MakeEdge(gp_Pnt(*c3), gp_Pnt(*c4)).Edge()
    e4 = BRepBuilderAPI_MakeEdge(gp_Pnt(*c4), gp_Pnt(*c1)).Edge()
    return BRepBuilderAPI_MakeWire(e1, e2, e3, e4)

def export_stacked_plates(frames, positions, base_wire, w=0.15, h=0.25, step=1, out_dir="output"):
    # Base Coil
    loft = BRepOffsetAPI_ThruSections(True, True)
    for i in range(0, len(frames), step):
        T, N = frames[i]
        wm = build_rect_wire(positions[i], T, N, w, h)
        loft.AddWire(wm.Wire())
    loft.Build()
    
    # Stacked Plate (Flush)
    loft2 = BRepOffsetAPI_ThruSections(True, True)
    for i in range(0, len(frames), step):
        T, N = frames[i]
        B = np.cross(T, N)
        p_offset = positions[i] + h * B
        wm2 = build_rect_wire(p_offset, T, N, w, h)
        loft2.AddWire(wm2.Wire())
    loft2.Build()
    
    # Export compound
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)
    builder.Add(compound, loft.Shape())
    builder.Add(compound, loft2.Shape())
    builder.Add(compound, base_wire)
    
    BRepTools.Write_s(compound, f"{out_dir}/stacked_plates.brep")
    print(f"Exported to {out_dir}/stacked_plates.brep")
    return loft.Shape(), loft2.Shape()
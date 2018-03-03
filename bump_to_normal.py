#!/usr/bin/env python

from gimpfu import *

def bump_to_normal(img, layer, btype, elevation, depth, invertX, invertY):
    
    pdb.gimp_image_undo_group_start(img)
    
    normal_map = gimp.Layer(img, "normal map", layer.width, layer.height, RGB_IMAGE, 100, NORMAL_MODE)
    img.add_layer(normal_map, 0)
    pdb.gimp_context_set_background((128, 128, 255))
    pdb.gimp_drawable_fill(normal_map, 1)
    decomposed = pdb.plug_in_decompose(img, normal_map, "RGB", 1)[0]
    pdb.plug_in_bump_map(decomposed, decomposed.layers[0], layer, 0, elevation, depth, 0, 0, 0, 0, 1, invertX, btype)
    pdb.plug_in_bump_map(decomposed, decomposed.layers[1], layer, 270, elevation, depth, 0, 0, 0, 0, 1, invertY, btype)
    pdb.plug_in_recompose(decomposed, decomposed.active_drawable)
    gimp.delete(decomposed)
    
    pdb.gimp_image_undo_group_end(img)

register(
    "python_fu_bump_to_normal",
    "Bump to Normal",
    "Makes normal map from bump map",
    "Grigory Ponomar",
    "MIT",
    "2018",
    "<Image>/Filters/Map/Bump to Normal...",
    "RGB, RGB*",
    [
        (PF_RADIO, "btype", "Bump map type", 0, (("Linear", 0), ("Shperical", 1), ("Sinusoidal", 2))),
        (PF_SLIDER, "elevation", "Elevation", 45, (1, 90, 1)),
        (PF_SLIDER, "depth", "Depth", 3, (1, 65, 1)),
        (PF_BOOL, "invertX", "Invert X", 0),
        (PF_BOOL, "invertY", "Invert Y", 0)
    ],
    [],
    bump_to_normal)

main()

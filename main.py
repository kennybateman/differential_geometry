import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import subprocess
from src.curve import *
from src.surface import *

r_data = [ 
    151,
    175,
    200,
    225,
    250,
    275, 
    300,
    325,  
    350,
    375 
]

z_data = [ 
    0, 
    0.5, 
    0.75, 
    0.9, 
    1.2, 
    1.6, 
    1.7, 
    2, 
    2.1, 
    2.2
]





params, _ = curve_fit(
    radial_bowl,
    r_data,
    z_data,
    p0=[10.0, 0.1]
)

self.a, self.b = params



depth = 12
sharpness = 0.0009

bowl = TiltedSaturatingBowl(a=depth,b=sharpness,tilt_x=0,tilt_y=0)
Xb, Yb, Zb = bowl.sample(size=400, resolution=100)
Xb, Yb, Zb = bowl.translate(dz=-2)
Xb, Yb, Zb = bowl.mask_out_inner_radius(radius=150)



surface = SomeSurface()
Xs, Ys, Zs = surface.sample(size=400, resolution=100)


# used for plotting a curve...
# fig = go.Figure(
#     data=[
#         go.Scatter3d(
#             x=X,
#             y=Y,
#             z=Z,
#             mode="lines",
#             name="helix"
#         )
#     ]
# )

# used for plotting a surface...
fig = go.Figure(
    data=[
        go.Surface(
            x=Xb,
            y=Yb,
            z=Zb,
            name="bowl"
        ),
        go.Surface(
            x=Xs,
            y=Ys,
            z=Zs,
            name="bowl"
        )
    ]
)

fig.update_layout(
    title="3D Parametric Curve",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z"
    )
)

# save file and run it
filename = "output.html"
fig.write_html(filename)
subprocess.run(["explorer.exe", filename])
import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import subprocess
from src.curve import *
from src.surface import *
from src.graphing import *
from pathlib import Path


measurements_filename = "data"

# Titled plane...
Path("data/").mkdir(parents=True, exist_ok=True)
raw_measurements2 = try_load_toml('tilted_plane_measurements_45', measurements_filename, 'data/', None)

tilted_surface = FlatSurface.make_from_measured_points(raw_measurements2)
Xts, Yts, Zts = tilted_surface.sample(size=400, resolution=100)

Path("output/").mkdir(parents=True, exist_ok=True)
plot_and_save("output/tilt_fit_x.png", tilted_surface.fit_points[:,[0,2]], tilted_surface.getZofX, None, None)
plot_and_save("output/tilt_fit_y.png", tilted_surface.fit_points[:,[1,2]], tilted_surface.getZofY, None, None)


# Bowl...
raw_measurements = try_load_toml('surface_plane_measurements_radius_45', measurements_filename, 'data/', None)

bowl = Bowl.make_quadratic_from_measured_r_z_points(raw_measurements)

P = np.column_stack((bowl.fit_r_points, bowl.fit_z_points))
print(P)

plot_and_save("output/bowl_fit.png", P, bowl.getZOfRQuatratic, None, None)

Xb, Yb, Zb = bowl.sampleQuadratic(size=400, resolution=100)
Xb, Yb, Zb = bowl.mask_out_inner_radius(radius=150)


# This represents the expected mechanical surface.
normal_surface = FlatSurface(z0=-98.17)
Xns, Yns, Zns = normal_surface.sample(size=400, resolution=100)

fig = go.Figure(
    data=[
        # Normal Flat Surface...
        go.Surface(
            x=Xns,
            y=Yns,
            z=Zns,
            name="normal flat"
        ),

        # Tilted Flat Surface...
        go.Surface(
            x=Xts,
            y=Yts,
            z=Zts,
            name="tilted flat"
        ),

        # #Normal Bowl Surface...
        # go.Surface(
        #     x=Xb,
        #     y=Yb,
        #     z=Zb,
        #     name="normal bowl"
        # ),

        #Tilted Bowl Surface...
        go.Surface(
            x=Xb,
            y=Yb,
            z=np.where(
                (Zb + Zts - Zns) >= -99, 
                Zb + Zts - Zns, 
                np.nan
            ),
            name="tilted bowl"
        ),
    ]
)


# Layout setup
fig.update_layout(
    title="3D Parametric Curve",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z"
    )
)

# save file
filename = "output/output.html"
fig.write_html(filename)

print("kind of done")

# automatically open it in browser...
# subprocess.run(["explorer.exe", filename])

print("done")

































# # FIGURE OUT OFFSETS FOR DOBOT SURFACE...

# # fake data....
# y_data = [
#     0,
#     0,
#     0,
#     0,
#     0,
#     0, 
#     0,
#     0,  
#     0,
#     0    
# ]

# x_data = [ 
#     151,
#     175,
#     200,
#     225,
#     250,
#     275, 
#     300,
#     325,  
#     350,
#     375 
# ]

# z_data = [ 
#     0, 
#     0.5, 
#     0.75, 
#     0.9, 
#     1.2, 
#     1.6, 
#     1.7, 
#     2, 
#     2.1, 
#     2.2
# ]

# # ideally, you'd imagine doing the radial conversion, but all my fake points are ON the x axis (y=0), thus x=r
# r_data = x_data
# points = np.column_stack((r_data, z_data))



# # Model the bowl...
# bowl = Bowl.make_from_measured_r_z_points(points)
# MatplotGraphing.plot_and_save("bowl_fit.png", bowl.fit_points, bowl.getZofR, 'measured', 'fit')



# # klunky, but this establishes an initial set of points...
# Xb, Yb, Zb = bowl.sample(size=400, resolution=100)

# # Manual offsets to those points...
# Xb, Yb, Zb = bowl.translate(dz=-4.5)
# Xb, Yb, Zb = bowl.mask_out_inner_radius(radius=150)



# # fake measurements for figuring out tilted plane...
# measurements = [
#     [100, 0,  1.2],
#     [0, 100, 0.8],
#     [-100, 0, 0.7],
#     [0, -100, 1.1],
# ]

# tilted_surface = FlatSurface.make_from_measured_points(measurements)
# Xts, Yts, Zts = tilted_surface.sample(size=400, resolution=100)

# MatplotGraphing.plot_and_save("tilt_fit_x.png", tilted_surface.fit_points[:,[0,2]], tilted_surface.getZofX, 'measuredx', 'fit')
# MatplotGraphing.plot_and_save("tilt_fit_y.png", tilted_surface.fit_points[:,[1,2]], tilted_surface.getZofY, 'measuredy', 'fit')


# # DATA VIEW SETUP....

# # This represents the expected mechanical surface.
# normal_surface = FlatSurface()
# Xns, Yns, Zns = normal_surface.sample(size=400, resolution=100)

# fig = go.Figure(
#     data=[
#         # Normal Flat Surface...
#         go.Surface(
#             x=Xns,
#             y=Yns,
#             z=Zns,
#             name="normal flat"
#         ),

#         # Tilted Flat Surface...
#         # go.Surface(
#         #     x=Xs,
#         #     y=Ys,
#         #     z=Zs,
#         #     name="tilted flat"
#         # ),

#         # Normal Bowl Surface...
#         # go.Surface(
#         #     x=Xb,
#         #     y=Yb,
#         #     z=Zb,
#         #     name="normal bowl"
#         # ),

#         # Tilted Bowl Surface...
#         go.Surface(
#             x=Xb,
#             y=Yb,
#             z=Zb + Zts,
#             name="tilted bowl"
#         ),
#     ]
# )

# # Layout setup
# fig.update_layout(
#     title="3D Parametric Curve",
#     scene=dict(
#         xaxis_title="X",
#         yaxis_title="Y",
#         zaxis_title="Z"
#     )
# )

# # save file
# filename = "output.html"
# fig.write_html(filename)

# # automatically open it in browser...
# subprocess.run(["explorer.exe", filename])









# # NOTES.....


# # used for plotting a curve...
# # fig = go.Figure(
# #     data=[
# #         go.Scatter3d(
# #             x=X,
# #             y=Y,
# #             z=Z,
# #             mode="lines",
# #             name="helix"
# #         )
# #     ]
# # )

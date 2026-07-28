import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import matplotlib.pyplot as plt

class Bowl:

    # several points (r, z)
    def make_from_measured_r_z_points(points):
        points = np.asarray(points)
        r_points = points[:,0]
        z_points = points[:,1]
        print(points)
        print(r_points)
        print(z_points)
        params, covariance = curve_fit(
            Bowl._zOfR,
            r_points,
            z_points,
            p0=[2.2, 0.01, 0.0], # starting params I guess
        )
        a, b, z0 = params
        bowl = Bowl(a=a,b=b, z0=z0)
        bowl.fit_points = points
        bowl.fit_r_points = r_points # we initialized with these points, so commit them to the object
        bowl.fit_z_points = z_points # we initialized with these points, so commit them to the object
        return bowl


    points = np.array([])
    def __init__(self, a=10, b=0.05, z0=0):
        self.a = a
        self.b = b
        self.z0 = z0


    def get(self, x, y):
        return Bowl._get(self.a, self.b, x, y)
    
    def _get(a, b, x, y):
        r = np.sqrt(x**2 + y**2)
        z = a * (1 - np.exp(-b * r))
        return np.array([x, y, z])

    def getZofR(self, r):
        return Bowl._zOfR(r, self.a, self.b, self.z0)

    def _zOfR(r, a, b, z0):
        return z0 + a * (1 - np.exp(-b * r))


    def _sample(self, size=400, resolution=200):
        u = np.linspace(-size, size, resolution)
        v = np.linspace(-size, size, resolution)

        U, V = np.meshgrid(u, v)

        X, Y, Z = self.get(U, V)

        return np.array([X, Y, Z])
    
    def sample(self, size=1, resolution=1000):
        self.size = size
        self.resolution = resolution
        if self.points.size == 0:
            self.points = self._sample(size, resolution)
        return self.points


    def _translate(self, points, dx=0, dy=0, dz=0):
        X, Y, Z = points
        return np.array([X + dx, Y + dy, Z + dz])

    def translate(self, dx=0, dy=0, dz=0):
        points = self.sample()
        self.points = self._translate(points, dx, dy, dz)
        return self.points


    def _mask_out_inner_radius(self, points, radius):
        X, Y, Z = points
        R = np.sqrt(X**2 + Y**2)

        mask = R >= radius
        X = np.where(mask, X, np.nan)
        Y = np.where(mask, Y, np.nan)
        Z = np.where(mask, Z, np.nan)

        return np.array([X, Y, Z])

    def mask_out_inner_radius(self, radius):
        points = self.sample()
        self.points = self._mask_out_inner_radius(points, 150)
        return self.points

















class FlatSurface:

    # minimum 3 points (x, y , z) taken ideally wherever
    def make_from_measured_points(points):
        points = np.asarray(points)
        tilt_x, tilt_y, z0 = FlatSurface.get_fit_plane_coefficients_from_points(points)
        surface = FlatSurface(tilt_x, tilt_y, z0)

        surface.fit_points = points
        surface.fit_points_x = points[0:,0]
        surface.fit_points_y = points[0:,1]
        surface.fit_points_z = points[0:,2]
        return surface


    def __init__(self, tilt_x=0.0, tilt_y=0.0, z0=0.0):
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.z0 = z0


    def get(self, u, v):
        x = u
        y = v
        z = self.tilt_x * x + self.tilt_y * y + self.z0

        return np.array([x, y, z])


    def getZofX(self, x):
        return self.tilt_x * x + self.z0


    def getZofY(self, y):
        return self.tilt_y * y + self.z0


    def sample(self, size=10, resolution=100):
        u = np.linspace(-size, size, resolution)
        v = np.linspace(-size, size, resolution)

        U, V = np.meshgrid(u, v)

        self.points = self.get(U, V)

        return self.points[0], self.points[1], self.points[2]


    def get_fit_plane_coefficients_from_points(points):
        points = np.asarray(points)
        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]
        A = np.column_stack([
            x,
            y,
            np.ones_like(x)
        ])
        # Solve z = ax + by + c
        coeffs, residuals, rank, singular_values = np.linalg.lstsq(
            A,
            z,
            rcond=None
        )
        a, b, c = coeffs
        return a, b, c
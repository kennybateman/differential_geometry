import numpy as np

class SomeBowl:
    def __init__(self, k=0.05):
        self.k = k

    def get(self, u, v):
        x = u
        y = v
        z = self.k * (u**2 + v**2)

        return np.array([x, y, z])


    def sample(self, size=10, resolution=100):
        u = np.linspace(-size, size, resolution)
        v = np.linspace(-size, size, resolution)

        U, V = np.meshgrid(u, v)

        self.points = self.get(U, V)

        return self.points[0], self.points[1], self.points[2]






class TiltedSaturatingBowl:

    points = np.array([])
    def __init__(self, a=10, b=0.05, tilt_x=0, tilt_y=0):
        self.a = a
        self.b = b
        # self.tilt_x = tilt_x
        # self.tilt_y = tilt_y


    def _get(self, u, v):
        x = u
        y = v

        r = np.sqrt(x**2 + y**2)

        # radial bowl distortion
        z = self.a * (1 - np.exp(-self.b * r))

        # optional tilt component
        #z += self.tilt_x * x + self.tilt_y * y

        return np.array([x, y, z])


    def _sample(self, size=400, resolution=200):
        u = np.linspace(-size, size, resolution)
        v = np.linspace(-size, size, resolution)

        U, V = np.meshgrid(u, v)

        X, Y, Z = self._get(U, V)

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

















class SomeSurface:
    def __init__(self):
        pass

    def get(self, u, v):
        x = u
        y = v
        z = np.zeros_like(x)

        return np.array([x, y, z])


    def sample(self, size=10, resolution=100):
        u = np.linspace(-size, size, resolution)
        v = np.linspace(-size, size, resolution)

        U, V = np.meshgrid(u, v)

        self.points = self.get(U, V)

        return self.points[0], self.points[1], self.points[2]  


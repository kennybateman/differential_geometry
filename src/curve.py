import numpy as np

class SomeHelix:
    def __init__(self, kappa, tau):
        self.kappa = kappa
        self.tau = tau

    def getR3(self, arc_increment=0.01, increments=1000):
        # Tangent vector
        T = np.array([1.,0.,0.])
        # Normal vector
        N = np.array([0.,1.,0.])
        # Binormal vector
        B = np.array([0.,0.,1.])

        # variable point on curve
        p = np.array([0.,0.,0.])

        # differential increment (resolution of curve)
        ds = arc_increment

        # calculate each increment along the arc...
        points = []
        for i in range(increments):
            # find change in Tangent is curvature * Normal
            dT = self.kappa * N
            # find change in Normal vector
            dN = -self.kappa * T + self.tau * B
            # find change in BiNormal vector
            dB = -self.tau * N

            # increment the vectors
            T += dT * ds
            N += dN * ds
            B += dB * ds

            # re-normalize
            T /= np.linalg.norm(T)
            N /= np.linalg.norm(N)
            B /= np.linalg.norm(B)

            # Figure out point
            p += T * ds

            points.append(p.copy())

        self.points = np.array(self.points)
        return self.points[:,0], self.points[:,1], self.points[:,2]


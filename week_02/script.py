from Rhino.Geometry import Vector3d, Point3d, PolylineCurve
import ghpythonlib.components as ghcomp
import random

box = ghcomp.DeconstructBox(boundary)
b_x = box.x[1]
b_y = box.y[1]
b_z = box.z[1]



class Boid:
    def __init__(self):
        self.position = Point3d(random.randint(box.x[0], b_x),random.randint(box.y[0], b_y),random.randint(box.z[0], b_z))
        self.velocity = Vector3d(random.random(),random.random(),random.random())
        self.trail = []
    def move(self):
        self.position = Point3d.Add(self.position, self.velocity)
        self.trail.append(self.position)
        self.trail = self.trail[-5:]
    
    def limit(self):
        if self.position.X >= b_x or self.position.X <= box.x[0]:
            self.velocity.X *= -1
        if self.position.Y >= b_y or self.position.Y <= box.y[0]:
            self.velocity.Y *= -1
        if self.position.Z >= b_z or self.position.Z <= box.z[0]:
            self.velocity.Z *= -1

if run:
    for i in agents:
        i.move()
        i.limit()
else:
    pass

if initialised:
    agents = []
    for i in range(n_boids):
        agents.append(Boid())

points = [i.position for i in agents]
trails = [PolylineCurve(i.trail) for i in agents]
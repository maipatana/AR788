class Boid:
    def __init__(self):
        self.position = Point3d(random.randint(box.x[0], b_x),random.randint(box.y[0], b_y), random.randint(box.z[0], b_z))
        self.velocity = Vector3d(random.random(),random.random(),random.random())
        self.acceleration = Vector3d(0,0,0)
        self.max_speed = 3
        self.max_force = 0.3
        self.trail = []
        
    def move(self):
        self.force(agents)
        self.velocity = Vector3d.Add(self.velocity, self.acceleration)
        Vector3d.Unitize(self.velocity)
        self.velocity *= self.max_speed
        self.position = Point3d.Add(self.position, self.velocity)
        self.acceleration *= 0
        self.trail.append(self.position)
        self.trail = self.trail[-5:]
    
    def force(self, boids):
        coh = self.cohesion(boids, 5, 10)
        sep = self.separation(boids, 1, 10)
        ali = self.alignment(boids, 10, 10)
        thr = self.separation(threat, 20, 10)
        coh *= coh_force
        sep *= sep_force
        ali *= ali_force
        thr *= thr_force
        self.acceleration = coh + sep + ali +thr
    
    def limit(self):
        if self.position.X >= b_x:
            self.position.X = box.x[0]
        elif self.position.X <= box.x[0]:
            self.position.X = b_x
        if self.position.Y >= b_y:
            self.position.Y = box.y[0]
        elif self.position.Y <= box.y[0]:
            self.position.Y = b_y
        if self.position.Z >= b_z:
            self.position.Z = box.z[0]
        elif self.position.Z <= box.z[0]:
            self.position.Z = b_z
    
    def cohesion(self, boids, radius = 5, angle=10):
        neighbors = self.get_neighbors(boids, radius, angle)
        pox = 0
        poy = 0
        poz = 0
        if len(neighbors) > 0:
            n_neighbors = len(neighbors)
            for i in neighbors:
                pox += i.position.X
                poy += i.position.Y
                poz += i.position.Z
            center = Point3d(pox/n_neighbors,poy/n_neighbors,poz/n_neighbors)
            return center - self.position
        else:
            return Vector3d(0,0,0)
            
    def separation(self, boids, radius = 3, angle=10):
        neighbors = self.get_neighbors(boids, radius, angle)
        pox = 0
        poy = 0
        poz = 0
        if len(neighbors) > 0:
            n_neighbors = len(neighbors)
            for i in neighbors:
                pox += i.position.X
                poy += i.position.Y
                poz += i.position.Z
            center = Point3d(pox/n_neighbors,poy/n_neighbors,poz/n_neighbors)
            return (center - self.position) * -1
        else:
            return Vector3d(0,0,0)
    def alignment(self, boids, radius = 5, angle=10):
        neighbors = self.get_neighbors(boids, radius, angle)
        if len(neighbors) > 0:
            n_neighbors = len(neighbors)
            pox = 0
            poy = 0
            poz = 0
            for i in neighbors:
                pox += i.velocity.X
                poy += i.velocity.Y
                poz += i.velocity.Z
            center = Vector3d(pox/n_neighbors,poy/n_neighbors,poz/n_neighbors)
            return center - self.velocity
        else:
            return Vector3d(0,0,0)
        
    def get_neighbors(self, boids, radius, angle):
        neighbors = []
        for boid in boids:
            if boid is self:
                continue
            
            offset = boid.position - self.position
            if offset.Length > radius:
                continue
            neighbors.append(boid)
        return neighbors

class Hunter(Boid):
    def __init__(self):
        Boid.__init__(self)
        
    def move(self):
        self.force(agents, threat)
        self.velocity = Vector3d.Add(self.velocity, self.acceleration)
        Vector3d.Unitize(self.velocity)
        self.velocity *= self.max_speed
        self.position = Point3d.Add(self.position, self.velocity)
        self.acceleration *= 0
        self.trail.append(self.position)
        self.trail = self.trail[-5:]
        
    def force(self, prey, hunter):
        coh = self.cohesion(prey, 20, 10)
        sep = self.separation(hunter, 5, 10)
        ali = self.alignment(hunter, 5, 10)
        coh *= 1
        sep *= 2
        ali *= 0.5
        self.acceleration = coh + sep + ali

def run_boids(agents):
    agents.move()
    agents.limit()
    points.append(Cone(Plane(agents.position, -1*(agents.velocity)), 2, 0.5))

def run_hunter(threat):
    threat.move()
    threat.limit()
    threats.append(Cone(Plane(threat.position, -1*(threat.velocity)), 6, 2))
    
if run:
    points = []
    threats = []
    parallel.run(run_hunter, threat, True)
    parallel.run(run_boids, agents, True)
else:
    pass

if initialised:
    from Rhino.Geometry import Vector3d, Point3d, PolylineCurve, Cone, Plane, Sphere
    import ghpythonlib.components as ghcomp
    from ghpythonlib import parallel
    import random

    box = ghcomp.DeconstructBox(boundary)
    b_x = box.x[1]
    b_y = box.y[1]
    b_z = box.z[1]
    agents = []
    threat = []
    for i in range(n_boids):
        agents.append(Boid())
    for i in range(2):
        threat.append(Hunter())
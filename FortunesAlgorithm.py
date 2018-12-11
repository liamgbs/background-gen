from math import sqrt
from heapq import heappop, heappush
from helpers import randomXY
from random import randint
from shapely.ops import polygonize

class Site:
  def __init__(self, xy=(None, None)):
    self.x = xy[0]
    self.y = xy[1]

  def __lt__(self, other):
      return self.x, other.x

  def __repr__(self):
      return str((self.x, self.y))


class Event:
  def __init__(self, x, p, a):
    self.x = x
    self.p = p
    self.a = a
    self.valid = True

  def __lt__(self, other):
      return self.x < other.x


class Parabola:
  def __init__(self, p, above=None, below=None):
    self.p = p
    self.intersect_above = above
    self.intersect_below = below
    self.e = None
    self.s0 = None
    self.s1 = None


class Line:
  def __init__(self, start=None, end=None):
    self.start = start
    self.end = end

  def __repr__(self):
    return str((self.start.x, self.start.y, self.end.x, self.end.y))


class Fortunes:
  def __init__(self, imgx, imgy, number_sites=1000):
    self.imgx = imgx
    self.imgy = imgy
    self.settled_lines = []
    self.parab = None
    self.sites = []
    self.event = []

    [heappush(self.sites, (s.x, s)) for s in
        set([Site(randomXY(imgx, imgy)) for i in range(number_sites)])]

    self.scan()

  def scan(self):
    while self.sites:
      if self.event and (self.event[0][1].x <= self.sites[0][1].x):
        self.process_event()
      else:
        site = heappop(self.sites)[1]
        self.add_parab(site)

    while self.event:
      self.process_event()

    self.settle_scanline()
    self.bound_lines()
    #self.complete_border_polygons()

  def complete_border_polygons(self):
      def is_border(ln):
          if 0 in [ln.start.x]:
              return True
      borderlines = [line for line in self.settled_lines if is_border(line)]
      borderlines.sort(key=lambda ln : ln.start.y)
      for i in range(len(borderlines) - 1):
          p1, p2 = borderlines[i].start, borderlines[i+1].start
          self.settled_lines.append(Line(p1, p2))

  def bound_lines(self):
    for ln in self.settled_lines:
        if (ln.start.x <= 0):
          ln.start.x = 0
        if (ln.start.x > self.imgx):
          ln.start.x = self.imgx
        if (ln.start.y <= 0):
          ln.start.y = 0
        if (ln.start.y > self.imgy):
          ln.start.y = self.imgy
        if (ln.end.x <= 0):
          ln.end.x = 0
        if (ln.end.x > self.imgx):
          ln.end.x = self.imgx
        if (ln.end.y <= 0):
          ln.end.y = 0
        if (ln.end.y > self.imgy):
          ln.end.y = self.imgy

  def process_event(self):
    # get next event from circle pq
    e = heappop(self.event)
    event = e[1]
    if event.valid:
      # start new edge
      s = Line()
      s.start = event.p
      self.settled_lines.append(s)

      a = event.a
      if a.intersect_above is not None:
        a.intersect_above.intersect_below = a.intersect_below
        a.intersect_above.s1 = s
      if a.intersect_below is not None:
        a.intersect_below.intersect_above = a.intersect_above
        a.intersect_below.s0 = s
      if a.s0 is not None:
          a.s0.end = event.p
      if a.s1 is not None:
          a.s1.end = event.p
      if a.intersect_above is not None:
          self.check_for_event(a.intersect_above)
      if a.intersect_below is not None:
          self.check_for_event(a.intersect_below)

  def parab_intersect(self, parab1, parab2):
    if not parab2 or parab2.p.x == parab1.x:
        return False

    if parab2.intersect_above is not None:
      a = self.do_intersection(parab2.intersect_above.p,
                            parab2.p,
                            abs(parab1.x)).y

    if parab2.intersect_below is not None:
      b = self.do_intersection(parab2.p,
                            parab2.intersect_below.p,
                            abs(parab1.x)).y

    if (((parab2.intersect_above is None)
                            or (a <= parab1.y))
                            and ((parab2.intersect_below is None)
                            or (parab1.y <= b))):
      py = parab1.y
      px = (pow(parab2.p.x, 2)
            + pow(parab2.p.y-py, 2)
            - pow(parab1.x, 2)) / (2*parab2.p.x - 2*parab1.x)

      intersect = Site((px, py))
      return intersect

  def add_parab(self, site):
    if self.parab is None:
      self.parab = Parabola(site)
    else:
      i = self.parab
      while i is not None:
        inter = self.parab_intersect(site, i)
        if inter:
          if (i.intersect_below is not None) and not self.parab_intersect(site, i.intersect_below):
            i.intersect_below.intersect_above = Parabola(i.p, i, i.intersect_below)
            i.intersect_below = i.intersect_below.intersect_above
          else:
            i.intersect_below = Parabola(i.p, i)

          i.intersect_below.s1 = i.s1

          i.intersect_below.intersect_above = Parabola(site, i, i.intersect_below)
          i.intersect_below = i.intersect_below.intersect_above

          i = i.intersect_below  # now i points to the new arc

          # add new half-edges connected to i's endpoints
          seg = Line()
          seg2 = Line()
          seg.start = inter
          seg2.start = inter
          self.settled_lines.append(seg)
          self.settled_lines.append(seg2)
          i.intersect_above.s1 = seg
          i.s0 = seg
          i.intersect_below.s0 = seg2
          i.s1 = seg2


          # check for new circle events around the new arc
          for int_point in [i, i.intersect_above, i.intersect_below]:
              self.check_for_event(int_point)
          return

        i = i.intersect_below

      # if p never intersects an arc, append it to the list
      i = self.parab
      while i.intersect_below is not None:
        i = i.intersect_below
      i.intersect_below = Parabola(site, i)

      y = (i.intersect_below.p.y + i.p.y) / 2.0;
      start = Site((0, y))

      seg = Line()
      seg.start = start
      i.s1 = i.intersect_below.s0 = seg
      self.settled_lines.append(seg)

  def check_for_event(self, i):
    if None in [i.intersect_above, i.intersect_below]:
        return

    if (i.e is not None):
      i.e.valid = False
    i.e = None

    x, o = self.circle_equation(i.intersect_above.p, i.p, i.intersect_below.p)
    if x > 0:
      i.e = Event(x, o, i)
      heappush(self.event, (i.e.x, i.e))

  def circle_equation(self, a, b, c):
    def circle_radius(x, y, h, k):
        return sqrt(pow(x-h, 2) + pow(y-k, 2))

    A, B, C, D = b.x - a.x, b.y - a.y, c.x - a.x, c.y - a.y

    if (A*D) - (B*C) > 0:
        return 0, None

    E = A*(a.x + b.x) + B*(a.y + b.y)
    F = C*(a.x + c.x) + D*(a.y + c.y)
    G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

    if (G == 0):
        return 0, None

    circle_center = Site()
    circle_center.x = (D*E - B*F) / G
    circle_center.y = (A*F - C*E) / G

    circle_r = circle_center.x + circle_radius(a.x,
                                               a.y,
                                               circle_center.x,
                                               circle_center.y)

    return circle_r, circle_center

  def do_intersection(self, p0, p1, l=-1):
    def quadratic(a, b, c):
        return (-1*(b)-sqrt(b*b - 4*a*c)) / (2*a)

    p = p0
    if (p0.x == p1.x):
      py = (p0.y + p1.y) / 2
    elif (p1.x == l):
      py = p1.y
    elif (p0.x == l):
      py = p0.y
      p = p1
    else:
      z0, z1 = (p0.x - l), (p1.x - l)
      a = 1/z0 - 1/z1;
      b = -2 * (p0.y/z0 - p1.y/z1)
      c = (pow(p0.y, 2) + pow(p0.x, 2) - pow(l, 2)) / z0 - 1 * (pow(p1.y, 2) + pow(p1.x, 2) - pow(l, 2)) / z1

      py = quadratic(a, b, c)

    px = (pow(p.x, 2) + pow(p.y-py, 2) - pow(l, 2)) / (2 * p.x-2 * l)
    res = Site((px, py))
    return res

  def settle_scanline(self):
    i = self.parab
    while i.intersect_below is not None:
      if i.s1 is not None:
        p = self.do_intersection(i.p, i.intersect_below.p)
        i.s1.end = p
      i = i.intersect_below

  def get_polygons(self):
    def format_line(ln):
        return ((ln.start.x, ln.start.y), (ln.end.x, ln.end.y))
    poly_lines = [format_line(ln) for ln in self.settled_lines]
    return polygonize(poly_lines)

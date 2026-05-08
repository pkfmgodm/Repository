from math import dist, pi, sqrt
ACCURACY = 1e-9


class Rectangle(Point):
    
    def __init__(self, point1: Point, point2: Point):
        if not isinstance(point1, Point) or not isinstance(point2, Point):
            raise ValueError("point1 та point2 мають бути точками")
        
        
        if point1.x == point2.x or point1.y == point2.y:
            raise ValueError("Точки не можуть лежати на  лінії") 
            
        self.point1 = point1
        self.point2 = point2

    def __repr__(self):
        return f"Прямокутник ({self.point1}, {self.point2})" [1]

    def _sides(self):
        width = abs(self.point1.x - self.point2.x)
        height = abs(self.point1.y - self.point2.y)
        return width, height

    def p(self):
       
        w, h = self._sides()
        return 2 * (w + h) [2]

    def s(self):
        w, h = self._sides()
        return w * h [2]

    def __eq__(self, other: 'Rectangle'):
        if not isinstance(other, self.__class__):
            return False
        
        self_coords_x = {self.point1.x, self.point2.x}
        self_coords_y = {self.point1.y, self.point2.y}
        other_coords_x = {other.point1.x, other.point2.x}
        other_coords_y = {other.point1.y, other.point2.y}
        return self_coords_x == other_coords_x and self_coords_y == other_coords_y [3, 4]

    def __contains__(self, point: Point):
        if not isinstance(point, Point):
            raise ValueError("Має бути точкою")
        min_x, max_x = min(self.point1.x, self.point2.x), max(self.point1.x, self.point2.x)
        min_y, max_y = min(self.point1.y, self.point2.y), max(self.point1.y, self.point2.y)
        return min_x <= point.x <= max_x and min_y <= point.y <= max_y [3]


class Circumference(Point):
    

    def __init__(self, center: Point, radius: float):
        if not isinstance(center, Point):
            raise ValueError("center має бути точкою")
        if radius <= 0:
            raise ValueError("Радіус має бути більшим за нуль") 
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Коло (центр: {self.center}, радіус: {self.radius})" [6, 8]

    def p(self):
        # Довжина кола: 2 * pi * r
        return 2 * pi * self.radius [8, 9]

    def s(self):
        
        return 0.0

    def __eq__(self, other: 'Circumference'):
        if not isinstance(other, self.__class__):
            return False
        return self.center == other.center and abs(self.radius - other.radius) < ACCURACY [6, 7]

    def __contains__(self, point: Point):
        if not isinstance(point, Point):
            raise ValueError("Має бути точкою")
       
        return abs(dist((self.center.x, self.center.y), (point.x, point.y)) - self.radius) < ACCURACY [10]

class Circle(Circumference):
   
    def s(self):
       
        return pi * (self.radius ** 2) [11, 12]

    def __contains__(self, point: Point):
        if not isinstance(point, Point):
            raise ValueError("Має бути точкою")
       
        return dist((self.center.x, self.center.y), (point.x, point.y)) <= self.radius + ACCURACY [11, 13]
  
  
class Polyline(Point):
    '''
    Клас "ламана лінія", що складається з послідовності точок
    '''
    def __init__(self, points: list[Point]):
        
        if len(points) < 3:
            raise ValueError("Ламана лінія має складатися щонайменше з двох точок")
        
       
        for i in range(len(points) - 1):
            if points[i] == points[i+1]:
                raise ValueError("Сусідні точки не мають збігатися")
        
        self.points = points

    def __repr__(self):
        if len(self.points) > 5:
            return f"Polyline([{self.points}, {self.points[5]}, ..., {self.points[-1]}])"
        return f"Polyline({self.points})"

    def p(self):
        total_length = 0.0
        for i in range(len(self.points) - 1):
            total_length += Segment(self.points[i], self.points[i+1]).length()
        return total_length

    def s(self):
        
        return 0.0

    def __contains__(self, point: Point):
        if not isinstance(point, Point):
            raise ValueError("Має бути точкою")
        
        for i in range(len(self.points) - 1):
            if point in Segment(self.points[i], self.points[i+1]):
                return True
        return False

    def __eq__(self, other: 'Polyline'):
        if not isinstance(other, self.__class__):
            return False
        return self.points == other.points or self.points == other.points[::-1]

def egcd(a, b):
	if a == 0:
		return b, 0, 1
	else:
		g, x, y = egcd(b % a, a)
		return g, y - (b // a) * x, x


def mulinv(b, n):
	g, x, _ = egcd(b, n)
	if g == 1:
		return x % n


class ElCur:

	def __init__(self, _p, _A, _B, _G, _O):
		if not ((4 * _A ** 3 + 27 * _B ** 2) % _p):
			print("низя")
			return

		self.p = _p
		self.A = _A
		self.B = _B
		self.O = _O
		self.G = _G
		# self.points = self.get_all_points()

	def add_points(self, _x1, _x2, _y1, _y2):
		if (_x1 == _x2) and (_y1 == (-_y2) % self.p):
			return _x1, _y2
		elif (_x1 == _x2) and (_y1 == _y2):
			lmbd = ((3 * _x1 ** 2 + self.A) * mulinv((2 * _y1), self.p)) % self.p
		else:
			x1 = (-_x1) % self.p
			lmbd = ((_y2 - _y1) * mulinv((_x2 + x1), self.p)) % self.p

		x3 = (lmbd * lmbd - _x1 - _x2) % self.p
		y3 = (lmbd * (_x1 - x3) - _y1) % self.p
		return x3, y3

	def get_all_points(self):
		flag = True
		points = [self.G]
		x1 = x2 = self.G[0]
		y1 = y2 = self.G[1]

		while flag:
			new_point = self.add_points(x1, x2, y1, y2)

			if new_point in points:
				flag = False
				points.append(self.O)
				print(self.O)
			else:
				points.append(new_point)
				x2 = new_point[0]
				y2 = new_point[1]
				print(new_point)

		return points

	def get_point(self, _n):
		return self.mul_point(_n, self.G)

	def mul_point(self, _n, _point):
		x1 = x2 = _point[0]
		y1 = y2 = _point[1]
		new_point = (0, 0)

		for i in range(1, _n):
			new_point = self.add_points(x1, x2, y1, y2)
			x2 = new_point[0]
			y2 = new_point[1]

		return new_point

	def point_belongs(self, _x, _y):
		left = (_y ** 2) % self.p
		right = (_x ** 3 + self.A * _x + self.B) % self.p

		if left == right:
			return True
		else:
			return False


el = ElCur(31991, 31988, 1000, (0, 5585), (0, 0))
# print(el.get_point(5103))
# print(el.get_point(523))
# print(el.mul_point(523, (12507, 2027)))
# el.print_points()
# print(el.get_point(0, 0, 5585, 5585))
# print(el.point_belongs(8.201019196290101, -5608.485604480835))
# print(el.point_belongs(0, 26406))
# print(el.point_belongs(0, 0))
# print(el.add_points(8, 0, 19435, 0))
# print((0, 0) in el.points)
# for p in el.points:
# 	if el.point_belongs(p[0], p[1]):
# 		print(p)

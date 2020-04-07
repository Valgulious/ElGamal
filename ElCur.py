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
		assert ((4 * _A ** 3 + 27 * _B ** 2) % _p) != 0, "Невозможно создать эллиптическую кривую с заданными " \
														 "параметрами A и B"

		self.p = _p
		self.A = _A
		self.B = _B
		self.O = _O
		assert self.point_belongs(_G), "Выбранная точка G не принадлежит заданной эллиптической кривой"
		self.G = _G
		self.points = self.get_all_points()

	def add_points(self, _point1, _point2):
		x1 = _point1[0]
		x2 = _point2[0]
		y1 = _point1[1]
		y2 = _point2[1]
		if (x1 == x2) and (y1 == (-y2) % self.p):
			return _point1
		elif (x1 == x2) and (y1 == y2):
			lmbd = ((3 * x1 ** 2 + self.A) * mulinv((2 * y1), self.p)) % self.p
		else:
			x = (-x1) % self.p
			lmbd = ((y2 - y1) * mulinv((x2 + x), self.p)) % self.p

		x3 = (lmbd * lmbd - x1 - x2) % self.p
		y3 = (lmbd * (x1 - x3) - y1) % self.p
		return x3, y3

	def get_all_points(self):
		flag = True
		points = [self.G]
		new_point = self.G
		count = 1

		while flag:
			new_point = self.add_points(self.G, new_point)

			if new_point in points:
				flag = False
				points.append(self.O)
				print(self.O)
			else:
				points.append(new_point)
				print(new_point)

			count += 1

		print("Количство точек = " + str(count))

		return points

	def get_point(self, _n):
		return self.mul_point(_n, self.G)

	def mul_point(self, _n, _point):
		new_point = _point

		for i in range(1, _n):
			new_point = self.add_points(_point, new_point)

		return new_point

	def point_belongs(self, _point):
		left = (_point[1] ** 2) % self.p
		right = (_point[0] ** 3 + self.A * _point[0] + self.B) % self.p

		return left == right

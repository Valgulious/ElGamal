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

	def __init__(self, _p, _a1, _a2, _a3, _a4, _a6, _G, _O):
		assert ((4 * _a4 ** 3 + 27 * _a6 ** 2) % _p) != 0, "Выберете другие параметры a4 и a6," \
														   "так чтобы (4*a4^3 + 27*a6^2) mod p"

		self.p = _p
		self.a1 = _a1
		self.a2 = _a2
		self.a3 = _a3
		self.a4 = _a4
		self.a6 = _a6
		self.O = _O
		assert self.point_belongs(_G), "Выбранная точка G не принадлежит заданной эллиптической кривой"
		self.G = _G
		# self.points = self.get_all_points()

	# Сложение точек
	def add_points(self, _point1, _point2):
		x1 = _point1[0]
		x2 = _point2[0]
		y1 = _point1[1]
		y2 = _point2[1]
		p = self.p
		a1 = self.a1
		a2 = self.a2
		a3 = self.a3
		a4 = self.a4
		a6 = self.a6
		if (x1 == x2) and (y1 == (-y2) % p):
			return _point1
		elif (x1 == x2) and (y1 == y2):
			lmbd = ((3*x1**2 + 2*a2*x1 + a4 - a1*y1) * mulinv((2 *y1 + a1*x1 + a3), p)) % p
			v = ((-x1**3 + a4*x1 + 2*a6 - a3*y1) * mulinv((2*y1 + a1*x1 + a3), p)) % p
		else:
			x = (-x1) % self.p
			lmbd = ((y2 - y1) * mulinv((x2 + x), p)) % p
			v = ((y1 * x2 - y2 * x1) * mulinv((x2 + x), p)) % p

		x3 = (lmbd**2 + a1*lmbd - a2 - x1 - x2) % p
		y3 = (-(lmbd + a1)*x3 - v - a3) % p
		return x3, y3

	# Генерация всех точек кривой
	def get_all_points(self):
		flag = True
		points = [self.G]
		new_point = self.G

		while flag:
			new_point = self.add_points(self.G, new_point)

			if new_point in points:
				flag = False
				points.append(self.O)
			else:
				points.append(new_point)

		return points

	# Получение _n-й точки кривой
	def get_point(self, _n):
		return self.mul_point(_n, self.G)

	# Умножение точки _point саму на себя _n раз
	def mul_point(self, _n, _point):
		new_point = _point

		for i in range(1, _n):
			new_point = self.add_points(_point, new_point)

		return new_point

	# Проверка принадлежит ли точка _point кривой
	def point_belongs(self, _point):
		x = _point[0]
		y = _point[1]
		left = (y ** 2 + self.a1 * x * y + self.a3 * y) % self.p
		right = (x ** 3 + self.a2 * x ** 2 + self.a4 * x + self.a6) % self.p

		return left == right

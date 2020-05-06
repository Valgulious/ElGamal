from random import randint
# import ElCur


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


class Eliptic:

	def __init__(self, p, a1, a2, a3, a4, a6, g, o):
		assert ((4 * a4 ** 3 + 27 * a6 ** 2) % p) != 0, "(4*a4^3 + 27*a6^2) mod p должно равняться 0"
		self.p = p
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3
		self.a4 = a4
		self.a6 = a6
		self.o = o
		assert self.point_belongs(g), "Точка g не принадлежит эллиптической кривой"
		self.g = g

	def add_points(self, p1, p2):
		x1 = p1[0]
		x2 = p2[0]
		y1 = p1[1]
		y2 = p2[1]
		if (x1 == x2) and (y1 == (-y2) % self.p):
			return p1
		elif (x1 == x2) and (y1 == y2):
			la = ((3*x1**2+2*self.a2*x1+self.a4-self.a1*y1)*mulinv((2*y1+self.a1*x1+self.a3), self.p)) % self.p
			nu = ((-x1**3+a4*x1+2*a6-a3*y1)*mulinv((2*y1+a1*x1+a3), p)) % p
		else:
			x = (-x1) % self.p
			la = ((y2-y1)*mulinv((x2+x), self.p)) % self.p
			nu = ((y1*x2-y2*x1)*mulinv((x2+x), self.p)) % self.p
		x3 = (la**2+self.a1*la-self.a2-x1-x2) % self.p
		y3 = (-(la+self.a1)*x3-nu-self.a3) % self.p
		return x3, y3

	def get_all_points(self):
		f = True
		new_p = self.g
		points = [new_p]
		while f:
			new_p = self.add_points(self.g, new_p)
			if new_p in points:
				f = False
				points.append(self.o)
			else:
				points.append(p)
		return points

	def get_point(self, n):
		return self.mul_point(n, self.g)

	def mul_point(self, n, p):
		new_p = p
		for i in range(1, n):
			new_p = self.add_points(p, new_p)
		return new_p

	def point_belongs(self, p):
		return (p[1]**2+self.a1*p[0]*p[1]+self.a3*p[1]) % self.p == (p[0]**3+self.a2*p[0]**2+self.a4*p[0]+self.a6) % self.p


class ElGamal:
	def __init__(self, eliptic, q):
		self.eliptic = eliptic
		self.q = q

	def encrypt(self, message, public):
		# k = randint(1, self.q - 1)
		k = 523
		r = self.eliptic.get_point(k)
		p = self.eliptic.mul_point(k, public)
		encrypt_message = (message*p[0]) % self.eliptic.p
		return r, encrypt_message

	def decrypt(self, encrypt, secret):
		q = self.eliptic.mul_point(secret, encrypt[0])
		message = (encrypt[1]*mulinv(q[0], self.eliptic.p)) % self.eliptic.p
		return message


p = 31991
a1 = 0
a2 = 0
a3 = 0
a4 = 31988
a6 = 1000
g = (0, 5585)
o = (0, 0)

eliptic = Eliptic(p, a1, a2, a3, a4, a6, g, o)
points = eliptic.get_all_points()
q = len(points)
for point in points:
	print(point)
print("Количество точек = " + str(q))
elgamal = ElGamal(eliptic, q)
c = 5103
D = (12507, 2027)
print(elgamal.encrypt(10000, D))
print(elgamal.decrypt(elgamal.encrypt(10000, D), c))

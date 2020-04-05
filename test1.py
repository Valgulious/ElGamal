def egcd(a, b):
	if a == 0:
		return b, 0, 1
	else:
		g, x, y = egcd(b % a, a)
		return g, y - (b // a) * x, x


# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
	g, x, _ = egcd(b, n)
	print(g, x, _)
	if g == 1:
		return x % n

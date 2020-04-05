from random import random
# from ElCur import ElCur
import ElCur


class User:
	def __init__(self, _elcur):
		self.elcur = _elcur
		self._secret_key = 5103
		self.public_key = self.elcur.get_point(self._secret_key)

	def encrypt(self, _message, _public_key):
		k = 523
		r = self.elcur.get_point(k)
		p = self.elcur.mul_point(k, _public_key)
		encrypt_message = (_message * p[0]) % self.elcur.p
		return r, encrypt_message

	def decrypt(self, _r, _encrypt_message):
		q = self.elcur.mul_point(self._secret_key, _r)
		message = (_encrypt_message * ElCur.mulinv(q[0], self.elcur.p)) % self.elcur.p
		return message


el = ElCur.ElCur(31991, 31988, 1000, (0, 5585), (0, 0))
user = User(el)
print(user.encrypt(10000, (12507, 2027)))
print(user.decrypt((9767, 11500), 11685))

from random import randint
import ElCur


class User:
	def __init__(self, _id, _name, _elcur):
		self.id = _id
		self.name = _name
		self.elcur = _elcur
		self._secret_key = randint(1, len(self.elcur.points) - 1)
		self.public_key = self.elcur.get_point(self._secret_key)

	def encrypt(self, _message, _public_key):
		k = randint(1, len(self.elcur.points) - 1)
		R = self.elcur.get_point(k)
		P = self.elcur.mul_point(k, _public_key)
		encrypt_message = (_message * P[0]) % self.elcur.p
		return R, encrypt_message

	def decrypt(self, _encrypt_message):
		Q = self.elcur.mul_point(self._secret_key, _encrypt_message[0])
		message = (_encrypt_message[1] * ElCur.mulinv(Q[0], self.elcur.p)) % self.elcur.p
		return message


class ElGamal:
	def __init__(self, _p, _A, _B, _G, _O):
		self.elcur = ElCur.ElCur(_p, _A, _B, _G, _O)
		self.users = []

	def add_user(self, _id, _name):
		for user in self.users:
			if _id == user.id:
				print("Пользователь с id: " + str(_id) + " уже существует!")
				return False
		self.users.append(User(_id, _name, self.elcur))
		print("Пользователь с id: " + str(_id) + " и именем: " + str(_name) + " создан!")
		return True

	def	send_massage(self, _message, _user_from, _user_to):
		print("Сообщение, которое надо передать: " + str(_message))
		encrypt_message = _user_from.encrypt(_message, _user_to.public_key)
		print("Зашифрованное сообщение: " + str(encrypt_message))
		print("Пользователь: " + _user_from.name + " посылает сообщение пользователю: " + _user_to.name)
		decrypt_message = _user_to.decrypt(encrypt_message)
		print("Расшифрованное сообщение: " + str(decrypt_message))


p = 31991
A = 31988
B = 1000
G = (0, 5585)
O = (0, 0)
elgamal = ElGamal(p, A, B, G, O)
elgamal.add_user(0, "Alice")
elgamal.add_user(1, "Bob")
elgamal.send_massage(10000, elgamal.users[0], elgamal.users[1])

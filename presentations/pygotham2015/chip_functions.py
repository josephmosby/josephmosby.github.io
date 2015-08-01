def single_bit_or(a, b):
	'''
	a: single bit, 1 or 0
	b: single bit, 1 or 0
	'''

	if a == 1 or b == 1:
		return 1
	else:
		return 0

def single_bit_not(a):
	'''
	a: single bit, 1 or 0
	'''

	if a == 1:
		return 0
	elif a == 0:
		return 1

def single_bit_and(a, b):
	'''
	a: single bit, 1 or 0
	b: single bit, 1 or 0
	'''

	if a == 1 and b == 1:
		return 1
	else:
		return 0

def 16_bit_multiplexer(a16, b16, sel):
	'''
	a16: binary number, formatted as list [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1]
	b16: binary number, formatted as list [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1]

	If selector bit (sel) == 0, return a16
	Else return b16
	'''

	if sel == 0:
		return a16
	else:
		return b16


	
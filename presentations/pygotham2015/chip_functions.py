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

def single_bit_mux(a, b, sel):

	if sel == 0:
		return a
	else:
		return b

def single_bit_xor(a, b):

	if a == b:
		return 0
	else:
		return 1

def sixteen_bit_not(a16):
	'''
	a16: binary number, formatted as list [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1]

	Flip bits of all inputs
	'''
	return [0 if bit == 1 else 1 for bit in a16]

def sixteen_bit_and(a16, b16):
	'''
	a16: binary number, formatted as list [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1]
	b16: binary number, formatted as list [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1]

	Binary AND bits of all inputs
	'''
	out = []
	for i, b in enumerate(a16):
		out.append(single_bit_and(a16[i], b16[i]))

	return out

def sixteen_bit_mux(a16, b16, sel):
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

def half_adder(a, b):
	'''
	Outputs:
	sum: right bit of a + b
	carry: left bit of a + b
	'''
	sum = single_bit_xor(a, b)
	carry = single_bit_and(a, b)

	return sum, carry

def full_adder(a, b, right_carry):
	'''
	Outputs:
	sum: right bit of a + b + right_carry
	carry: left bit of a + b + right_carry
	'''
	sum = single_bit_xor(a, b)
	carry = single_bit_and(a, b)

	return sum, carry

	right_sum, carry1 = half_adder(a, b)
	sum, carry2 = half_adder(right_sum, right_carry)
	carry = single_bit_or(carry1, carry2)
	
	return sum, carry

def sixteen_bit_adder(a16, b16):
	'''
	Outputs:
	sum: a sixteen-bit-sum of two numbers

	Discard the most significant carry bit. 
	'''
	sum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	sum[0], carry0 = half_adder(a16[0], b16[0])
	sum[1], carry1 = full_adder(a16[1], b16[1], carry0)
	sum[2], carry2 = full_adder(a16[2], b16[2], carry1)
	sum[3], carry3 = full_adder(a16[3], b16[3], carry2)
	sum[4], carry4 = full_adder(a16[4], b16[4], carry3)
	sum[5], carry5 = full_adder(a16[5], b16[5], carry4)
	sum[6], carry6 = full_adder(a16[6], b16[6], carry5)
	sum[7], carry7 = full_adder(a16[7], b16[7], carry6)
	sum[8], carry8 = full_adder(a16[8], b16[8], carry7)
	sum[9], carry9 = full_adder(a16[9], b16[9], carry8)
	sum[10], carry10 = full_adder(a16[10], b16[10], carry9)
	sum[11], carry11 = full_adder(a16[11], b16[11], carry10)
	sum[12], carry12 = full_adder(a16[12], b16[12], carry11)
	sum[13], carry13 = full_adder(a16[13], b16[13], carry12)
	sum[14], carry14 = full_adder(a16[14], b16[14], carry13)
	sum[15], carry15 = full_adder(a16[15], b16[15], carry14)

	return sum

def alu(x16, y16, zx, nx, zy, ny, f, no):
	'''
	Inputs:

	a16, b16,  // 16-bit inputs        
	zx, // zero the x input?
	nx, // negate the x input?
	zy, // zero the y input?
	ny, // negate the y input?
	f,  // compute out = x + y (if 1) or x & y (if 0)
	no; // negate the out output?
	'''
	all_zeroes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

	### determine the X to use

	# zero the x if zx is set, else output incoming x
	zerox = sixteen_bit_mux(a16=x16, b16=all_zeroes, sel=zx)

	# not the x
	notx = sixteen_bit_not(x16)

	usex = sixteen_bit_mux(a16=zerox, b16=notx, sel=nx)

	### determine the Y to use

	# zero the y if zy is set, else output incoming y
	zeroy = sixteen_bit_mux(a16=y16, b16=all_zeroes, sel=zy)

	# not the y
	noty = sixteen_bit_not(y16)

	usey = sixteen_bit_mux(a16=zeroy, b16=noty, sel=ny)

	### compute the Fs

	addxy = sixteen_bit_adder(a16=usex, b16=usey)
	andxy = sixteen_bit_and(a16=usex, b16=usey)

	posout = sixteen_bit_mux(a16=addxy, b16=addxy, sel=f)
	negout = sixteen_bit_not(posout)

	out16 = sixteen_bit_mux(a16=posout, b16=negout, sel=no)
	ng = out16[15]

	### determine if output is zero
	### out16 == all_zeroes
	c1 = single_bit_or(out16[0], out16[1])
	c2 = single_bit_or(out16[2], out16[3])
	c3 = single_bit_or(out16[4], out16[5])
	c4 = single_bit_or(out16[6], out16[7])
	c5 = single_bit_or(out16[8], out16[9])
	c6 = single_bit_or(out16[10], out16[11])
	c7 = single_bit_or(out16[12], out16[13])
	c8 = single_bit_or(out16[14], out16[15])

	c9 = single_bit_or(c1, c2)
	c10 = single_bit_or(c3, c4)
	c11 = single_bit_or(c5, c6)
	c12 = single_bit_or(c7, c8)
	c13 = single_bit_or(c9, c10)
	c14 = single_bit_or(c11, c12)
	check = single_bit_or(c13, c14)

	zr = single_bit_not(check)

	return out16, zr, ng

a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
a.reverse()
b.reverse() 

test_add = sixteen_bit_adder(a, b)
test_add.reverse()
print(test_add)

out, zr, ng = alu(a, b, 0, 0, 0, 0, 1, 0)
out.reverse()
print(out)
print(zr, ng)
print(test_add==out)
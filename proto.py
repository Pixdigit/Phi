# -*- coding: utf-8 -*-

reserves = {0: "const"}

variables = {"null": 0}

global code
global pointer
code = ""
pointer = 0


def get_free(D_consecutive_ram):
	D_free = 0
	for pos in reserves:
		if reserves[pos] is None:
			D_free += 1
		else:
			D_free = 0
		if D_free == D_consecutive_ram:
			return pos
	#Have not found enough space
	first_new = max(reserves.keys()) + 1
	for i in range(D_consecutive_ram):
		reserves[first_new + i] = None
	return first_new


def sub_null():
	global code
	code += "[-]"


def goto(addr):
	global code
	global pointer
	if addr < pointer:
		while pointer != addr:
			pointer -= 1
			code += "<"
	if addr > pointer:
		while pointer != addr:
			pointer += 1
			code += ">"


def add(amount):
	global code
	code += "+" * amount


def sub(amount):
	global code
	code += "-" * amount


def output():
	global code
	code += "."


def read_input():
	global code
	code += ","

inp = 1
char = 2

goto(inp)
read_input()
goto(char)
add(47)

for i in range(10):
	goto(char)
	add(1)
	output()
	goto(inp)
	sub(1)
goto(char)
sub_null()
goto(0)
sub_null()

print code

# -*- coding: utf-8 -*-
import sys


def read_triggers(list_of_triggers, alt_value=None):
	"""Returns following element of one in list_of_triggers in sys.argv"""
	for trigger in list_of_triggers:
		if trigger in sys.argv:
			return sys.argv[sys.argv.index(trigger) + 1]
	return alt_value


#Read conf from comandline
filename = read_triggers(["-f", "--file"])
if filename is None:
	if len(sys.argv) < 2:
		filename = "."
	filename = sys.argv[1]

try:
	code_file = open(filename, "r")
except IOError:
	raise IOError("Could not find specified file: \"" + filename + "\"")

#ascii or str out
print_mode = read_triggers(["-m", "--mode"], "ascii")

#define log_out
log_file_name = read_triggers(["-l", "--log"], "None")
if log_file_name == "stdout":
	log_file = sys.stdout
elif log_file_name == "None":
	log_file = open("/dev/null", "w")
else:
	log_file = open(log_file_name, "w")

#define out for stdout
out_file_name = read_triggers(["-o", "--output"], "stdout")
if out_file_name == "stdout":
	out_file = sys.stdout
else:
	out_file = open(out_file_name, "w")

#define in for stdin
in_file_name = read_triggers(["-i", "--input"], "stdin")
if in_file_name == "stdin":
	in_file = sys.stdin
else:
	in_file = open(in_file_name, "r")

#load code
code = code_file.read()
#remove unnecessary chars
code = "".join([char for char in code
	if char in ["<", ">", "+", "-", ",", ".", "[", "]"]])


def find_partner(start_index):
	for index in range(len(tmp_code) - start_index - 1):
		char = tmp_code[index + start_index + 1]
		if char == "[":
			find_partner(index + start_index + 1)
		if char == "]":
			jmps[index + start_index + 1] = start_index
			tmp_code[index + start_index + 1] = "*"
			tmp_code[start_index] = "\'"
			break

tmp_code = list(code)
jmps = {}
while "[" in tmp_code:
	find_partner(tmp_code.index("["))

stack = {0: 0}
input_stack = []
pointer = 0
skip = False
run = True
index = 0
counter = 0

while run:

	char = code[index]

	log_file.write(str(counter) + ": " + str(list(stack.values()))
			+ "  " + str(pointer) + " | " + char + "\n")
	counter += 1

	if not pointer in stack:
		stack[pointer] = 0

	if not skip:
		if char == "+":
			stack[pointer] += 1
		elif char == "-":
			stack[pointer] -= 1
		elif char == ".":
			if print_mode == "ascii":
				out_file.write(chr(stack[pointer] % 256))
			else:
				out_file.write(str(stack[pointer]))
		elif char == ",":
			if len(input_stack) == 0:
				input_stack = list(in_file.read())
				try:
					input_stack = [int(value) for value in input_stack]
				except ValueError:
					input_stack = [ord(value) for value in input_stack]
				if len(input_stack) == 0:
					input_stack = [0]
			stack[pointer] = input_stack.pop(0)

		elif char == ">":
			pointer += 1
		elif char == "<":
			pointer -= 1

	if char == "[":
		start_index = index
		if stack[pointer] == 0:
			skip = True
	elif char == "]":
		skip = False
		if stack[pointer] != 0:
			index = jmps[index]

	index += 1
	if index == len(code):
		run = False

print("")

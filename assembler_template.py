#!/usr/bin/env python
#
# Template for MIPS assembler.py
#
# Usage:
#    python assembler_template.py [asm file]

import sys, re

def bin_to_hex(x):
  y = hex(int(x,2))[2:]
  if len(y) < 8:
    y = (8-len(y))*"0" + y
  return y

def dec_to_bin(value, nbits):
  value = int(value)
  fill = "0"
  if value < 0:
    value = (abs(value) ^ 0xffffffff) + 1
    fill = "1"

  value = bin(value)[2:]
  if len(value) < nbits:
    value = (nbits-len(value))*fill + value
  if len(value) > nbits:
    value = value[-nbits:]
  return value

rtypes = [
  # List of all R-type instructions.
  "sll",
  "srl",
  "sra",
  "jr",
  "add",
  "sub",
  "and",
  "or",
  "xor",
  "nor",
  "slt"
]

op_codes = {
  # Fill in mapping from instruction to its opcode.
  "add" : 
  "addi" : dec_to_bin(8, 6)
  "sub" :
  "and" :
  "andi" : int('0b001100')
  "or" :
  "ori" : int('0b001101')
  "xor" :
  "xori" : int('0b001110')
  "nor" :
  "sll" : int('0b000000')
  "sra" :
  "srl" :
  "slt" :
  "slti" : int('0b001010')
  "beq" : int('0b000100')
  "bne" : int('0b000101')
  "j" : int('0b000010')
  "jal" : int('0b000011')
  "jr" :
  "lw" : int('0b100011')
  "sw" : int('0b101011')
  "nop" : bin(0, 32)
}

function_codes = {
  # Fill in function codes.
  "sll",
  "srl",
  "sra",
  "jr",
  "add",
  "sub",
  "and",
  "or",
  "xor",
  "nor",
  "slt" : 
}

registers = {
  '$zero' : dec_to_bin(00, 5),
  # Fill out the rest of the registers.
}

def main():
  me, fname = sys.argv

  f = open(fname, "r")
  labels = {}        # Map from label to its address.
  parsed_lines = []  # List of parsed instructions.
  address = 0        # Track the current address of the instruction.
  line_count = 0     # Number of lines.
  for line in f:
    line_count = line_count + 1

    for attr in line.split():
      if attr.
    # Stores attributes about the current line of code, like its label, line
    # number, instruction, and arguments.
    line_attr = {}

    # Handle comments, whitespace.

    if line:
      # We'll get you started here with line_count.
      line_attr['line_number'] = line_count

      # Handle labels
      # Parse the rest of the instruction and its register arguments.

      # Finally, add this dict to the complete list of instructions.
      parsed_lines.append(line_attr)
  f.close()

  machine = ""  # Current machine code word.

  for line in parsed_lines:
    if line['instruction'] == 'nop':
      print 8*'0'
    elif line['instruction'] in rtypes:
      # Encode an R-type instruction.
      print 'Not Implemented'
    else:
      # Encode a non-R-type instruction.
      # Hint: the function_codes map will be useful here.
      print 'Not Implemented'
      # We'll get you started with jr.
      if line['instruction'] == 'jr':
        print 'Not Implemented'
        # Fill out jr.

      # Finish handling the rest of the instructions (load/store, other jumps).

if __name__ == "__main__":
  main()

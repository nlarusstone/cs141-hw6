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
  "add",
  "sub",
  "and",
  "or",
  "xor",
  "nor",
  "jr",
  "slt"
]

itypes = [
  "addi",
  "andi",
  "ori",
  "xori",
  "slti",
  "beq",
  "bne",
  "lw",
  "sw"
]

op_codes = {
  # Fill in mapping from instruction to its opcode.
  "add" : dec_to_bin(0, 6),
  "addi" : dec_to_bin(8, 6),
  "sub" : dec_to_bin(0, 6),
  "and" : dec_to_bin(0, 6),
  "andi" : dec_to_bin(12, 6),
  "or" : dec_to_bin(0, 6),
  "ori" : dec_to_bin(13, 6),
  "xor" : dec_to_bin(0, 6),
  "xori" : dec_to_bin(14, 6),
  "nor" : dec_to_bin(0, 6),
  "sll" : dec_to_bin(0, 6),
  "sra" : dec_to_bin(0, 6),
  "srl" : dec_to_bin(0, 6),
  "slt" : dec_to_bin(0, 6),
  "slti" : dec_to_bin(10, 6),
  "beq" : dec_to_bin(4, 6),
  "bne" : dec_to_bin(5, 6),
  "j" : dec_to_bin(2, 6),
  "jal" : dec_to_bin(3, 6),
  "jr" : dec_to_bin(0, 6),
  "lw" : dec_to_bin(35, 6),
  "sw" : dec_to_bin(43, 6),
  "nop" : dec_to_bin(0, 32)
}

function_codes = {
  # Fill in function codes.
  "sll": dec_to_bin(0, 6),
  "srl": dec_to_bin(2, 6),
  "sra": dec_to_bin(3, 6),
  "jr": dec_to_bin(8, 6),
  "add": dec_to_bin(32, 6),
  "sub": dec_to_bin(34, 6),
  "and": dec_to_bin(36, 6),
  "or": dec_to_bin(37, 6),
  "xor": dec_to_bin(38, 6),
  "nor": dec_to_bin(39, 6),
  "slt" : dec_to_bin(42, 6)
}

registers = {
  '$zero' : dec_to_bin(0, 5),
  '$at' : dec_to_bin(1,5),
  '$v0' : dec_to_bin(2,5),
  '$v1' : dec_to_bin(3,5),
  '$a0' : dec_to_bin(4,5),
  '$a1' : dec_to_bin(5,5),
  '$a2' : dec_to_bin(6,5),
  '$a3' : dec_to_bin(7,5),
  '$t0' : dec_to_bin(8,5),
  '$t1' : dec_to_bin(9,5),
  '$t2' : dec_to_bin(10,5),
  '$t3' : dec_to_bin(11,5),
  '$t4' : dec_to_bin(12,5),
  '$t5' : dec_to_bin(13,5),
  '$t6' : dec_to_bin(14,5),
  '$t7' : dec_to_bin(15,5),
  '$s0' : dec_to_bin(16,5),
  '$s1' : dec_to_bin(17,5),
  '$s2' : dec_to_bin(18,5),
  '$s3' : dec_to_bin(19,5),
  '$s4' : dec_to_bin(20,5),
  '$s5' : dec_to_bin(21,5),
  '$s6' : dec_to_bin(22,5),
  '$s7' : dec_to_bin(23,5),
  '$t8' : dec_to_bin(24,5),
  '$t9' : dec_to_bin(25,5),
  '$k0' : dec_to_bin(26,5),
  '$k1' : dec_to_bin(27,5),
  '$gp' : dec_to_bin(28,5),
  '$sp' : dec_to_bin(29,5),
  '$fp' : dec_to_bin(30,5),
  '$ra' : dec_to_bin(31,5)
}

def main():
  me, fname = sys.argv

  f = open(fname, "r")
  labels = {}           # Map from label to its address.
  parsed_lines = []     # List of parsed instructions.
  address = 0x00400000  # Track the current address of the instruction.
  line_count = 0        # Number of lines.
  for line in f:
    line_count += 1

    # Stores attributes about the current line of code, like its label, line
    # number, instruction, and arguments.
    line_attr = {}

    line = line.replace(',', '')
    split = line.split('#')[0].split()
    # Handle comments, whitespace.

    if line:
      # We'll get you started here with line_count.
      line_attr['line_number'] = line_count

      if split[0] == 'nop':
        line_attr['instruction'] = 'nop'
        parsed_lines.append(line_attr)
        address += 4
        continue

      # Handle labels
      # Parse the rest of the instruction and its register arguments.
      index = 0
      if ':' in split[index]:
        label = split[index][:-1]
        labels[label] = address
        line_attr['label'] = label
        index += 1

      line_attr['instruction'] = split[index]
      index += 1
      line_attr['arg0'] = split[index]
      index += 1

      if len(split) > index:
        line_attr['arg1'] = split[index]
        index += 1

      if len(split) > index:
        line_attr['arg2'] = split[index]
        index += 1

      # Finally, add this dict to the complete list of instructions.
      parsed_lines.append(line_attr)
      address += 4
  f.close()

  out = open("output.machine", "w")
  #machine = ""  # Current machine code word.
  for line in parsed_lines:
    machine = ''
    if line['instruction'] == 'nop':
      machine = 8 *'0'
    elif line['instruction'] in rtypes:
      # Encode an R-type instruction.
      machine += dec_to_bin(0, 5)

      if line['instruction'] == 'jr':
          machine += registers[line['arg0']]
          machine += dec_to_bin(0, 15)
      elif line['instruction'] == 'sll' or line['instruction'] == 'sra' or line['instruction'] == 'srl':
        if line['arg1'] in registers:
          machine += registers[line['arg1']]
        else:
          machine += dec_to_bin(line['arg1'], 5)
        machine += registers[line['arg0']]
        if line['arg2'] in registers:
          machine += registers[line['arg2']]
        else:
          machine += dec_to_bin(line['arg2'], 5)
      else:
        machine += registers[line['arg1']]
        machine += registers[line['arg2']]
        machine += registers[line['arg0']]
        machine += dec_to_bin(0, 5)

      machine += function_codes[line['instruction']]

    elif line['instruction'] in itypes:
      machine = '1'
    else:
      machine += op_codes[line['instruction']]
      # Encode a J-type instruction.
      if line['arg0'] in labels:
        print 'JAL'
        addr = labels[line['arg0']]
        machine += dec_to_bin(addr, 32)[6:30]
        print machine
      elif line['arg0'] in registers:
        machine += registers[line['arg0']]
        machine += dec_to_bin(0, 21)
      else:
        machine += dec_to_bin(line['arg0'], 26)

    print bin_to_hex(bin(int(machine, 2)))
  out.close()

def sign_extend(num, bits):
  for i in xrange(bits):
    num = num[0] + num
  return num

if __name__ == "__main__":
  main()

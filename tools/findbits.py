#!/usr/bin/python

#  findbits.py - find Binary, Octal, Decimal or Hex number in bitstream
# 
#  Adam Laurie <adam@algroup.co.uk>
#  http://rfidiot.org/
# 
#  This code is copyright (c) Adam Laurie, 2009, All rights reserved.
#  For non-commercial use only, the following terms apply - for all other
#  uses, please contact the author:
#
#    This code is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#

import sys
import os
import string

# invert binary string
def invert(data):
	i=  0
	out= ''
	while(i < len(data)):
		if data[i] == '0':
			out += '1'
		else:
			out += '0'
		i += 1
	return out

# do the actual search
def search(target,data):
	location= string.find(data,target)
	if location >= 0:
		print '*** Match at bit %d:' % location,
		print '%s<%s>%s' % (data[:location],target,data[location+len(target):])
	else:
		print 'Not found'

# convert integer to binary string
def binstring(number):
	out= ''
	while number > 0:
		out += chr(0x30 + (number & 0x01))
		number= number >> 1
	return stringreverse(out)

# reverse string order
def stringreverse(data):
	out= ''
	for x in range(len(data) -1,-1,-1):
		out += data[x]
	return out

# match forward, backward and inverted
def domatch(number,binary):
	reversed= stringreverse(number)
	inverted= invert(binary)

	print '  Forward: (%s)' % number,
	search(binary,number)
	print '  Reverse: (%s)' % reversed,
	search(binary,reversed)
	print '  Inverse: (%s)' % inverted
	print '    Forward: (%s)' % number,
	search(inverted,number)
	print '    Reverse: (%s)' % reversed,
	search(inverted,reversed)

if(len(sys.argv) < 3):
	print
	print '\t'+sys.argv[0] + ' - Search bitstream for a known number'
	print
	print 'Usage: ' + sys.argv[0] + ' <NUMBER> <BITSTREAM>'
	print
	print '\tNUMBER will be converted to it\'s BINARY equivalent for all valid'
	print '\tinstances of BINARY, OCTAL, DECIMAL and HEX, and the bitstream'
	print '\tand it\'s inverse will be searched for a pattern match. Note that'
	print '\tNUMBER must be specified in BINARY to match leading zeros.'
	print
	print 'Example:'
	print
	print '\tfindbits.py 73 0110010101110011'
	print
	os._exit(True)

bases=	{ 
	2:'BINARY',
	8:'OCTAL',
	10:'DECIMAL',
	16:'HEX',
       	}

for base in 2,8,10,16:
	try:
		number= int(sys.argv[1],base)
		print
		print 'Trying', bases[base]
		# do BINARY as specified to preserve leading zeros
		if base == 2:
			domatch(sys.argv[1],sys.argv[2])
		else:
			domatch(binstring(number),sys.argv[2])
	except:
		continue

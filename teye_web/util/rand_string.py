#coding=utf-8
'''
rand_string.py
'''
from string import letters, digits
from random import choice, randint

def rand_letter(length=0):
    '''
    '''
    return ''.join(choice(letters) for x in xrange(length or randint(6, 10)))
    
def rand_char(length=0):
    '''	
    '''
    str_char = ''.join([letters, digits])
    return ''.join(choice(str_char) for x in xrange(length or randint(6, 10)))

def rand_number(length=0):
    '''
    '''
    return ''.join(choice(digits) for x in xrange(length or randint(6, 10)))


if __name__=="__main__" :
	'''
	'''
	print rand_letter(10)
	print rand_char(10)
	print rand_number(10)

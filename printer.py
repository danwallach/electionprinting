import sys
from sys import argv

def main():
	usage = 'Command Syntax: \n\t./printer input_filename \nArguments:\n\tinput_filename\tfile of voters to format to PDF\n'
	if (len(argv) >= 2 and argv[1] == '-h') or len(argv) <= 1 or len(argv) > 2:
	    print usage
	elif len(argv) == 2:
		# print PDFs
		print_pdfs(argv[1])


def print_pdfs(filename):

	print(filename)




main()
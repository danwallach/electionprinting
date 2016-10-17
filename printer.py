import sys
from sys import argv
from reportlab.pdfgen import canvas

from reportlab.lib.units import inch
from reportlab.lib.colors import magenta, red

def main():
	print sys.path
	usage = 'Command Syntax: \n\t./printer input_filename \nArguments:\n\tinput_filename\tfile of voters to format to PDF\n'
	if (len(argv) >= 2 and argv[1] == '-h') or len(argv) <= 1 or len(argv) > 2:
	    print usage
	elif len(argv) == 2:
		# print PDFs
		print_pdfs(argv[1])


def print_pdfs(filename):
	

	c = canvas.Canvas("hello.pdf")

	c.setFont("Times-Roman", 20)
	c.setFillColor(red)
	c.drawCentredString(2.75*inch, 2.5*inch, "Font size examples")
	c.setFillColor(magenta)

	lyrics = ["hi", "hello", "goodbye", "hi"]
	size = 7
	y = 2.3*inch
	x = 1.3*inch
	for line in lyrics:
		c.setFont("Helvetica", size)
		c.drawRightString(x,y,"%s points: " % size)
		c.drawString(x,y, line)
		y = y-size*1.2
		size = size+1.5

 	c.showPage()
 	c.save()
	print(filename)




main()
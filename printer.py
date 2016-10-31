import sys
from sys import argv

from reportlab.lib import colors
from reportlab.lib.colors import magenta, red
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph


class SelectionInfo:

	def __init__(self, race_name, selection, party):
		self.race_name = race_name
		self.selection = selection
		self.party = party


def main():
	usage = 'Command Syntax: \n\t./printer input_filename num_columns\nArguments:\n\tinput_filename\tfile of voters to format to PDF\n\tnum_columns\tnumber of columns for PDF\n'
	if argv[1] == '-h' or len(argv) <= 1 or len(argv) > 3:
	    print usage
	elif len(argv) == 3:
		# print PDFs
		print_pdfs(argv[1], argv[2])


def print_pdfs(filename, num_columns):

	spaced_flag = True
	space_between_columns = .2

	ncols = int(num_columns)
	if spaced_flag:
		ncols = ncols + ncols-1

	doc = SimpleDocTemplate(filename, pagesize=letter)

	styles = getSampleStyleSheet()
	styleN = styles["BodyText"]
	styleN.alignment = TA_LEFT

	results = []
	for i in range(0, 30):
		results.append(SelectionInfo("Presiding Judge Texas Supreme Court Place 3", "Randy H. Clemons", "DEM"));

	num_rows = len(results)/int(num_columns)

	data = []
	candidate_index = 0
	style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)

	for i in range(num_rows):
		new_row = []
		for j in range(ncols):

			if spaced_flag and j % 2 == 1:
				new_row.append("  ")

			else:
				# Table for each race
				race_name = Paragraph("<b>"+results[i].race_name+"</b>", styleN)
				selection_name = results[i].selection
				party = Paragraph("<b>"+results[i].party+"</b>", style_right)

				race_data = [[race_name], [selection_name, party]]

				race_table = Table(race_data,style=[('SPAN',(0,0),(1,0)), ('LINEBELOW', (0,1), (1,1), 1, colors.black)])
				# selection = Paragraph("<b>" + results[i].race_name+ "</b><br/>" + "\n" + results[i].selection, styleN)
				new_row.append(race_table)
				candidate_index += 1

			if candidate_index >= len(results):
				break
		data.append(new_row)
		if candidate_index >= len(results):
				break

	column_widths = []
	if spaced_flag:
		column_size = (7.5 - (int(num_columns)-1)*space_between_columns) / int(num_columns)

		for i in range(ncols + ncols-1):
			if i % 2 == 1:
				column_widths.append(inch*space_between_columns)
			else:
				column_widths.append(inch*column_size)

		print (int(num_columns)-1)*space_between_columns + column_size*int(num_columns)
	else:
		column_widths = [7.5*inch/ncols] * ncols

	t=Table(data,colWidths=inch*7.5/len(data[0]), style=[])

	elements = []
	elements.append(t)

	doc.build(elements)

	# c.setFont("Times-Roman", 20)
	# c.setFillColor(red)
	# # c.drawCentredString(2.75*inch, 2.5*inch, "Font size examples")
	# c.setFillColor(magenta)

	# lyrics = ["hi", "hello", "goodbye", "hi"]
	# size = 7
	# y = 2.3*inch
	# x = 1.3*inch
	# for line in lyrics:
	# 	c.setFont("Helvetica", size)
	# 	c.drawRightString(x,y,"%s points: " % size)
	# 	c.drawString(x,y, line)
	# 	y = y-size*1.2
	# 	size = size+1.5

 	# c.showPage()
 	# c.save()


main()



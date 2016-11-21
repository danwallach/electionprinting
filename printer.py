import sys
import math
import ConfigParser


from reportlab.lib import colors
from reportlab.lib.colors import magenta, red
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.pagesizes import letter, legal
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Image, PageBreak, Frame, PageTemplate, NextPageTemplate
from sys import argv
from reportlab.lib.units import mm
from functools import partial

"""
1) create a way to read race info from a file

	what type of file? STAR link in here?

2) anchor barcode in bottom left
3) make num_rows depend on amount of text 
	can we check the height of paragraph to determine when a col gets too long
4) look into human testing readability limits and consider making chart
5) finish config file setup
6) create documentation

"""

styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT

page_size = letter
font_size = 7
font_type = 'Times-Roman'
 
def header_footer(canvas, doc):
    canvas.saveState()
    # Footer
    barcode = Image("barcode1.jpg")
    barcode.drawHeight = 2.25*inch*barcode.drawHeight / barcode.drawWidth
    barcode.drawWidth = 2.25*inch
    barcode.hAlign = 'LEFT'
    barcode.vAlign = 'BOTTOM'

    w, h = barcode.wrap(doc.width, doc.bottomMargin)
    barcode.drawOn(canvas, doc.leftMargin + 15, h)

    # Header
    header = []
    header_style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
    header.append([Paragraph("<font size=12><b>Official Ballot</b></font><font size=8><br/>November 8, 2016 General Election<br/>Harris County, Texas Precinct 101A </font>", styleN), [barcode, Paragraph('<b><font size=15>PLACE THIS IN BALLOT BOX</font></b>', header_style_right)]])
    header = Table(header, colWidths=[inch*3, inch*5], style=[('FONTSIZE', (0, 0), (-1, -1), 50), ('TEXTFONT', (0, 0), (1, 0), font_type), ('ALIGN',(1,0),(1,0),'RIGHT')])

    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin + 15, doc.height + doc.topMargin - h)

    canvas.restoreState()


FONTSIZE = 0

class SelectionInfo:

	def __init__(self, race_name, selection, party):
		self.race_name = race_name
		self.selection = selection
		self.party = party


def main():
	usage = 'Command Syntax: \n\t./printer input_filename num_columns\nArguments:\n\tinput_filename\tfile to save results to\n\tnum_columns\tnumber of columns for PDF\n\traces_filename\tsemi-colon delimited list of race results\n'
	if argv[1] == '-h' or len(argv) <= 1 or len(argv) > 4:
	    print(usage)
	elif len(argv) == 4:
		# print PDFs
		print_pdfs(argv[1], argv[2], argv[3])


def print_pdfs(filename, num_columns, races):

	config = ConfigParser.ConfigParser()
	config.read('config.cfg')
	page_size = config.get('Paper', 'size')
	font_size = config.getint('Fonts', 'font_size')
	font_type = config.get('Fonts', 'font_type')

	styleN.fontSize = font_size

	page_type = letter
	if page_size == 'Legal':
		page_type = legal


	ncols = int(num_columns)

	doc = SimpleDocTemplate(filename, pagesize=page_type, topMargin=15, bottomMargin=15, leftMargin=0, rightMargin=15)

	style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
	style_right.fontSize = font_size


	results = []
	f = open(races, "r")
	for item in f.readlines():
		item = item.split(";")
		results.append(SelectionInfo(item[0], item[1], item[2].strip("\n")))

	#num_rows = math.ceil(len(results)/int(num_columns))
	num_rows = 12


	
	candidate_index = 0
	column_index = 0

	num_colums_total = math.ceil(len(results)/num_rows + 1)
	num_pages_total = math.ceil(num_colums_total/ncols)

	print("num cols total %i, num pages total %i" %(num_colums_total, num_pages_total))


	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-20*mm, id='normal2')
	template = PageTemplate(id='header_footer', frames=frame, onPage=header_footer)
	doc.addPageTemplates([template])

	elements = []

	for page in range(int(num_pages_total)):
		data = [[]]

		for i in range(ncols):
			new_col = []
			for j in range(num_rows):

				race_name = Paragraph("<b>"+results[candidate_index].race_name+"</b>", styleN)
				selection_name = Paragraph(results[candidate_index].selection, styleN)
				party = Paragraph("<b>"+results[candidate_index].party+"</b>", style_right)

				race_data = [[race_name], [selection_name, party]]

				race_table = Table(race_data, colWidths=[inch*7.5/ncols*24/32, inch*7.5/ncols*8/32], \
					style=[('SPAN',(0,0),(1,0)), ('LINEBELOW', (0,1), (1,1), 1, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 3)])

				new_col.append([race_table])
				candidate_index += 1

				if candidate_index >= len(results):
					break


			col_table = Table(new_col)
			data[0].append(col_table)
			column_index += 1
			if column_index >= num_colums_total:
				break

		column_widths = [8*inch/ncols] * ncols

		t=Table(data,colWidths=inch*8/ncols, style=[('VALIGN',(0,0), (-1, -1), 'TOP')],hAlign='LEFT')
		
		#elements.append(header)
		elements.append(t)
		#TODO: ensure this barcode is aligned to bottom of page, for example see 3 col with 59 races
		#elements.append(barcode)
		elements.append(NextPageTemplate('header_footer'))
		elements.append(PageBreak())

	#doc.addPageTemplates([template])

	#doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
	doc.build(elements)

main()

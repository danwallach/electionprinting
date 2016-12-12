import sys
import math
import barcode
from barcode.writer import ImageWriter
from svglib.svglib import svg2rlg

try:
	from configparser import ConfigParser
except:
	from ConfigParser import ConfigParser


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


styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT

# default values
page_size = letter
font_size = 7
font_type = 'Times-Roman'
page_num = 0
barcode_num_saved = ''
 
def header_footer(canvas, doc):
	global page_num

	canvas.saveState()

	# Footer

	# Create Barcode and increment page num
	bar_num_page = barcode_num_saved + str(page_num)
	page_num += 1
	ean = barcode.get('upc', bar_num_page)
	barcode_file_name = ean.save('upc' + bar_num_page)
	# converted to "ReportLab Graphics Drawing"
	barcode_drawing = svg2rlg(barcode_file_name)

	w, h = barcode_drawing.wrap(doc.width, doc.bottomMargin)

	barcode_drawing.drawOn(canvas, doc.leftMargin + 15, 15)

	# Header
	header = []
	header_style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
	try:
		header.append([Paragraph("<font size=12><b>Official Ballot</b></font><font size=8><br/>November 8, 2016 General Election<br/>Harris County, Texas Precinct 101A </font>", styleN), [barcode_drawing, Paragraph('<b><font size=15 name="' + font_type + '">PLACE THIS IN BALLOT BOX</font></b>', header_style_right)]])
	except:
		print('Error creating header. This font, ' + font_type + ', may not be allowed.')
		return
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
	global barcode_num_saved

	usage = 'Command Syntax: \n\t./printer input_filename\nArguments:\n\tinput_filename\tfile to save results to\n'
	if argv[1] == '-h' or len(argv) <= 2 or len(argv) > 3:
		print(usage)
	else:
		# print PDFs
		barcode_num_saved = argv[2]
		if len(barcode_num_saved) >= 11:
			print('\nERROR: Number for barcode is too long. Automatically truncating to 10 digitss. \nIf this is not inteded behavior please change barcode number.\n')
			barcode_num_saved = barcode_num_saved[0:10]
		print_pdfs(argv[1])


def print_pdfs(filename):
	global font_size, font_type, barcode_file_name

	# read in configurations
	config = ConfigParser()
	config.read('config.cfg')
	page_size = config.get('Paper', 'size')
	font_size = config.getint('Fonts', 'font_size')
	font_type = config.get('Fonts', 'font_type')
	num_columns = config.get('Columns', 'num_columns')
	races = config.get('Races', 'filename')

	styleN.fontSize = font_size
	styleN.fontName = font_type

	# determine page size
	page_type = letter
	if page_size == 'Legal':
		page_type = legal
		page_height = 670
	else:
		page_height = 470


	ncols = int(num_columns)

	doc = SimpleDocTemplate(filename, pagesize=page_type, topMargin=15, bottomMargin=15, leftMargin=0, rightMargin=15)

	# create styles
	style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
	style_right.fontSize = font_size
	style_right.fontName = font_type

	# read in races
	results = []
	try:
		f = open(races, "r")
		for item in f.readlines():
			item = item.split(";")
			if len(item) < 3:
				continue
			results.append(SelectionInfo(item[0], item[1], item[2].strip("\n")))
	except:
		print("Unable to read Races file: "+ str(races))
		return


	candidate_index = 0

	# Set up page
	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-30*mm, id='normal2')
	template = PageTemplate(id='header_footer', frames=frame, onPage=header_footer)
	doc.addPageTemplates([template])

	elements = []
	entries = 0
	bigH = 0

	# add entries to the page
	while entries < len(results):
		data = [[]]
		for i in range(ncols):
			new_col = []
			tot_h = 0

			# while there is still room in this column 
			while tot_h < page_height:
				
				# Format paragraphs for this race
				try:
					race_name = Paragraph("<b>"+results[candidate_index].race_name+"</b>", styleN)
					selection_name = Paragraph(results[candidate_index].selection, styleN)
					party = Paragraph("<b>"+results[candidate_index].party+"</b>", style_right)
				except:
					print('Error bolding text. This font may not be allowed, or it may not allow bolded text.')
					return

				# Create race data list from those paragraph
				race_data = [[race_name], [selection_name, party]]

				# form table from the race data information: 1 table per race that goes inside larger table
				race_table = Table(race_data, colWidths=[inch*7.5/ncols*23/32, inch*7.5/ncols*10/32], \
					style=[('SPAN',(0,0),(1,0)), ('LINEBELOW', (0,1), (1,1), 1, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 3), ('FONTNAME', (0, 0), (-1, -1), font_type)])
				w,h = race_table.wrap(0,0)
				tot_h += h
				new_col.append([race_table])
				candidate_index += 1
				entries += 1

				# we've added them all
				if candidate_index > (len(results) - 1):
					break

			col_table = Table(new_col)
			data[0].append(col_table)
			if candidate_index > (len(results) - 1):
				break
			
		column_widths = [8*inch/ncols] * ncols

		# Create table with all this information and add to this page, adding header and footer as well
		t=Table(data,colWidths=inch*8/ncols, style=[('VALIGN',(0,0), (-1, -1), 'TOP')],hAlign='LEFT')
		elements.append(t)
		elements.append(NextPageTemplate('header_footer'))
		elements.append(PageBreak())
		
	try:
		doc.build(elements)
	except:
		print("Error building the document, unable to determine cause.")


main()
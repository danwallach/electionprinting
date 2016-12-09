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

page_size = letter
font_size = 7
font_type = 'Times-Roman'
page_num = 0
 
def header_footer(canvas, doc):
	canvas.saveState()
	# Footer
	barcode = svg2rlg(barcode_file_name)
	#barcode = Image("barcode1.jpg")
	barcode.drawHeight = 2.25*inch*barcode.drawHeight / barcode.drawWidth
	barcode.drawWidth = 2.25*inch
	barcode.hAlign = 'LEFT'
	barcode.vAlign = 'BOTTOM'

	w, h = barcode.wrap(doc.width, doc.bottomMargin)
	barcode.drawOn(canvas, doc.leftMargin + 15, h)
	#canvas.drawImage(barcode, doc.leftMargin + 15, h)

	# Header
	header = []
	header_style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
	try:
		header.append([Paragraph("<font size=12><b>Official Ballot</b></font><font size=8><br/>November 8, 2016 General Election<br/>Harris County, Texas Precinct 101A </font>", styleN), [barcode, Paragraph('<b><font size=15 name="' + font_type + '">PLACE THIS IN BALLOT BOX</font></b>', header_style_right)]])
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
	usage = 'Command Syntax: \n\t./printer input_filename\nArguments:\n\tinput_filename\tfile to save results to\n'
	if argv[1] == '-h' or len(argv) <= 2 or len(argv) > 3:
		print(usage)
	else:
		# print PDFs
		print_pdfs(argv[1], argv[2])


def print_pdfs(filename, barcode_num):
	global font_size, font_type

	config = ConfigParser()
	config.read('config.cfg')
	page_size = config.get('Paper', 'size')
	font_size = config.getint('Fonts', 'font_size')
	font_type = config.get('Fonts', 'font_type')
	num_columns = config.get('Columns', 'num_columns')
	races = config.get('Races', 'filename')

	styleN.fontSize = font_size
	styleN.fontName = font_type

	page_type = letter
	if page_size == 'Legal':
		page_type = legal
		page_height = 700
	else:
		page_height = 500


	ncols = int(num_columns)

	doc = SimpleDocTemplate(filename, pagesize=page_type, topMargin=15, bottomMargin=15, leftMargin=0, rightMargin=15)

	style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
	style_right.fontSize = font_size
	style_right.fontName = font_type


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


	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-20*mm, id='normal2')
	template = PageTemplate(id='header_footer', frames=frame, onPage=header_footer)
	doc.addPageTemplates([template])

	elements = []
	entries = 0
	bigH = 0
	#print("Adding {} entries".format(len(results)))
	while entries < len(results):

		data = [[]]

		# generate barcode for this page
		ean = barcode.get('ean13', barcode_num + str(page_num))
		barcode_file_name = ean.save('ean13')

		for i in range(ncols):
			new_col = []
			tot_h = 0
			while tot_h < page_height:
				
				try:
					race_name = Paragraph("<b>"+results[candidate_index].race_name+"</b>", styleN)
					selection_name = Paragraph(results[candidate_index].selection, styleN)
					party = Paragraph("<b>"+results[candidate_index].party+"</b>", style_right)
				except:
					print('Error bolding text. This font may not be allowed, or it may not allow bolded text.')
					return

				race_data = [[race_name], [selection_name, party]]

				race_table = Table(race_data, colWidths=[inch*7.5/ncols*23/32, inch*7.5/ncols*10/32], \
					style=[('SPAN',(0,0),(1,0)), ('LINEBELOW', (0,1), (1,1), 1, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 3), ('FONTNAME', (0, 0), (-1, -1), font_type)])
				w,h = race_table.wrap(0,0)
				tot_h += h
				new_col.append([race_table])
				candidate_index += 1
				entries += 1
				if candidate_index > (len(results) - 1):
					break
			col_table = Table(new_col)
			data[0].append(col_table)
			if candidate_index > (len(results) - 1):
				#print('candidate_index >= len results: ' + str(candidate_index))
				break
			
		column_widths = [8*inch/ncols] * ncols

		t=Table(data,colWidths=inch*8/ncols, style=[('VALIGN',(0,0), (-1, -1), 'TOP')],hAlign='LEFT')
		
		elements.append(t)
		elements.append(NextPageTemplate('header_footer'))
		elements.append(PageBreak())
		
	try:
		doc.build(elements)
	except:
		print("invalid inputs")


main()
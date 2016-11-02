import sys
import math
from sys import argv

from reportlab.lib import colors
from reportlab.lib.colors import magenta, red
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Image, PageBreak


FONTSIZE = 7

class SelectionInfo:

	def __init__(self, race_name, selection, party):
		self.race_name = race_name
		self.selection = selection
		self.party = party


def main():
	usage = 'Command Syntax: \n\t./printer input_filename num_columns\nArguments:\n\tinput_filename\tfile to save results to\n\tnum_columns\tnumber of columns for PDF\n'
	if argv[1] == '-h' or len(argv) <= 1 or len(argv) > 3:
	    print(usage)
	elif len(argv) == 3:
		# print PDFs
		print_pdfs(argv[1], argv[2])


def print_pdfs(filename, num_columns):

	ncols = int(num_columns)

	doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=15, bottomMargin=15, leftMargin=0, rightMargin=15)

	styles = getSampleStyleSheet()
	styleN = styles["BodyText"]
	styleN.alignment = TA_LEFT
	styleN.fontSize = FONTSIZE

	style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
	style_right.fontSize = FONTSIZE
	header_style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)

	header = []
	barcode = Image("barcode1.jpg")
	barcode.drawHeight = 2.25*inch*barcode.drawHeight / barcode.drawWidth
	barcode.drawWidth = 2.25*inch
	barcode.hAlign = 'LEFT'
	barcode.vAlign = 'BOTTOM'


	header.append([Paragraph("<font size=12><b>Official Ballot</b></font><font size=8><br/>November 8, 2016 General Election<br/>Harris County, Texas Precinct 101A </font>", styleN), \
		[barcode, Paragraph('<b><font size=15>PLACE THIS IN BALLOT BOX</font></b>', header_style_right)]])
	# header.append(["", ""])
	#  
	header = Table(header, colWidths=[inch*3, inch*4.5], style=[('FONTSIZE', (0, 0), (-1, -1), 50), \
		('TEXTFONT', (0, 0), (1, 0), 'Times-Roman'), \
		('ALIGN',(1,0),(1,0),'RIGHT')])


	results = []
	races = [("President and Vice President", "Hillary Clinton / Tim Kaine", "DEM"),
		("Representative, District 2", "James B. Veasaw", "LIB"),
		("Railroad Commissioner", "Grady Yarbrough", "DEM"),
		("Justice, Supreme Court, Place 3", "Rodolfo Rivera Munoz", "GP"),
		("Justice, Supreme Court, Place 5", "Dori Contreras Garza", "GP"),
		("Justice, Supreme Court, Place 9", "Savannah Robinson", "DEM"),
		("Judge, Court of Criminal Appeals, Place 2", "Lawrence Larry Meyers", "DEM"),
		("Judge, Court of Criminal Appeals, Place 5", "William Bryan Strange, III", "LIB"),
		("Judge, Court of Criminal Appeals, Place 6", "Michael E. Keasler", "DEM"),
		("Member, State Board of Education, District 6" , "Donna Bahorich", "REP"),
		("State Senator, District 13" , "Borris L. Miles", "DEM"),
		("State Representative, District 134" , "Gilberto \"Gil\" Velasquez Jr.", "LIB"),
		("Chief Justice, 1st Court of Appeals" , "Sherry Radack", "REP"),
		("Justice, 14th Court of Appeals District, Place 2" , "Candace White", "DEM"),
		("Justice, 14th Court of Appeals District, Place 9" , "Tracy Elizabeth Christopher", "REP"),
		("District Judge, 11th Judicial District", "Kristen Hawkins", "DEM"),
		("District Judge, 61st Judicial District", "Erin Elizabeth Lunceford", "REP"),
		("District Judge, 80th Judicial District", "Larry Weiman", "DEM"),
		("District Judge, 125th Judicial District", "Sharon Hemphill", "REP"),
		("District Judge, 127th Judicial District", "Sarahjane Swanson", "REP"),
		("District Judge, 129th Judicial District", "Michael Gomez", "DEM"),
		("District Judge, 133rd Judicial District", "Cindy Bennett Smith", "REP"),
		("District Judge, 151st Judicial District", "Mike Englehart", "DEM"),
		("District Judge, 152nd Judicial District", "Robert K. Schaffer", "DEM"),
		("District Judge, 164th Judicial District", "Alexandra Smoots-Hogan", "DEM"),
		("District Judge, 165th Judicial District", "Debra Ibarra Mayfield", "REP"),
		("District Judge, 174th Judicial District", "Katherine McDaniel", "REP"),
		("District Judge, 176th Judicial District", "Nikita \"Niki\" Harmon", "DEM"),
		("District Judge, 177th Judicial District", "Robert	Johnson", "DEM"),
		("District Judge, 178th Judicial District", "Phil Gommels", "REP"),
		("District Judge, 179th Judicial District", "Kristin M. Guiney", "REP"),
		("District Judge, 215th Judicial District", "Fred Schuchart", "REP"),
		("District Judge, 333rd Judicial District", "Joseph \"Tad\"	Halbach", "REP"),
		("District Judge, 334th Judicial District", "Steven Kirkland", "DEM"),
		("District Judge, 337th Judicial District", "Renee Magee", "REP"),
		("District Judge, 338th Judicial District", "Ramona Franklin", "DEM"),
		("District Judge, 339th Judicial District", "Maria T. (Terri) Jackson", "DEM"),
		("District Judge, 351st Judicial District", "Mark Kent Ellis", "REP"),
		("District Judge, 507th Judicial District", "Julia Maldonado", "DEM"),
		("District Attorney", "Devon Anderson", "REP"),
		("Judge, County Civil Court at Law No. 1 (Unexpired Term)", "Clyde Raymond Leuchtag", "REP"),
		("Judge, County Criminal Court No. 16", "Darrell William Jordan", "DEM"),
		("County Attorney", "Jim Leitner", "REP"),
		("Sheriff", "Ed Gonzalez", "DEM"),
		("County Tax Assessor-Collector", "Ann Harris Bennett", "DEM"),
		("County Commissioner, Precinct 1", "Rodney Ellis", "DEM"),
		("Justice of the Peace, Precinct 1, Place 1", "Eric William Carter", "DEM"),
		("Constable, Precint 1", "Joe Danna", "REP"),
		("Houston I.S.D., Proposition 1", "AGAINST", "")]

	results = []
	for item in races:
		results.append(SelectionInfo(item[0], item[1], item[2]))

	#num_rows = math.ceil(len(results)/int(num_columns))
	num_rows = 15


	
	candidate_index = 0
	column_index = 0

	num_colums_total = math.ceil(len(races)/num_rows)
	num_pages_total = math.ceil(num_colums_total/ncols)

	print("num cols total %i, num pages total %i" %(num_colums_total, num_pages_total))


	elements = []

	for page in range(num_pages_total):
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
		
		elements.append(header)
		elements.append(t)
		#TODO: ensure this barcode is aligned to bottom of page, for example see 3 col with 59 races
		elements.append(barcode)
		elements.append(PageBreak())
		

	doc.build(elements)


main()



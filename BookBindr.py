# this is for bookbinding, for proper imposition required for the 
# creation of signatures with the correct pagination

# only works for DUPLEX PRINTING flipped on the SHORT EDGE, HORIZONTAL

from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path
import itertools

# get number of pages

file_str = 'pride-and-prejudice.pdf'

pdf = PdfFileReader(file_str)

page_no = pdf.getNumPages()

print('Number of pages: ' + str(page_no))

# calculate how many signatures this will create

# leaf_no has to be multiple of 4

leaf_no = 20

x = leaf_no - page_no%leaf_no

sig_no = (page_no + x)/leaf_no

print('Add ' + str(x) + ' pages to make ' + str(int(sig_no)) + ' signatures')

# add correct number of blank pages for signatures of 
# selected leaf number

pdf_writer = PdfFileWriter()
pdf_writer.appendPagesFromReader(pdf)

while x > 0:
    pdf_writer.addBlankPage()
    x = x - 1
    
name_str_ext = file_str.replace('.pdf', '_extended.pdf')

with Path(name_str_ext).open(mode='wb') as output_file:
    pdf_writer.write(output_file)

pdf_1 = PdfFileReader(name_str_ext)
page_no_1 = pdf_1.getNumPages()
print('New number of pages: ' + str(page_no_1))   

# first create lists of page positions

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

        
page_list_ori = list(range(0,page_no_1))
page_list_seg = list(chunks(page_list_ori,leaf_no))

page_list_imp = []

for item in page_list_seg:
    y = int(leaf_no/2)
    list1 = item[0:y]
    list2 = item[y:leaf_no]
    list2.reverse()
    zip_list = list(zip(list1, list2))
    single_impos_list = []
    for a,b in zip_list:
    
        if a%2 == 0:
            single_impos_list.append(b)
            single_impos_list.append(a)
        else:
            single_impos_list.append(a)
            single_impos_list.append(b)
        
    page_list_imp.append(single_impos_list)
    
page_list_imp = list(itertools.chain(*page_list_imp))

# move pages from original order into new order
# and write into new file

pdf_writer = PdfFileWriter()

for n in page_list_imp:
    page = pdf_1.getPage(n)
    pdf_writer.addPage(page)

name_str_imp = file_str.replace('.pdf', '_imposed.pdf')
    
with Path(name_str_imp).open(mode='wb') as output_file:
    pdf_writer.write(output_file)

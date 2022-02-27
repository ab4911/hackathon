# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 15:49:11 2022

@author: Aarefa Bhurka
"""
import fitz
from fpdf import FPDF

from pdfrw import PdfReader
import os


path = "C:/Users/Aarefa Bhurka/OneDrive/Desktop/hackathon/sample.pdf"


reader = os.path.basename(path)

pdf = FPDF()

doc = fitz.open(path)

pdf.add_page(orientation = 'L')
pdf.set_font("Arial", size = 15)
pdf.set_margins(left= 2.0, top= 2.0, right = -1.0)

for page in doc:
    highlights=[]
   
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            all_coordinates = annot.vertices
            if len(all_coordinates) == 4:
                highlight_coord = fitz.Quad(all_coordinates).rect
                highlights.append(highlight_coord)
            else:
                all_coordinates = [all_coordinates[x:x+4] for x in range(0, len(all_coordinates), 4)]
                for i in range(0,len(all_coordinates)):
                    coord = fitz.Quad(all_coordinates[i]).rect
                    highlights.append(coord)
        annot = annot.next
        
    all_words = page.get_text_words()
    
    highlight_text = []
    for h in highlights:
        sentence = [w[4] for w in all_words if   fitz.Rect(w[0:4]).intersects(h)]
        highlight_text.append(" ".join(sentence))
    
    line = 1
    
    for text in highlight_text:
        pdf.cell(300, 10, txt = text,
        		ln = line, align = 'L')
        line+=2


# save the pdf with name .pdf
pdf.output(reader+"_Notes.pdf")

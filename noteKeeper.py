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
    text_highlighted=[]
   
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            coords = annot.vertices
            if len(coords) == 4:
                coord_highlighted = fitz.Quad(coords).rect
                text_highlighted.append(coord_highlighted)
            else:
                coords = [coords[x:x+4] for x in range(0, len(coords), 4)]
                for i in range(0,len(coords)):
                    coord = fitz.Quad(coords[i]).rect
                    text_highlighted.append(coord)
        annot = annot.next
        
    words_bag = page.get_text_words()
    
    text_highlighted_words = []
    for h in text_highlighted:
        sentence = [w[4] for w in words_bag if   fitz.Rect(w[0:4]).intersects(h)]
        text_highlighted_words.append(" ".join(sentence))
    
    line = 1
    
    for text in text_highlighted_words:
        pdf.cell(300, 10, txt = text,
        		ln = line, align = 'L')
        line+=2


# save the pdf with name .pdf
pdf.output(reader+"_Notes.pdf")

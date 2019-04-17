import os
import re
import csv
import sys
from cStringIO import StringIO
from django.conf import settings

import spacy
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def extract_name(text):
    reload(sys)
    sys.setdefaultencoding('utf8')
    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(unicode(text))
    for ent in doc.ents:
        if ent.label_ == 'PER':
            return ent.text


def extract_skills(lookup, text):
    skills = []
    for word in text.split(' '):
        if word in lookup.keys():
            skills.append(word)
    return (list(set(skills)))

def parse_resume(resume):
    skills_dict = {}

    with open(os.path.join(settings.BASE_DIR, 'techskills.csv'), 'r') as ts:
        reader = csv.reader(ts)
        for row in reader:
            skills_dict[row[1]] = row[0]

    path = os.path.join(settings.MEDIA_ROOT, resume.resume.name)
    text = convert(path)
    name = extract_name(text).rstrip()
    text = text.lower().replace(',', '')
    sites = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    return {
        'name': name,
        'sites': sites,
        'email': re.findall('\S+@\S+', text)[0],
        'skills': extract_skills(skills_dict, text)
    }
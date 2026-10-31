"""Export an anonymous submission PDF and record reproducible format checks."""
from pathlib import Path
import hashlib,json,re,os
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[3]
PAPER=ROOT/'papers/meta-routing/intellisys2027'
OUT=ROOT/'output/pdf/IntelliSys2027_Tool_Recovery_Draft.pdf'

def main():
    source=PAPER/'main.tex'
    tex=source.read_text()
    tables='\n'.join(p.read_text() for p in PAPER.glob('*_table.tex'))
    cites={k for block in re.findall(r'\\cite\{([^}]+)\}',tex) for k in block.split(',')}
    bib=set(re.findall(r'@\w+\{([^,]+),',(PAPER/'references.bib').read_text()))
    assert cites==bib
    labels=re.findall(r'\\label\{((?:fig|tab):[^}]+)\}',tex+'\n'+tables)
    refs=set(re.findall(r'\\ref\{([^}]+)\}',tex))
    assert len(labels)==len(set(labels)) and all(label in refs for label in labels)
    assert all(token in tex for token in [r'\author{}',r'\authorrunning{}',r'\institute{}',r'\documentclass{svproc}'])
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\keywords',tex,re.S).group(1)
    assert 150<=len(abstract.split())<=250
    log=(PAPER/'build/main.log').read_text()
    assert not any(token in log for token in ['Overfull','undefined','LaTeX Warning:','\n!'])
    reader=PdfReader(PAPER/'build/main.pdf')
    writer=PdfWriter();writer.append_pages_from_reader(reader)
    title='When Tool Agreement Is Not Enough: Budgeted Recovery and Silent-Error Acceptance in Intelligent Workflows'
    writer.add_metadata({'/Title':title,'/Author':'','/Subject':'Anonymous IntelliSys 2027 research draft'})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('wb') as f:writer.write(f)
    final=PdfReader(OUT)
    text='\n'.join(p.extract_text() or '' for p in final.pages)
    references_page=next(i+1 for i,p in enumerate(final.pages) if '\nReferences\n' in p.extract_text())
    assert references_page<=18 and len(final.pages)-references_page+1<=7
    assert final.metadata.get('/Author','')==''
    assert not final.trailer['/Root'].get('/Metadata')
    # Keep identifying author strings outside distributable source bundles.
    identity_file=os.environ.get('INTELLISYS_AUTHOR_IDENTIFIERS_FILE')
    known=[s.strip().lower() for s in Path(identity_file).read_text().splitlines() if s.strip()] if identity_file else []
    forbidden=['/users/','mailto:','@gmail.com']+known
    links=[]
    for page in final.pages:
        for annotation in page.get('/Annots',[]):
            action=annotation.get_object().get('/A')
            if action and action.get('/URI'):links.append(str(action['/URI']))
    check='\n'.join([text,str(dict(final.metadata)),*links]).lower()
    assert not any(term in check for term in forbidden)
    assert '[?]' not in text and '??' not in text
    fonts={}
    for page in final.pages:
        for resource in page['/Resources'].get('/Font',{}).values():
            font=resource.get_object()
            for actual in font.get('/DescendantFonts',[font]):
                actual=actual.get_object();desc=actual.get('/FontDescriptor')
                if desc:
                    desc=desc.get_object();embedded=any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3'])
                    assert embedded;fonts[str(actual.get('/BaseFont'))]=True
    checks={'pages_total':len(final.pages),'references_start_page':references_page,'abstract_words':len(abstract.split()),
            'references_cited':len(cites),'figures_numbered_and_cited':sum(l.startswith('fig:') for l in labels),
            'tables_numbered_and_cited':sum(l.startswith('tab:') for l in labels),
            'author_metadata_empty':True,'generic_identity_strings_absent':True,
            'known_identity_patterns_checked':len(known),'owner_identifiers_absent':True if known else None,'embedded_body_fonts':list(fonts),
            'latex_warnings_or_overfull_boxes':False,'template_sha256':hashlib.sha256((PAPER/'svproc.cls').read_bytes()).hexdigest(),
            'pdf_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
            'limits':'Automated checks do not certify research originality, author review, or GenAI-policy eligibility.'}
    report=ROOT/'output/intellisys2027/PREFLIGHT.json';report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()

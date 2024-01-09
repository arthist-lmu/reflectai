# Reflectai Scraping

Folder locations for raw pdfs on the server: /nfs/data/reflectai/scientific_pdfs
Folder locations for processed files: /nfs/data/reflectai/scientific_pdfs/processed


Every paper has a a folder with a .json file of the same name. 

The json contains the text of the pdf, as well as an array of images with locations.

# Setup

python3 -m venv .venv
cd fatcat

Activate the python environment.
Inside the python env type:

pip install poetry
poetry install


# Scraping Journal PDFs from fatcat

# Identifiinng relevant publishers

Possible routes:
* Usings Lens.org search

List of 7 examples for selected publishers identified by issn:
* Art-History (Wiley (Blackwell Publishing)) https://portal.issn.org/resource/issn/0141-6790 ([Fatcat](https://fatcat.wiki/container/jgycezv425g3noofwb2asxefwi))
* Journal of Art Historiography (University of Birmingham) https://portal.issn.org/resource/issn/2042-4752 ([Fatcat](https://fatcat.wiki/container/mzxayawf4jfgpmk3bzhmhsagqq))
*  International Journal of Art and Art History (American Research Institute for Policy Development) American Research Institute for Policy Development https://portal.issn.org/resource/issn/2374-233X ([Fatcat](https://fatcat.wiki/container/5w6kmdih7rapnmchwgy4ouwa5a))
* Athanor (Department of Art History, Florida State University) https://portal.issn.org/resource/issn/0732-1619 ([Fatcat](https://fatcat.wiki/container/fmqbs7mct5buvdw5g26kogjehq))
* Baltic Journal of Art History (University of Tartu Press) https://portal.issn.org/resource/issn/1736-8812 ([Fatcat](https://fatcat.wiki/container/dbinufk7mzbjdameaqvl5embse))
* GISAP Culturology Sports and Art History (International Academy of Science and Higher Education) https://portal.issn.org/resource/issn/2054-0809 ([Fatcat](https://fatcat.wiki/container/ay23mjcbcnhcrlcbwop7mmvemq))
* Text and Image Essential Problems in Art History (Taras Shevchenko National University of Kyiv) https://portal.issn.org/resource/issn/2519-4801 ([Fatcat](https://fatcat.wiki/container/v4hinx7yyzgrhgp7byanwmjxdy))


# Publisher to DOI

Fatcat Api?

# DOI to PDF Link

Example paper:

"The Development of Painting from Primitive to Post-Modern: A Case Study of Egypt"
DOI: https://doi.org/10.15640/ijaah.v5n1a3


Three possible routes:
* Using [Fatcat Wiki](fatcat.wiki) API to translate DOI to PDF sources directly.  
Example paper in the webservice: https://fatcat.wiki/release/qd6tugevkfdsvd6xd4acej7t7u  
Example query: https://api.fatcat.wiki/v0/release/lookup?doi=10.15640/ijaah.v5n1a3&expand=files&hide=abstracts,refs
Notes: Fatcat is sometimes down  
* Using the Unpaywal API to get pdf and HTML links https://api.unpaywall.org/v2/10.15640/ijaah.v5n1a3?email=unpaywall_01@example.com  
Notes: Litmited to 100.000 requests per day
* Webscraping the sites linked by DOIs for pdf links (Could work for some set of definded journals)

# PDF Link to Content
Download and store pdfs in the folder downloaded_pdfs. Only examples should be commited to Github, as the size will expand the limits of git qulickly.
GIT-LFS or external hosting at TIB would be required.

Extract content of PDFs to the extracted_text directory. Possible toolchains:
* [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) (is used atm)
* [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/index.html)
* others

The content should be stored under the filename of the original file, as a UTF8 .txt

Images could be extracted with the fitz module from PyMuPDF and should be stored alongside the extracted text.

How to identify multi column pdf? 
Layoutparser:

https://pypi.org/project/layoutparser/

https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html

# Useful links
* Szczepanski's List of Open Access Journals: https://www.ebsco.com/open-access/szczepanski-list
* List of 150 Art History Journals: https://docs.google.com/spreadsheets/d/1B8sUm7B9hjHNY-YOslipljlQ-_TshFALmGzBIiiKNLQ
* List with a few online journals from Cambridge: https://libguides.cam.ac.uk/c.php?g=318378&p=4712521

# Using Fatcat dump to find journals

Fatcat dump 195.659 journals

Downloaded: https://archive.org/details/fatcat_bulk_exports_2022-11-24
Processing: removing languages other that de en
Remove obvous mismatches: Bio, Buissness, Medical etc


# Running KnowGL pipeline

```
poetry run pipeline -i /nfs/data/reflectai/redai-data/data/processed/rijksmuseum-20220107.jsonl -p '[{"plugin": "NLTKSentenceSplitter"}, {"plugin": "XLMRobertaLanguageDetection"},{"plugin": "SentenceMerger"}, {"plugin": "KnowGL"}]'
```

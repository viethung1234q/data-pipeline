import textwrap

# Dry run information
info = textwrap.dedent("""
===== Dry Run =====

1. luigi_main.py
- Get information of input article (by running 'luigi_subprocess.py' then read the file output)
- Connect to database and Display all articles have same category
- Insert input article (all the information got) to database connected

2. luigi_subprocess.py
- Crawl all data from the input article link, include:
    data = {
    'article_id': ,
    'title': ,
    'description': ,
    'date': ,
    'category': ,
    'link': ,
    'author': ,
    'tag': ,
    'update_date': 
    }
- Write all data crawled to file

===== Dry Run =====
""")

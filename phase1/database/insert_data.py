import json
import os
from datetime import datetime

from phase1.database import Session

from models import Article, Author, Category, Tag

db = Session()

# Get output file's path
now = datetime.now()
day_month_year = now.strftime('%d_%m_%Y') # DD_MM_YYYY
ROOT_DIR = os.path.abspath(__file__ + "/../../")
output_dir = os.path.join('output', f'{day_month_year}.jsonl')
final_path = os.path.join(ROOT_DIR, output_dir)

# Open output file for importing data into database
f = open(final_path, 'r', encoding='utf_8')

# Inser data into database
for data in f:
    dataJson = json.loads(data)

    """
    If article is not None -> already exist -> do nothing
    If article is None -> insert to database
    """
    article = db.query(Article).filter(Article.id == dataJson['article_id']).first()
    if not article:
        article = Article(
            id=dataJson['article_id'],
            title=dataJson['title'],
            description=dataJson['description'],
            publish_date=dataJson['date'], 
            url=dataJson['link'],
            update_date=dataJson['update_date']
        )
        db.add(article)

    author = db.query(Author).filter(Author.name == dataJson["author"]).first()
    if not author:
        author = Author(name=dataJson["author"])
        db.add(author)
    
    category = db.query(Category).filter(Category.name == dataJson["category"]).first()
    if not category:
        category = Category(name=dataJson["category"])
        db.add(category)

    for tagItem in dataJson["tag"]:
        tag = db.query(Tag).filter(Tag.name == tagItem).first()
        if not tag:
            tag = Tag(name=tagItem)
            db.add(tag)
        tag.articleTag.append(article)

    author.articleAuthor.append(article)
    category.articleCategory.append(article)

    db.commit()

# Close file
f.close()
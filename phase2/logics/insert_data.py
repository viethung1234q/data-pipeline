import json
import os

from phase1.database import Session, models

# Path to file of the input article
DIR = os.path.abspath(__file__ + "/../../")
output_path = os.path.join(DIR, "output")
article_path = os.path.join(output_path, "luigi_article.jsonl")

db = Session()

def insert_to_database():
    # Read file
    with open(article_path, 'r', encoding="utf_8") as f:
        data = f.read()
        inputArticle = json.loads(data)

    # Insert to database
    article = models.Article(
        id=inputArticle['article_id'],
        title=inputArticle['title'],
        description=inputArticle['description'],
        publish_date=inputArticle['date'],
        url=inputArticle['link'],
        update_date=inputArticle['update_date']
    )
    db.add(article)

    author = db.query(models.Author).filter(models.Author.name == inputArticle["author"]).first()
    if not author:
        author = models.Author(name=inputArticle["author"])
        db.add(author)
    
    category = db.query(models.Category).filter(models.Category.name == inputArticle["category"]).first()
    if not category:
        category = models.Category(name=inputArticle["category"])
        db.add(category)

    for tagItem in inputArticle["tag"]:
        tag = db.query(models.Tag).filter(models.Tag.name == tagItem).first()
        if not tag:
            tag = models.Tag(name=tagItem)
            db.add(tag)
        tag.articleTag.append(article)

    author.articleAuthor.append(article)
    category.articleCategory.append(article)

    db.commit()
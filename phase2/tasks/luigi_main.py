import json
import logging
import os
import subprocess
import sys

import luigi
from phase1.database import Session, models
from phase2.logics.dry_run_info import info
from phase2.logics.insert_data import insert_to_database

DIR = os.path.abspath(__file__ + "/../../")
output_path = os.path.join(DIR, "output")
luigi_path = os.path.join(output_path, "luigi_output.jsonl")
article_path = os.path.join(output_path, "luigi_article.jsonl")

logging.basicConfig(level=logging.INFO)


class GetArticleTask(luigi.Task):
    "Get all articles with the same category"

    dry_run = luigi.BoolParameter(
        default=True,
        parsing=luigi.BoolParameter.EXPLICIT_PARSING)

    # Output path
    def output(self):
        return luigi.LocalTarget(luigi_path)

    def run(self):
        if self.dry_run == True:
            logging.info(info)
        else:
            # Start crawling, then write output to 'luigiArticle.jsonl' file
            subprocess.run([sys.executable, "luigi_subprocess.py"])

            # Read 'luigiArticle.jsonl' file to get Article category
            with open(article_path, 'r', encoding="utf_8") as f:
                data = f.read()
                inputArticle = json.loads(data)
            
            # Query all articles have the same category
            db = Session()
            category = db.query(models.Category.id).filter(models.Category.name == inputArticle['category']).first()
            same_articles = db.query(models.Article.id, models.Article.url).filter(models.Article.category_id == category.id).all()
            
            # If article already exists in database, remove it from result
            # Else insert it to database
            duplicate = db.query(models.Article.id, models.Article.url).filter(models.Article.id == int(inputArticle['article_id'])).first()
            if duplicate:
                same_articles.remove(duplicate)
            else:
                insert_to_database()

            # Write to output file
            with self.output().open('w') as output_file:
                for item in same_articles:
                    data = {
                        'link': item.url
                    }
                    data_json_object = json.dumps(data, ensure_ascii=False)
                    output_file.write(data_json_object + "\n")

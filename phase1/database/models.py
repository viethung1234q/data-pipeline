from phase1.database import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

# Association table between Article and Tag
article_tag = Table(
    "articles_tags",
    Base.metadata,
    Column("articles_id", ForeignKey("articles.id"), primary_key=True),
    Column("tags_id", ForeignKey("tags.id"), primary_key=True),
)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    description = Column(String(500))
    publish_date = Column(Date)
    url = Column(String(255))
    update_date = Column(Date)

    # set Author - Article relationship: 1 - n
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="articleAuthor")
    
    # set Category - Article relationship: 1 - n
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="articleCategory")

    # set Tag - Article relationship: m - n
    tag = relationship(
        "Tag", secondary=article_tag, back_populates="articleTag"
    )


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    # set Author - Article relationship: 1 - n
    articleAuthor = relationship("Article", back_populates="author")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # set Category - Article relationship: 1 - n
    articleCategory = relationship("Article", back_populates="category")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    # set Tag - Article relationship: m - n
    articleTag = relationship(
        "Article", secondary=article_tag, back_populates="tag"
    )
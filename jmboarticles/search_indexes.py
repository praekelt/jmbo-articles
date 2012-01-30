import datetime
from haystack import indexes
from haystack import site
from article.models import Article


class ArticleIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def index_queryset(self):
        return Article.published_objects.all()


site.register(Article, ArticleIndex)
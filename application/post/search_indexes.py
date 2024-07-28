from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    author = indexes.CharField(model_attr='author__username')
    created_time = indexes.DateTimeField(model_attr='created_time')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
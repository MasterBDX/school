from django.forms import modelformset_factory

from .forms import MainArticleForm
from .models import MainArticle

MainArticleFormset = modelformset_factory(MainArticle,
                                          form=MainArticleForm,
                                          max_num=3,
                                          extra=0
                                          )

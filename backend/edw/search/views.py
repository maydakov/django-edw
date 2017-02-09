# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.mixins import ListModelMixin
from rest_framework.renderers import BrowsableAPIRenderer
from drf_haystack.generics import HaystackGenericAPIView
#from shop.rest.renderers import CMSPageRenderer
#from shop.rest.money import JSONRenderer


class SearchView(ListModelMixin, HaystackGenericAPIView):
    """
    A generic view to be used for rendering the result list while searching.
    """
    #renderer_classes = (CMSPageRenderer, JSONRenderer, BrowsableAPIRenderer)
    renderer_classes = (BrowsableAPIRenderer)
    serializer_class = None  # to be set by SearchView.as_view(serializer_class=...)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

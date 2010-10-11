# -*- coding: utf-8 -*-
from django import dispatch


pre_merge = dispatch.Signal(providing_args=["merge_pairs"])
pre_move = dispatch.Signal(providing_args=["moving"])

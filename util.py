# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas.motl@panodata.org>
# Distributed under the AGPLv3 License. See LICENSE for more info.
class DocHelper:
    def __init__(self, doc):
        self.doc = doc

    def find_tokens(self, types):
        for token in self.doc:
            if token.pos_ in types:
                yield token

    def find_names(self, types):
        for entity in self.doc.ents:
            if entity.label_ in types:
                yield entity

    def find_tags(self, types):
        for token in self.doc:
            if token.tag_ in types:
                yield token

    def find_token(self, *types):
        items = list(self.find_tokens(types))
        if items:
            return items[0].lemma_

    def find_name(self, *types, lemma=False):
        items = list(self.find_names(types))
        if items:
            if lemma:
                return items[0].lemma_
            else:
                return items[0].text

    def find_tag(self, *types, pure=False):
        items = list(self.find_tags(types))
        if items:
            if pure:
                return items[0]
            else:
                return items[0].lemma_

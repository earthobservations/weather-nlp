# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas.motl@panodata.org>
# Distributed under the AGPLv3 License. See LICENSE for more info.
import logging
import sys
from dataclasses import dataclass

import spacy

from util import DocHelper

logger = logging.getLogger(__name__)

DEBUG = True


@dataclass
class Result:
    where: str
    when: str
    what: str


models = {}


def load_model(name):

    global models

    if name in models:
        nlp = models[name]
    else:
        nlp = spacy.load(name)
        models[name] = nlp

    return nlp


def detect_language(text: str):
    import spacy
    from spacy_langdetect import LanguageDetector

    # Detect language.
    nlp = load_model("en")
    try:
        nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
    except:
        pass
    doc = nlp(text)
    language = doc._.language["language"]

    return language


def analyze_spacy(expression: str):

    # Load language-specific tokenizer, tagger, parser, NER and word vectors.
    language = detect_language(expression)
    print(f"Language: {language}")

    nlp = load_model(language)
    sentence = nlp(expression)

    # nlp = spacy.load("en_core_web_sm")
    # nlp = spacy.load("de_core_news_sm")

    if DEBUG:

        # https://stackabuse.com/python-for-nlp-tokenization-stemming-and-lemmatization-with-spacy-library/
        for word in sentence:
            # print(word.text, word.pos_)
            print(f"- [{word.pos_}, {word.tag_}] {word.text}")

        # Merge entities and noun chunks into one token
        """
        spans = list(doc.ents) + list(doc.noun_chunks)
        spans = spacy.util.filter_spans(spans)
        with doc.retokenize() as retokenizer:
            for span in spans:
                #retokenizer.merge(span)
                pass
        """

        print(sentence)
        # print(doc.text_with_ws)
        # print(doc.to_json())
        # print(dir(doc))

        for token in sentence:
            print(
                "token:",
                token,
                token.lemma_,
                token.pos_,
                token.tag_,
                list(token.subtree),
                token.sent,
            )
            # print(dir(token))
            print(list(token.subtree))
            # print(token.cluster)

        # Analyze syntax
        print("Noun phrases:", [chunk.text for chunk in sentence.noun_chunks])
        print("Nouns:", [token.lemma_ for token in sentence if token.pos_ == "NOUN"])
        print("Verbs:", [token.lemma_ for token in sentence if token.pos_ == "VERB"])
        print(
            "Adjectives:", [token.lemma_ for token in sentence if token.pos_ == "ADJ"]
        )

        # Find named entities, phrases and concepts.
        print("Named entities:")
        for entity in sentence.ents:
            print(f"- [{entity.label_}] {entity.text}")

        print("Phrases:")
        for phrase in sentence.noun_chunks:
            # print(dir(phrase))
            print(f"- [{phrase.label_}] {phrase.text}")

    entity_names = [entity.text for entity in sentence.ents]

    return improve_with_heuristics(nlp, expression, sentence)


def improve_with_heuristics(nlp, expression, sentence):

    dh = DocHelper(sentence)

    # A. Extraction

    try:
        what = list(sentence.noun_chunks)[0].lemma_
    except IndexError:
        what = dh.find_token("NOUN")

    # TODO: Use "pop_name" here.
    # where = dh.find_name("GPE", "LOC", "MISC", lemma=True).capitalize()
    where = dh.find_name("GPE", "LOC", "MISC")
    when = dh.find_name("DATE")

    if when is None:
        items = list(dh.find_tags("APPR"))
        # print(list(find_tag("APPR", pure=True).subtree))
        for item in dh.find_tags("APPR"):
            subtree = list(item.subtree)
            if len(subtree) >= 3:
                when = " ".join(map(str, subtree))

    # Berliner Temperatur => Temperatur
    if what is not None:
        for entity in sentence.ents:
            if entity.label_ not in ["TIME", "DATE"]:
                what = what.replace(entity.text, "")
        what = what.strip()

    if when is None:
        when = "now"

    if where is not None:

        # Nebel im Taunus
        if where.lower() == expression.lower():
            # where =
            try:
                where = list(sentence.noun_chunks)[1].lemma_
            except IndexError:
                try:
                    where = list(dh.find_tokens(["NOUN"]))[1]
                except IndexError:
                    pass

        # Regen in der Deutschen Bucht
        if where.lower() in when.lower():
            when = "now"

    # B. Formatting
    if where is not None:
        w = nlp(where)
        parts = [t.lemma_ for t in w]
        where = " ".join(parts).title()

    # Rain in Chengdu
    if where is None:
        try:
            where = list(sentence.noun_chunks)[1].lemma_
        except IndexError:
            pass

    result = Result(where=where, when=when, what=what)
    return result


def analyze_spacy_2():

    qualifier = find_name("TIME")
    if qualifier is None:
        candidate = find_token("ADJ")
        if (
            candidate is not None
            and candidate not in entity_names
            and candidate not in what
        ):
            qualifier = candidate


def analyze_flair(expression: str):
    from flair.data import Sentence
    from flair.models import MultiTagger, SequenceTagger

    # Make a sentence.
    sentence = Sentence(expression)

    # Load the NER tagger.
    # tagger = SequenceTagger.load("ner")

    # Load tagger for POS and NER.
    tagger = MultiTagger.load(["pos", "ner"])
    # tagger = MultiTagger.load([, "pos-multi-fast", "ner-multi-fast"])

    # Run tagger over sentence.
    tagger.predict(sentence)
    logger.info(sentence)

    if DEBUG:

        # Iterate over entities and print.
        logger.info("NER tags")
        for entity in sentence.get_spans("ner"):
            print(entity)

        # Iterate over entities and print.
        logger.info("POS tags")
        for entity in sentence.get_spans("pos"):
            print(entity)

    return

    print(dir(sentence))
    print(sentence.labels)
    print(sentence.to_dict())

    logger.info("The following NER tags are found:")

    print(sentence.to_tagged_string())


def query(expression: str) -> Result:

    if not expression:
        logger.warning("Empty expression")
        return

    logger.info(f"Analyzing '{expression}'")

    result = analyze_spacy(expression)
    logger.info(result)

    # result = analyze_flair(expression)
    # logger.info(result)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(message)s")
    expression = " ".join(sys.argv[1:])
    query(expression)


if __name__ == "__main__":
    main()
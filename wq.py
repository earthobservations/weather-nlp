# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas.motl@panodata.org>
# Distributed under the AGPLv3 License. See LICENSE for more info.
import logging
import sys
from dataclasses import dataclass

import spacy
from spacy_langdetect import LanguageDetector

from util import DocHelper

logger = logging.getLogger(__name__)

DEBUG = True


@dataclass
class Result:
    where: str
    when: str
    what: str


use_models = {}
english_model = None


def load_model(name):

    global use_models

    if name in use_models:
        nlp = use_models[name]
    else:
        nlp = spacy.load(name)
        # nlp = spacy.blank(name)
        use_models[name] = nlp

    return nlp


def detect_language(text: str):

    # Short-circuit misdetections.
    # Why? "snow depth on Zugspitze" is sometimes detected as German.
    if "snow" in text.lower() or "rain" in text.lower():
        return "en"

    global english_model

    if english_model is None:
        english_model = spacy.load("en")

    nlp = english_model

    # Detect language.
    try:
        nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
    except:
        pass
    doc = nlp(text)
    language = doc._.language["language"]

    # Correct language misdetections.
    if language == "ko":
        language = "zh-cn"

    # Map language to model.
    if language == "zh-cn":
        language = "zh_core_web_md"

    return language


def translate(from_language, to_language, text):
    # Load translator.
    from argostranslate import package, translate

    model_name = f"{from_language}_{to_language}"
    model_file = f"./var/translate-{model_name}-1.1.argosmodel"
    logger.info(f"Loading translation model from {model_file}")
    package.install_from_path(model_file)
    installed_languages = translate.get_installed_languages()
    translation_from, translation_to = installed_languages

    # Invoke translation.
    translator = translation_to.get_translation(translation_from)
    return translator.translate(text)


def analyze_spacy(expression: str):

    # Load language-specific tokenizer, tagger, parser, NER and word vectors.
    language = detect_language(expression)
    logger.info(f"Language: {language}")

    if language in ["hi"]:

        # Translate text.
        expression = translate(language, "en", expression)
        logger.info(f"Analyzing translation '{expression}'")

        # Load language-specific tokenizer, tagger, parser, NER and word vectors.
        language = detect_language(expression)
        logger.info(f"Language: {language}")

    # Analyze expression.
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
        what = list(sentence.noun_chunks)[0].lemma_.title()
    except IndexError:
        what = dh.find_token("NOUN", "PER")

    # TODO: Use "pop_name" here.
    # where = dh.find_name("GPE", "LOC", "MISC", lemma=True).capitalize()
    where = dh.find_name("GPE", "LOC", "MISC")
    when = dh.find_name("DATE")

    if when is None:
        items = list(dh.find_tags("APPR", "APPRART"))
        # print(list(find_tag("APPR", pure=True).subtree))
        for item in items:
            subtree = list(item.subtree)
            if len(subtree) >= 2:
                when = " ".join(map(str, subtree))

    # Berliner Temperatur => Temperatur
    if what is not None and where is not None and where in what:
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

    # "Temperature in Nanchang on 2020-09-17" in Chinese: "2020年9月17日南昌市的温度"
    if what in when:
        for noun in dh.find_tokens("NOUN"):
            if noun.lemma_ in when:
                continue
            what = noun.lemma_

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

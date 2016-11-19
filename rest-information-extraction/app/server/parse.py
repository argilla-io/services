from __future__ import unicode_literals

import textacy
import requests
import json

class Parse(object):
    def __init__(self, nlp, text, collapse_punctuation, collapse_phrases):
        self.doc = nlp(text)
        if collapse_punctuation:
            spans = []
            for word in self.doc[:-1]:
                if word.is_punct:
                    continue
                if not word.nbor(1).is_punct:
                    continue
                start = word.i
                end = word.i + 1
                while end < len(self.doc) and self.doc[end].is_punct:
                    end += 1
                span = self.doc[start : end]
                spans.append(
                    (span.start_char, span.end_char, word.tag_, word.lemma_, word.ent_type_)
                )
            for span_props in spans:
                self.doc.merge(*span_props)

        if collapse_phrases:
            for np in list(self.doc.noun_chunks):
                np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)

    def to_json(self):
        words = [{'text': w.text, 'tag': w.tag_} for w in self.doc]
        arcs = []
        for word in self.doc:
            if word.i < word.head.i:
                arcs.append(
                    {
                        'start': word.i,
                        'end': word.head.i,
                        'label': word.dep_,
                        'dir': 'left'
                    })
            elif word.i > word.head.i:
                arcs.append(
                    {
                        'start': word.head.i,
                        'end': word.i,
                        'label': word.dep_,
                        'dir': 'right'
                    })
        return {'words': words, 'arcs': arcs}


class Entities(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        return [{'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
                for ent in self.doc.ents]

class Triples(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)
    def get_uri(self, text):
        headers = {'Content-type': 'application/json'}
        data = {"size" : 1, "query" : {"match" : { "labelsGroup" : {"query": text, "operator": "and"}}}}
        data_json = json.dumps(data)
        response = requests.post("http://146.148.120.198:9200/_search?fields=id,type", data=data_json, headers=headers)
        hits = response.json()['hits']
        if(hits['total'] > 0):
            return hits['hits'][0]['_id']
        return ""
    def to_json(self):
        return [{'subject': triple[0].text,
                 'subject_uri': self.get_uri(triple[0].text),
                 's_start': triple[0].start_char,
                 's_end': triple[0].end_char,
                 'predicate': triple[1]['text'],
                 'object': triple[2].text,
                 'object_uri': self.get_uri(triple[2].text),
                 'o_start': triple[2].start_char,
                 'o_end': triple[2].end_char}
                for triple in textacy.extract.subject_verb_object_triples(self.doc)]

class Keywords(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        return [{'text': keyword[0], 'score': keyword[1]}
                for keyword in textacy.keyterms.sgrank(self.doc)]

class Concepts(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        return [{'text':chunk.text, 'start': chunk.start_char, 'end': chunk.end_char}
                for chunk in textacy.extract.noun_chunks(self.doc)]

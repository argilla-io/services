#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

from pathlib import Path
import falcon
import spacy
import json

import sys, traceback

from spacy.symbols import ENT_TYPE, TAG, DEP

import spacy.util

from .parse import Parse, Entities, Triples, Keywords


try:
    MODELS = spacy.util.LANGUAGES.keys()
except NameError:
    # Support older spaCy versions, pre 0.100.0
    data_dir = Path(spacy.util.__file__).parent / 'data'
    MODELS = [d for d in data_dir.iterdir() if d.is_dir()]


try:
    unicode
except NameError:
    unicode = str


_models = {}


def get_model(model_name):
    if model_name not in _models:
        _models[model_name] = spacy.load(model_name)
    return _models[model_name]


def get_dep_types(model):
    '''List the available dep labels in the model.'''
    labels = []
    for label_id in model.parser.moves.freqs[DEP]:
        labels.append(model.vocab.strings[label_id])
    return labels


def get_ent_types(model):
    '''List the available entity types in the model.'''
    labels = []
    for label_id in model.parser.moves.freqs[ENT_TYPE]:
        labels.append(model.vocab.strings[label_id])
    return labels


def get_pos_types(model):
    '''List the available part-of-speech tags in the model.'''
    labels = []
    for label_id in model.parser.moves.freqs[TAG]:
        labels.append(model.vocab.strings[label_id])
    return labels


class ModelsResource(object):
    """List the available models."""
    def on_get(self, req, resp):
        try:
            output = list(MODELS)
            resp.body = json.dumps(output.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500


class SchemaResource(object):
    """Describe the annotation scheme of a model."""
    def on_get(self, req, resp, model_name):
        try:
            model = get_model(model_name)
            output = {
                'dep_types': get_dep_types(model),
                'ent_types': get_ent_types(model),
                'pos_types': get_pos_types(model)
            }

            resp.body = json.dumps(output.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500


class DepResource(object):
    """Parse text and return displacy's expected JSON output."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        model_name = json_data.get('model', 'en')
        collapse_punctuation = json_data.get('collapse_punctuation', True)
        collapse_phrases = json_data.get('collapse_phrases', True)

        try:
            model = get_model(model_name)
            parse = Parse(model, text, collapse_punctuation, collapse_phrases)
            resp.body = json.dumps(parse.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500


class EntResource(object):
    """Parse text and return displaCy ent's expected output."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            entities = Entities(model, text)
            resp.body = json.dumps(entities.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500

class TriplesResource(object):
    """Parse text and return triples."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            triples = Triples(model, text)
            resp.body = json.dumps(triples.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            resp.status = falcon.HTTP_500

class KeywordsResource(object):
    """Parse text and return keywords."""
    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            keywords = Keywords(model, text)
            resp.body = json.dumps(keywords.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            resp.status = falcon.HTTP_500

APP = falcon.API()
APP.add_route('/dep', DepResource())
APP.add_route('/ent', EntResource())
APP.add_route('/triples', TriplesResource())
APP.add_route('/keywords', KeywordsResource())
APP.add_route('/{model_name}/schema', SchemaResource())
APP.add_route('/models', ModelsResource())

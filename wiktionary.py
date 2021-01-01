#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import django
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionaryDB.settings')
django.setup()
from wiktionaryparser import WiktionaryParser
from wikdictionary.models import (
    Dict,
    DictMap
)

definition_patterns = [
    re.compile('simple past tense and past participle of (\w+)'),
    re.compile('simple past tense of (\w+)'),
    re.compile('present participle of (\w+)'),
    re.compile('plural of (\w+)'),
    re.compile('Obsolete spelling of (\w+)'),
    re.compile('Third-person singular simple present indicative form of (\w+)'),
    re.compile('Alternative form of (\w+)'),
    re.compile('Alternative spelling of (\w+)'),
    re.compile('comparative form of (\w+)'),
]

etymology_patterns = [
    re.compile('^(\w+) \+\u200e -ly'),
]

def match(text, patterns):
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            return m
    return None

def main(x):
    """Run administrative tasks."""

    parser = WiktionaryParser()
    parser.set_default_language('english')
    toDelete = list()
    toMap = dict()
    # QS = Dict.objects.all()
    QS = Dict.objects.filter(word__startswith=x)
    for qs in QS:
        if re.search('\W', qs.word):
            toDelete.append(qs.word)
            continue
        wiki = parser.fetch(qs.word)
        if len(wiki) == 0:
            toDelete.append(qs.word)

        # whether in patterns
        for i in range(len(wiki)):
            if not ('definitions' in wiki[i]):
                continue
            for j in range(len(wiki[i]['definitions'])):
                if not ('text' in wiki[i]['definitions'][j]):
                    continue
                texts = wiki[i]['definitions'][j]['text']
                for text in texts:
                    m = match(text, definition_patterns)
                    if m:
                        toMap[qs.word] = m.group(1)
                        print('definition: ' + qs.word)
                        continue
                    m = re.match('.*\sof\s(\w+)$', text)
                    if m:
                        print(text)
                        print(m.group(1))
                        pass
                    pass
                pass
            pass
        # whether + ly
        for i in range(len(wiki)):
            if not ('etymology' in wiki[i]):
                continue
            text = wiki[i]['etymology']
            m = match(text, etymology_patterns)
            if m:
                toMap[qs.word] = m.group(1)
                print('etymology: ' + qs.word)
                continue
        pass

    for keyword in toDelete:
        Dict.objects.filter(word = keyword).delete()

    for keyword in toMap:
        if len(Dict.objects.filter(word = keyword)) >= 1 :
            if len(Dict.objects.filter(word = toMap[keyword])) >= 1 :
                Dict.objects.filter(word = keyword).delete()
                map = DictMap()
                map.word = keyword
                map.origin = toMap[keyword]
                map.save()
                pass
        pass

if __name__ == '__main__':
    main('s')
    # for x in ['u', 'v', 'w', 'x', 'y', 'z']:
    # for x in ['o', 'p', 'q', 'r', 's', 't']:
    # for x in ['h', 'i', 'j', 'k', 'l', 'm', 'n']:
    # for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        # main(x)

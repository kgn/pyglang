'''
Translate text with the 'Google AJAX Language API'
http://code.google.com/apis/ajaxlanguage/documentation/
'''

from __future__ import with_statement

__all__ = [
    'TranslationError',
    'GetLanguages',
    'GetLanguageCode',
    'Detect',
    'Translate',
]

import os
import urllib
try:
    #python2.6+
    import json
except ImportError:
    #python2.5
    import simplejson as json

k_apiVersion      = '1.0'
k_baseUrl         = 'http://ajax.googleapis.com/ajax/services/language'
k_htmlCodes = (
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    ("'", '&#39;'),
    #this has to be last
    ('&', '&amp;'),
)

class TranslationError(Exception):
    pass

g_languages = None
def GetLanguages():
    '''
    Load the languages dictionary from the Languages.json file.
    The dictionary is cached so the file is only read 
    the first time the data is requested.
    '''
    global g_languages
    if not g_languages:
        with open(os.path.join(os.path.dirname(__file__), 'Languages.json')) as languagesFile:
            g_languages = json.load(languagesFile)
    return g_languages

def GetLanguageCode(language):
    '''Given a language name return the language code'''
    if not language:
        return ''
    languageKey = language.strip().lower().replace(' ', '_')
    return GetLanguages().get(languageKey, language)

def Detect(text):
    '''
    Use the google language api to detect the language of the given text.

    Example url:    
    http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=hello
    '''
    #TODO: currently the detect call returns a 405 error...
    return _GetData(text, 'detect')
    
def Translate(text, **options):
    '''
    Use the google language api to translate the given text from one language to another.
    English is the default 'translate to' language, 
    if no 'from language' is given google will guess what the language is.
    
    Example url:
    http://ajax.googleapis.com/ajax/services/language/translate?langpair=en|ru&q=hello&v=1.0
    '''

    params = {
        'langpair' : '%s|%s' % (
            GetLanguageCode(options.get('fromLang', '')),
            GetLanguageCode(options.get('toLang', 'en')),
        ),
    }
    
    #call the google api
    return _GetData(text, 'translate', params, **options)

def _Unescape(s):
    '''Unescape html safe characters'''
    if not s:
        return u''

    for replace, search in k_htmlCodes:
        s = s.replace(search, replace)
    return s

def _GetData(text, urlType, params=None, **options):
    '''Make the calls to the Google Language API and return the resutling data'''
    
    if not text:
        return u''

    params = params or {}
    fullUrl = '%s/%s' % (k_baseUrl.rstrip('/'), urlType)
    
    params['v'] = k_apiVersion
    
    #try to encode the text 
    try:
        params['q'] = text.encode('utf_8')
    except UnicodeDecodeError:
        params['q'] = text

    #get the translated text from google
    if urlType == 'detect':
        #for some reason passing the params to data does not work for detect...
        result = urllib.urlopen('%s?%s' % (fullUrl, urllib.urlencode(params)))
    else:
        result = urllib.urlopen(fullUrl, data=urllib.urlencode(params))
    jsonData = json.load(result)
    responseData = jsonData.get('responseData')
    if not responseData:
        raise TranslationError(jsonData['responseDetails'])
    else:
        if urlType == 'translate':
            return _Unescape(responseData.get('translatedText'))
        elif urlType == 'detect':
            return _Unescape(responseData.get('language'))
    return u''

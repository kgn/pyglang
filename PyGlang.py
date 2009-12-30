'''
Translate text with the 'Google AJAX Language API'
http://code.google.com/apis/ajaxlanguage/documentation/
'''

import os
import urllib
try:
    #python2.6+
    import json
except ImportError:
    #python2.5
    import simplejson as json

apiVersion      = '1.0'
baseUrl         = 'http://ajax.googleapis.com/ajax/services/language'

class TranslationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

def unescape(s):
    '''Unescape html safe characters'''
    htmlCodes = (
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
        #this has to be last
        ('&', '&amp;'),
    )

    for eachItem in htmlCodes:
        s = s.replace(eachItem[1], eachItem[0])
    return s

languages = None
def getLanguages():
    '''
    Load the languages dictionary from the Languages.json file.
    The dictionary is cached so the file is only read 
    the first time the data is requested.
    '''
    global languages
    if languages == None:
        languagesFile = open(os.path.join(os.path.dirname(__file__), 'Languages.json'))
        languages = json.load(languagesFile)
        languagesFile.close()
    return languages

def getLanguageCode(language):
    '''Given a language name return the language code'''
    languageKey = language.lower()
    if languageKey in getLanguages():
        return getLanguages()[languageKey]
    return language

def getData(text, urlType, params=None, **options):
    '''Make the calls to the Google Language API and return the resutling data'''
    
    if len(text) == 0:
        return u''
    
    fullUrl = baseUrl
    if not(fullUrl.endswith('/')):
        fullUrl += '/'
    fullUrl += urlType
    
    if params == None:
        params = {}
    
    params['v'] = apiVersion
    
    #try to encode the text 
    try:
        params['q'] = text.encode('utf_8')
    except UnicodeDecodeError:
        params['q'] = text
    
    #get the translated text from google
    jsonData = json.load(urllib.urlopen(fullUrl, data=urllib.urlencode(params)))
    responseData = jsonData['responseData']
    if responseData == None:
        raise TranslationError(jsonData['responseDetails'])
    else:
        if urlType == 'translate' and responseData['translatedText'] != None:
            return unescape(responseData['translatedText'])
        elif urlType == 'detect' and responseData['language'] != None:
            return unescape(responseData['language'])
    return u''

def detect(text):
    '''
    Use the google language api to detect the language of the given text.
    
    http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=hello
    '''
    #TODO: currently the detect call returns a 405 error...
    return getData(text, 'detect')
    
def translate(text, **options):
    '''
    Use the google language api to translate the given text from one language to another.
    English is the default 'translate to' language, 
    if no 'from language' is given google will guess what the language is.
    
    Example url:
    http://ajax.googleapis.com/ajax/services/language/translate?langpair=en|ru&q=hello&v=1.0
    '''
    
    defaultToLang   = 'en'
    defaultFromLang = ''

    #parse options
    def getToLang():
        if 'toLang' in options:
            if options['toLang'] == None or options['toLang'] == '':
                return defaultToLang
            return getLanguageCode(options['toLang'])
        return defaultToLang
            
    def getFromLang():
        if 'fromLang' in options:
            if options['fromLang'] == None or options['fromLang'].lower() == 'unknown':
                return defaultFromLang
            return getLanguageCode(options['fromLang'])
        return defaultFromLang
    
    #setup parameters 
    params = {}
    params['langpair']  = '%s|%s' % (getFromLang(), getToLang())
    
    #call the google api
    return getData(text, 'translate', params, **options)

'''
Translate text with the 'Google AJAX Language API'
http://code.google.com/apis/ajaxlanguage/documentation/
'''

import urllib
try:
    #python2.6+
    import json
except ImportError:
    #python2.5
    import simplejson as json

apiVersion  = '1.0'
baseUrl     = 'http://ajax.googleapis.com/ajax/services/language/translate'

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

#TODO: add language enum
#TODO: add detect function

def translate(text, **options):
    '''
    Use the google language api to translate the given text from one language to another.
    English is the default 'translate to' language, 
    if no 'from language' is given google will guess what the language is.
    
    Example url:
    http://ajax.googleapis.com/ajax/services/language/translate?langpair=en|ru&q=hello&v=1.0
    '''
    fromLang=None
    toLang='en'
    inputType = 'text'
    textEncode = 'utf_8'
    
    if 'fromLang' in options:
        fromLang = options['fromLang']
        
    if 'toLang' in options:
        toLang = options['toLang']
     
    if 'encoding' in options:
        textEncode = options['encoding']
        
    if 'inputType' in options and options['inputType'] == 'html':
        inputType = 'html'
    
    #if there is nothing to translate or no language to tranlate to reutrn an empty unicode string
    if len(text) == 0 or len(toLang) == 0:
        return u''
        
    if fromLang == None:
        fromLang = ''
    
    #setup the arguments for the url   
    params = {}
    params['langpair']  = '%s|%s' % (fromLang, toLang)
    params['v']         = apiVersion
    
    #try to encode the text as utf-8
    try:
        params['q'] = text.encode(textEncode)
    except UnicodeDecodeError:
        params['q'] = text
    
    #get the translated text from google
    jsonData = json.load(urllib.urlopen(baseUrl, data=urllib.urlencode(params)))
    responseData = jsonData['responseData']
    if responseData == None:
        raise TranslationError(jsonData['responseDetails'])
    else:
        if responseData['translatedText'] != None:
            return unescape(responseData['translatedText'])
            
    return u''

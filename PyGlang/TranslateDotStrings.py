'''
Translate a .strings file from one language to another.
'''

from __future__ import with_statement

import re, sys, time
import codecs, locale
import PyGlang

k_langPathRegEx = re.compile('.*/([^\.]+)\.lproj.+$')
k_valueRegEx = re.compile('"([^"]*)"(\s*=\s*)"([^"]*)";', re.UNICODE)

def DetectEncoding(filepath):
    '''
    Try to detect the file's encoding.
    If its not utf-16 assume it's utf-8, this should work for ascii
    files becuase the first 128 characters are the same...
    '''
    
    with open(filepath, 'r') as f:
        firstBytes = f.read(2)

        if firstBytes == codecs.BOM_UTF16_BE:
            return 'utf_16_be'
        elif firstBytes == codecs.BOM_UTF16_LE:
            return 'utf_16_le'

    #use sig just encase there is a BOM in the file
    return 'utf_8_sig'

def LangFromPath(filepath):
    '''Get the languages from a filepath'''
    pathMatch = k_langPathRegEx.match(filepath)
    if pathMatch:
        return pathMatch.group(1)
    
def Translate(fromFilepath, toFilepath, utf8=False):
    '''
    Read a .strings file and localize it for the language of another .strings file.
    The language of each file is determined by the what 'lproj' directory they reside in.
    '''
    
    #detect encoding of output for printing
    language, output_encoding = locale.getdefaultlocale()
    
    #detect the encodeing of the file
    fromFileEncoding = 'utf_8' if utf8 else DetectEncoding(fromFilepath)
    
    #get the languages
    fromLang = LangFromPath(fromFilepath)
    toLang = LangFromPath(toFilepath)
    
    #regular expression
    def transValue(regExMatch):
        value = regExMatch.group(3)
        transText = PyGlang.Translate(value, fromLang=fromLang, toLang=toLang, encoding=fromFileEncoding)
        #TODO: only write this in command line mode
        print '%s > %s' % (value.encode(output_encoding), transText.encode(output_encoding))
        return '"%s"%s"%s";' % (regExMatch.group(1), regExMatch.group(2), transText)
    
    #read the file
    with codecs.open(fromFilepath, 'r', fromFileEncoding) as fromFile:
        with codecs.open(toFilepath, 'w', fromFileEncoding) as toFile:
            for eachLine in fromFile:
                toFile.write(k_valueRegEx.sub(transValue, eachLine))
   
if __name__ == '__main__':
    #TODO: add more robust options
    startTime = time.time()
    Translate(sys.argv[1], sys.argv[2], True)
    print 'Translated in %.2f seconds' % (time.time()-startTime)

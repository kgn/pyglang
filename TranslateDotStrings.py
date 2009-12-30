'''
Translate a .strings file from one language to another.
'''

import re, sys, time
import codecs, locale
import PyGlang

def detectEncoding(filepath):
    '''
    Try to detect the file's encoding.
    If its not utf-16 assume it's utf-8, this should work for ascii
    files becuase the first 128 characters are the same...
    '''
    
    f = open(filepath, 'r')
    firstBytes = f.read(2)
    f.close()
    
    if firstBytes == codecs.BOM_UTF16_BE:
        return 'utf_16_be'
    elif firstBytes == codecs.BOM_UTF16_LE:
        return 'utf_16_le'
    #use sig just encase there is a BOM in the file
    return 'utf_8_sig'

def langFromPath(filepath):
    '''Get the languages from a filepath'''
    pathMatch = re.match('.*/([^\.]+)\.lproj.+$', filepath)
    if pathMatch:
        return pathMatch.group(1)
    return None
    
def translate(fromFilepath, toFilepath):
    '''Read a .strings file and localize it for the language of another .strings file'''
    
    #detect encoding of output for printing
    language, output_encoding = locale.getdefaultlocale()
    
    #detect the encodeing of the file
    fromFileEncoding = detectEncoding(fromFilepath)
    
    #get the languages
    fromLang = langFromPath(fromFilepath)
    toLang = langFromPath(toFilepath)
    
    #regular expression
    valueRegEx = re.compile('"([^"]*)"(\s*=\s*)"([^"]*)";', re.UNICODE)
    def transValue(regExMatch):
        value = regExMatch.group(3)
        transText = PyGlang.translate(value, fromLang=fromLang, toLang=toLang, encoding=fromFileEncoding)
        #TODO: only write this in command line mode
        print '%s > %s' % (value.encode(output_encoding), transText.encode(output_encoding))
        return '"%s"%s"%s";' % (regExMatch.group(1), regExMatch.group(2), transText)
    
    #read the file
    fromFile = codecs.open(fromFilepath, 'r', fromFileEncoding)
    toFile = codecs.open(toFilepath, 'w', fromFileEncoding)
    for eachLine in fromFile:
        toFile.write(valueRegEx.sub(transValue, eachLine))
    
    toFile.close()            
    fromFile.close()
   
if __name__ == '__main__':
    startTime = time.time()
    translate(sys.argv[1], sys.argv[2])
    print 'Translated in %.2f seconds' % (time.time()-startTime)

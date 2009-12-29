'''
Translate a .strings file from one language to another.
'''

import sys, re, time
import codecs, locale
import PyGlang
from optparse import OptionParser

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

def writeToStdout(value):
    sys.stdout.write(value+'\n')

def writeToStderr(value):
    sys.stderr.write(value)

def translate(filepath, toLang, fromLang=None):
    '''Read a .strings file and localize it for another language'''
    
    #detect encoding of output for printing
    language, output_encoding = locale.getdefaultlocale()
    
    #detect the encodeing of the file
    fromFileEncoding = detectEncoding(filepath)
    
    #regular expression
    valueRegEx = re.compile('"([^"]*)"(\s*=\s*)"([^"]*)";', re.UNICODE)
    def transValue(regExMatch):
        value = regExMatch.group(3)
        transText = PyGlang.translate(value, fromLang=fromLang, toLang=toLang, encoding=fromFileEncoding)
        #TODO: only write this in command line mode
        writeToStdout('%s > %s' % (value.encode(output_encoding), transText.encode(output_encoding)))
        return '"%s"%s"%s";' % (regExMatch.group(1), regExMatch.group(2), transText)
    
    #read the file
    fromFile = codecs.open(filepath, 'r', fromFileEncoding)
    #TODO: if fromLang  is None detect the language from the filepath, 
    #and write the file to the correct language path
    toFile = codecs.open(filepath+'.tmp', 'w', fromFileEncoding)
    for eachLine in fromFile:
        toFile.write(valueRegEx.sub(transValue, eachLine))
    
    toFile.close()            
    fromFile.close()
   
if __name__ == '__main__':
    '''Command line options'''
    
    opts = OptionParser()
    opts.add_option('--fromLang', '-f', dest='fromLang', help='the language to convert from', metavar='LANG')
    opts.add_option('--toLang', '-t', dest='toLang', help='the language to convert to', metavar='LANG')
    options, arguments = opts.parse_args()
    
    if len(arguments) == 0:
        writeToStderr('no filepath provided\n')
    
    else:
        startTime = time.time()
        translate(arguments[0], options.toLang, options.fromLang)
        writeToStdout('Translated in %.2f seconds' % (time.time()-startTime))

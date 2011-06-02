Willkommen - Üdvözlöm - ยินดีต้อนรับ
========

Welcome to PyGlang, a python package for translating text with the [Google Translation API](http://code.google.com/apis/ajaxlanguage/documentation/)!

How to say 'Hello'
--------

    import PyGlang
    
    for language in PyGlang.GetLanguages().iterkeys():
        try:
            print language, PyGlang.Translate('Hello', fromLang='English', toLang=language)
         except PyGlang.TranslationError:
            print ''

By David Keegan <contact@inscopeapps.com>
With contributions from John Burnett

Documentation
========

PyGlang
--------

Translate text with the [Google AJAX Language API](http://code.google.com/apis/ajaxlanguage/documentation/)

`PyGlang.Translate(text[, fromLang[, toLang]])`

* Use the google language api to translate the given text from one language to another.
* English is the default 'translate to' language, if no 'from language' is given google will guess what the language is.
* Example url: http://ajax.googleapis.com/ajax/services/language/translate?langpair=en|ru&q=hello&v=1.0
* **text** the text to translate
* **fromLang** the language to translate from
* **toLang** the language to translate to

`PyGlang.Detect(text)`

* Use the google language api to detect the language of the given text.
* Example url: http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=hello
* **text** the text to detect the language of

`PyGlang.GetLanguageCode(language)`

* Given a language name return the language code
* **language** the language name

`PyGlang.GetLanguages()`

* A dictionary of supported languages, where the language name is the key, and the language code is the value.
* This dictionary comes from the Languages.json file, but it is cached so the file is only read once.

TranslateDotStrings
--------

Translate a .strings file from one language to another.

This script is designed to be a command line tool, the user passes in two .strings files. The first is the file to read and translate, and the second is the file to write to.

`python TranslateDotStrings.py fromFilepath toFilepath`

`TranslateDotStrings.Translate(fromFilepath, toFilepath)`

* Read a .strings file and localize it for the language of another .strings file.
* The language of each file is determined by the what 'lproj' directory they reside in.
* **fromFilepath** the file path of the .strings file to read and translate
* **toFilepath** the file path of the .strings file to write

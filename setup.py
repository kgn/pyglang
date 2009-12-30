from distutils.core import setup

name = 'PyGlang'
description = "Translate text with the 'Google AJAX Language API'"
author = 'David Keegan'
author_email = 'keegan3d@gmail.com'

setup(name=name,
    version='1.0',
    description=description,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    url='http://bitbucket.org/keegan3d/pyglang/',
    download_url='http://bitbucket.org/keegan3d/pyglang/downloads/',
    license='MIT - See LICENSE file',
    keywords=['google','api', 'language', 'translate'],
    platforms=['Independant'],  
    long_description=description,
    packages = [name],
    package_data={name:['Languages.json']},
    )
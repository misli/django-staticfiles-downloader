-----------------------------
django-staticfiles-downloader
-----------------------------

``django-staticfiles-downloader`` provides ``staticfiles_downloader.DownloaderFinder``,
an extension of ``django.contrib.staticfiles``, which allows you to specify static files
with urls and optionaly checksum in your Django application or Django project settings.
This is particularly useful, when using third-party static files, if you don't want to
either include the files in your project nor depend on CDN in runtime.

The static files are collected with ``python manage.py collectstatic``.

Installation
------------

.. code-block:: bash

    pip install  django-staticfiles-downloader


Configuration
-------------

Add ``staticfiles_downloader.DownloaderFinder`` to ``settings.STATICFILES_FINDERS``:

.. code-block:: python

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'staticfiles_downloader.DownloaderFinder',
    ]

Define static files urls in your Django application
...................................................

.. code-block:: python

    # your_app/__init__.py
    staticfiles_urls = {
        # use only url
        'my_app/js/jquery-3.2.1.min.js': 'https://code.jquery.com/jquery-3.2.1.min.js',
        # or use url and checksum
        'my_app/js/jquery-2.2.4.min.js': (
            'https://code.jquery.com/jquery-2.2.4.min.js',
            'sha384',
            'rY/jv8mMhqDabXSo+UCggqKtdmBfd3qC2/KvyTDNQ6PcUJXaxK1tMepoQda4g5vB',
        ),
    }

Define static files urls in your Django project settings
........................................................

.. code-block:: python

    # your_project/settings.py
    STATICFILES_URLS = {
        # use only url
        'js/jquery-3.2.1.min.js': 'https://code.jquery.com/jquery-3.2.1.min.js',
        # or use url and checksum
        'js/jquery-2.2.4.min.js': (
            'https://code.jquery.com/jquery-2.2.4.min.js',
            'sha384',
            'rY/jv8mMhqDabXSo+UCggqKtdmBfd3qC2/KvyTDNQ6PcUJXaxK1tMepoQda4g5vB',
        ),
    }

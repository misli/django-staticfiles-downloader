import base64
import hashlib
import os
from collections import defaultdict
from datetime import datetime
from urllib.request import Request, urlopen

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from django.utils.http import parse_http_date
from django.utils.timezone import now
from pytz import UTC


class GetRequest(Request):
    def __init__(self, url, **kwargs):
        kwargs.setdefault("headers", dict()).setdefault(
            "User-Agent",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
        )
        super().__init__(url, **kwargs)


class HeadRequest(GetRequest):
    def get_method(self):
        return "HEAD"


class DownloaderStorage(Storage):
    def __init__(self, url, algorithm, checksum):
        self.url, self.algorithm, self.checksum = url, algorithm, checksum
        self.request, self.hash = None, None

    def path(self, name):
        """
        Returns a local filesystem path where the file can be retrieved using
        Python's built-in open() function. Storage systems that can't be
        accessed using open() should *not* implement this method.
        """
        return self.url

    def open(self, name, mode="rb"):
        """
        Retrieves the specified file from storage.
        """
        self.request = urlopen(GetRequest(self.url))
        if self.algorithm:
            self.hash = hashlib.new(self.algorithm)
        return self

    def chunks(self, chunk_size=None):
        while True:
            chunk = self.read(chunk_size)
            yield chunk
            if not chunk:
                break

    def read(self, length=None):
        chunk = self.request.read(length)
        if self.hash:
            self.hash.update(chunk)
        return chunk

    def close(self):
        self.request.close()
        if self.hash:
            checksum = base64.encodebytes(self.hash.digest()).decode()
            if checksum.strip() != self.checksum:
                raise RuntimeError(
                    'Checksum {} of {} does not match: expected "{}", got "{}"'.format(
                        self.algorithm, self.url, self.checksum, checksum
                    )
                )

    def get_modified_time(self, path):
        response = None
        try:
            response = urlopen(HeadRequest(self.url))
            last_modified = response.headers["Last-Modified"]
            return datetime.fromtimestamp(parse_http_date(last_modified), UTC)
        except Exception:
            return now()
        finally:
            if response:
                response.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class DownloaderFinder(BaseFinder):
    """
    A static files finder that uses the ``app.staticfiles_urls`` to download
    files.
    """

    storage_class = DownloaderStorage
    urls_attr = "staticfiles_urls"

    def __init__(self, app_names=None, *args, **kwargs):
        # The list of apps that are handled
        self.apps = []
        # Mapping of file paths to storage instances
        self.firsts = {}
        self.lists = defaultdict(list)
        # First try to load urls from settings
        staticfiles_urls = getattr(settings, "STATICFILES_URLS", {})
        if staticfiles_urls:
            self._load(
                staticfiles_urls,
                "settings.STATICFILES_URLS",
            )
        # Then try to load staticfiles_urls from installed apps
        app_configs = apps.get_app_configs()
        if app_names:
            app_names = set(app_names)
            app_configs = [ac for ac in app_configs if ac.name in app_names]
        for app_config in app_configs:
            staticfiles_urls = getattr(app_config.module, self.urls_attr, None)
            if staticfiles_urls:
                self._load(
                    staticfiles_urls,
                    ".".join([app_config.name, self.urls_attr]),
                )
        super(DownloaderFinder, self).__init__(*args, **kwargs)

    def _load(self, staticfiles_urls, variable_name):
        if not isinstance(staticfiles_urls, dict):
            raise ImproperlyConfigured(
                'Value of "{}" is not a dict.'.format(variable_name)
            )
        for path, url in staticfiles_urls.items():
            if isinstance(url, (list, tuple)):
                try:
                    url, algorithm, checksum = url
                except ValueError:
                    raise ImproperlyConfigured(
                        'Values of "{}" must be string '
                        "urls or tuples (url, algorithm, checksum).".format(
                            variable_name
                        )
                    )
                if algorithm not in hashlib.algorithms_available:
                    raise ImproperlyConfigured(
                        'The algorythm "{}" is not available.'.format(algorithm)
                    )
            else:
                algorithm, checksum = None, None
            if path not in self.firsts:
                self.firsts[path] = self.storage_class(url, algorithm, checksum)
                self.lists[path].append(url)

    def list(self, ignore_patterns):
        """
        List all files in all storages.
        """
        return self.firsts.items()

    def find(self, path, all=False):
        """
        Looks for files in the app directories.
        """
        found = os.path.join(settings.STATIC_ROOT, path)
        if all:
            return [found]
        else:
            return found

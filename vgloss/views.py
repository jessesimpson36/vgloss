import os
import posixpath
import mimetypes
from functools import lru_cache

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse

DIST_DIR = os.path.join(settings.VGLOSS_CODE_DIR, "dist")

@lru_cache()
def read_dist_file(path):
    path = posixpath.normpath(path).lstrip("/")
    abspath = os.path.abspath(os.path.join(DIST_DIR, path))

    if os.path.commonpath([abspath, DIST_DIR]) != DIST_DIR:
        # abspath must be within DIST_DIR
        return None, None, None
    if not os.path.exists(abspath) or os.path.isdir(abspath):
        return None, None, None

    content_type, encoding = mimetypes.guess_type(abspath)
    content_type = content_type or 'application/octet-stream'
    is_bin = content_type.startswith("image/")
    content = open(abspath, "rb" if is_bin else "r").read()
    return content, content_type, encoding

class GalleryView(View):

    def get(self, request, *args, **kwargs):
        content, content_type, encoding = read_dist_file(request.path)
        if not content:
            # Fallback to serving index.html
            content, content_type, encoding = read_dist_file("index.html")
        if not content:
            raise ValueError("Compiled javascript not found. Please run `yarn build`")

        #TODO: This view should do some things that django.views.static.serve
        #      does. Namely:
        #      * Respect HTTP_IF_MODIFIED_SINCE header
        #      * Send Last-Modified header

        response = HttpResponse(
            content=content,
            content_type=content_type,
        )
        if encoding:
            response["Content-Encoding"] = encoding
        return response
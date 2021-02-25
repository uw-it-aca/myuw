import json
import os

from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.cache import cache
from django.utils.safestring import mark_safe

CACHE_TAG = 'webpack_manifest.entrys.{}'
LOADER_SETTINGS = {
    'manifest_file': 'manifest.json',
    'cache': not settings.DEBUG,
    'cache_timeout': 86400,  # 1 Day
}
EXTENSIONS_GROUP = {
    ('js', ): 'script',
    ('css', ): 'style',
}
GROUP_TAG = {
    'script': '<script src="{path}" {attributes}></script>',
    'style':
        '<link rel="stylesheet" type="text/css" href="{path}" {attributes}>',
}

register = template.Library()

if hasattr(settings, 'WEBPACK_MANIFEST_LOADER'):
    LOADER_SETTINGS.update(settings.WEBPACK_MANIFEST_LOADER)


class WebpackManifestNotFound(Exception):
    def __init__(self, name, path):
        message = 'Manifest file with name ({}) not found in {}'
        super().__init__(message.format(name, path))


class WebpackEntryNotFound(Exception):
    def __init__(self, entry):
        message = 'Webpack entry with name {} not found in manifest.'
        super().__init__(message.format(entry))


class FileExtensionHasNoMapping(Exception):
    def __init__(self, ext):
        message = 'File extension has not mapping {}, available mappings {}'
        super().__init__(message.format(ext, EXTENSIONS_GROUP))


def find_manifest_path():
    for static_dir in settings.STATICFILES_DIRS:
        manifest_path = os.path.join(
            static_dir, LOADER_SETTINGS['manifest_file']
        )
        if os.path.isfile(manifest_path):
            return manifest_path

    raise WebpackManifestNotFound(
        LOADER_SETTINGS['manifest_file'],
        settings.STATICFILES_DIRS
    )


def get_webpack_manifest():
    try:
        with open(find_manifest_path()) as manifest_file:
            manifest_data = json.load(manifest_file)
            return manifest_data
    except FileNotFoundError:
        raise WebpackManifestNotFound(
            LOADER_SETTINGS['manifest_file'],
            settings.STATICFILES_DIRS
        )


# @register.simple_tag
def render_webpack_entry(entry, **tag_attrs):
    entry_bundles = None
    if LOADER_SETTINGS['cache']:
        entry_bundles = cache.get(CACHE_TAG.format(entry))

    if entry_bundles is None:
        entry_bundles = []
        webpack_manifest = get_webpack_manifest()

        if entry not in webpack_manifest['entries']:
            raise WebpackEntryNotFound(entry)

        for bundle_name in webpack_manifest['entries'][entry]:
            bundle_path = webpack_manifest['bundles'][bundle_name]
            bundle_ext = os.path.splitext(bundle_path)[1][1:]

            html_tag = None
            for group in EXTENSIONS_GROUP:
                if bundle_ext in group:
                    html_tag = GROUP_TAG[EXTENSIONS_GROUP[group]]
                    break
            if html_tag is None:
                raise FileExtensionHasNoMapping(bundle_ext)

            entry_bundles.append((
                bundle_ext,
                html_tag.format(
                    path=static(bundle_path),
                    attributes='{attributes}'
                ),
            ))

        if LOADER_SETTINGS['cache']:
            cache.set(
                CACHE_TAG.format(entry),
                entry_bundles,
                timeout=LOADER_SETTINGS['cache_timeout']
            )

    parsed_html = ""
    for entry_bundle in entry_bundles:
        if entry_bundle[0] in tag_attrs:
            bundle_html = entry_bundle[1].format(
                attributes=tag_attrs[entry_bundle[0]]
            )
        else:
            bundle_html = entry_bundle[1].format(attributes="")
        parsed_html += bundle_html + '\n'

    return mark_safe(parsed_html)

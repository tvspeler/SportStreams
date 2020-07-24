from __future__ import unicode_literals

import re

from .common import InfoExtractor


class WayOfTheMainIE(InfoExtractor):
    _VALID_URL = r'https?://www\.wayofthemain\.com/([^/?#]*/)*(?P<id>[^/?#]+)\.s?html(?:$|[?#])'

    _TEST = {
        'url': 'http://www.wayofthemain.com/hbks.shtml',
        'md5': '5316b57487ada8480606a93cb3d18d24',
        'info_dict': {
            'id': 'hbks',
            'ext': 'mp4',
            'title': 'Intelligent Design vs. Evolution',
        },
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        webpage = self._download_webpage(url, video_id)

        title = self._search_regex(
            r'<img src="images/title_[^"]+".*?alt="([^"]+)"',
            webpage, 'title', default=None)
        if title is None:
            title = self._html_search_regex(
                r'<title>(.*?)</title>', webpage, 'page title')

        url_base = self._search_regex(
            r'<param\s+name="?movie"?\s+value=".*?/wotm_videoplayer_highlow[0-9]*\.swf\?vid=([^"]+)"',
            webpage, 'URL base')
        formats = [{
            'format_id': 'low',
            'quality': 1,
            'url': url_base + '_low.mp4',
        }, {
            'format_id': 'high',
            'quality': 2,
            'url': url_base + '_high.mp4',
        }]
        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
        }

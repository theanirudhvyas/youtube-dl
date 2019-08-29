from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    parse_duration
)


class YourPornIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?sxyprn\.com/post/(?P<id>[^/?#&.]+)'
    _TESTS = [{
        'url': 'https://sxyprn.com/post/57ffcb2e1179b.html',
        'md5': '6f8682b6464033d87acaa7a8ff0c092e',
        'info_dict': {
            'id': '57ffcb2e1179b',
            'ext': 'mp4',
            'title': 'md5:c9f43630bd968267672651ba905a7d35',
            'thumbnail': r're:^https?://.*\.jpg$',
            'duration': 165,
            'age_limit': 18,
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://sxyprn.com/post/57ffcb2e1179b.html',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        url_parts = self._parse_json(self._search_regex(
            r'data-vnfo=(["\'])(?P<data>{.+?})\1', webpage, 'data info', group='data'), video_id)[video_id].split("/")

        aid = self._search_regex(r'data-aid=\'(.*?)\'', webpage, 'aid')

        video_url = 'https://' + url_parts[2] + '.trafficdeposit.com/video/' + url_parts[3] + '/' + url_parts[
            4] + '/' + url_parts[5] + '/' + aid + '/' + video_id + '.mp4'

        title = (self._search_regex(
            r'<[^>]+\bclass=["\']PostEditTA[^>]+>([^<]+)', webpage, 'title',
            default=None) or self._og_search_description(webpage)).strip()
        thumbnail = self._og_search_thumbnail(webpage)
        duration = parse_duration(self._search_regex(
            r'duration\s*:\s*<[^>]+>([\d:]+)', webpage, 'duration',
            default=None))

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'age_limit': 18,
        }

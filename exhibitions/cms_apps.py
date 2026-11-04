from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class ExhibitionsApphook(CMSApp):
    name = 'Exhibitions'
    app_name = 'exhibitions'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['exhibitions.urls']


@apphook_pool.register
class ArtistsApphook(CMSApp):
    name = 'Artists'
    app_name = 'artists'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['exhibitions.artist_urls']
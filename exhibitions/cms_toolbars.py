from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


@toolbar_pool.register
class ItemsToolbar(CMSToolbar):
    def populate(self):
        if not self.request.user.is_staff:
            return

        menu = self.toolbar.get_or_create_menu("items-menu", _("Items"))
        menu.add_sideframe_item(_("Projects"), url=reverse("admin:exhibitions_project_changelist"))
        menu.add_modal_item(
            _("Add project"),
            url=f"{reverse('admin:exhibitions_project_add')}?cms_modal=1",
        )
        menu.add_break()
        menu.add_link_item(_("Artists"), url=reverse("admin:exhibitions_artist_changelist"))
        menu.add_modal_item(
            _("Add artist"),
            url=f"{reverse('admin:exhibitions_artist_add')}?cms_modal=1",
        )
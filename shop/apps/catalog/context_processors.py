# coding: utf-8


from leon.base import BaseContextProcessor
from catalog.base import CatalogParamsValidatorMixin


class CategoryMenuContextProcessor(BaseContextProcessor, CatalogParamsValidatorMixin):
    """
    Class for block context processor menu
    """

    request_params_slots = {
        'catalog_slug_title': [None, '']
    }

    CATEGORY_SITE_MODEL = None

    def _create_data(self):
        self.menu_catalog_category_s = self.CATEGORY_SITE_MODEL.get_root_nodes()
        self.menu_catalog_current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        self.menu_catalog_parent_category = self.menu_catalog_current_category.get_parent()

        if not self.menu_catalog_parent_category:
            self.menu_catalog_parent_category = self.menu_catalog_current_category
            self.menu_catalog_parent_category.selected = True
        else:
            self.menu_catalog_parent_category.selected = False

    def _format(self):
        pass

    def __call__(self, request):
        self.main_menu = {}
        self.output_context = {
            'menu_catalog_category_s': None,
            'menu_catalog_current_category': None,
            'menu_catalog_parent_category': None
        }
        self._init(request)
        self._create_data()
        self._format()
        self._aggregate()
        return self.output_context


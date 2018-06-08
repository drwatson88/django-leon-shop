# About project

This library created from me for using in bulding some e-commerce sites with Django framework. Library has more effectively wrappers for smart using Django.


## Getting Started (Examples)
~~~
Creating Model for Catalog:

from shop_base.catalog.models import ShopProduct
class Product(ShopProduct):
    pass

Creating ContextProcessor for Catalog Product List:

from shop_base.catalog.context_processors import ShopCatalogFilterContextProcessor 
class CatalogFilterContextProcessor(ShopCatalogFilterContextProcessor):
    CATEGORY_SITE_MODEL = CategorySite
    PRODUCT_MODEL = Product
    ORDER_REFERENCE_MODEL = OrderReference
    
Creating View for Catalog Product List:

from shop_base.catalog.views import ShopProductListView
class ProductListView(ShopProductListView):
    context_processors = [CatalogFilterContextProcessor, CatalogBreadcrumbContextProcessor,
                          CatalogSidebarMenuContextProcessor]
    template_name = 'catalog/product_list.html'
    template_popup = {'grid': 'catalog/popup/product_list_grid.html',
                      'pagination': 'catalog/popup/product_list_pagination.html'}
    template_popup_change = {'grid': 'catalog/popup/product_list_grid.html',
                             'list': 'catalog/popup/product_list_list.html'}
    page_size = 21
    CATEGORY_SITE_MODEL = CategorySite
    PRODUCT_MODEL = Product
    ORDER_REFERENCE_MODEL = OrderReference
~~~ 

### Prerequisites

Python >= 3.5
Django >= 1.11


### Installing
~~~
pip install git+http://github.com/dvsidorov/django-leon-shop.git
~~~

### Building documentation
~~~
git clone http://github.com/dvsidorov/django-leon-shop.git djshop
cd ./djshop/docs/
make html
~~~

## Built With

* [Django](https://github.com/django/django.git) - The web framework used


## Authors

* **Denis Sidorov** - *Initial work* - [dvsidorov](https://github.com/dvsidorov)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

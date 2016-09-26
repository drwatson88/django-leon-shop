# coding: utf-8

import sys
import os
import argparse


CATEGORY_SITE_IMAGE = 'upload_category/demo/image.jpg'
PRODUCT_IMAGE = 'upload_product/demo/image.jpg'


def args():
    parser = argparse.ArgumentParser(description='Generate test '
                                                 'objects for catalog demo')
    parser.add_argument('PROJECT_PATH', nargs='+', help='PROJECT_PATH help')
    return parser.parse_args()


def main(project_dir):
    project_dir = project_dir or u'/'.join(os.getcwd().split(u'/')[:-3])
    sys.path.append(project_dir)
    sys.path.append(os.path.join(project_dir, u'apps'))
    os.environ[u'DJANGO_SETTINGS_MODULE'] = u'settings'

    import django
    django.setup()

    from mixer.backend.django import mixer, Mixer
    from catalog.models import Maker, BrandMaker, Brand, \
        PrintTypeMaker, PrintType, CategorySite, CategoryXML, \
        Product, ProductAttachment, ProductParamsOther, \
        ProductParamsPack, ProductParamsStock, \
        SubProduct, SubProductParamsOther, SubProductParamsStock, \
        Status, Settings, OrderReference

    # Generate a random maker
    maker_s = mixer.cycle(5).blend(Maker)

    # Generate a random status
    status_s = mixer.cycle(5).blend(Status)

    # Create filters
    i = 0
    for k, v in {'default': ['По умолчанию', 'title', 0, 0],
                 'NAZ': ['По названию (А-Я)', 'title', 0, 1],
                 'NZA': ['По названию (Я-А)', 'title', 1, 2]}.items():
        OrderReference(name=k, official=v[0], field_name=v[1],
                       field_order=v[2], position=v[3]).save()
        i += 1

    # Generate a random brand
    brand_s = mixer.cycle(5).blend(Brand)
    brand_maker_s = mixer.cycle(20).blend(BrandMaker,
                                          maker=mixer.SELECT,
                                          brand=(bm for bm in brand_s*4))

    # Generate a random print type
    print_type_s = mixer.cycle(5).blend(PrintType)
    print_type_maker_s = mixer.cycle(20).blend(PrintTypeMaker,
                                               maker=mixer.SELECT,
                                               print_type=(pt for pt in print_type_s*4))

    # Generate a random category site
    mixer = Mixer(commit=False)
    category_site_parent_s = mixer.cycle(5).blend(CategorySite)
    for cat_site_parent in category_site_parent_s:
        print(cat_site_parent.slug_title)
        cat_site_parent_obj = CategorySite.add_root(
            title=cat_site_parent.title,
            slug_title=cat_site_parent.slug_title,
            preview=cat_site_parent.preview,
            content=cat_site_parent.content,
            show=cat_site_parent.show,
            image=CATEGORY_SITE_IMAGE,
            position=cat_site_parent.position
        )
        cat_site_parent_obj.save()

        category_site_child_s = mixer.cycle(5).blend(CategorySite)
        for cat_site_child in category_site_child_s:
            cat_site_child_obj = cat_site_parent_obj.add_child(
                title=cat_site_child.title,
                slug_title=cat_site_child.slug_title,
                preview=cat_site_child.preview,
                content=cat_site_child.content,
                show=cat_site_child.show,
                image=CATEGORY_SITE_IMAGE,
                position=cat_site_child.position
            )
            cat_site_child_obj.save()

    # Generate a random category xml
    mixer = Mixer(commit=False)
    for maker in Maker.objects.all():
        category_xml_parent_s = mixer.cycle(5).blend(CategoryXML,
                                                     maker=maker,
                                                     category_site=(category_site for category_site
                                                                    in CategorySite.objects.filter(depth=1)),
                                                     cat_id=(i for i in range(1, 9))
                                                     )
        for cat_xml_parent in category_xml_parent_s:
            cat_xml_parent_obj = CategoryXML.add_root(
                maker=maker,
                title=cat_xml_parent.title,
                cat_id=cat_xml_parent.cat_id,
                category_site=cat_xml_parent.category_site,
                import_fl=1
            )
            cat_xml_parent_obj.save()

            category_xml_child_s = mixer.cycle(5).blend(CategoryXML,
                                                        maker=maker,
                                                        category_site=(category_site for category_site
                                                                       in CategorySite.objects.filter(depth=2)),
                                                        cat_id=(i for i in range(int(cat_xml_parent.cat_id) * 10,
                                                                                 int(cat_xml_parent.cat_id) * 10 + 10)))

            for cat_xml_child in category_xml_child_s:
                cat_xml_child_obj = cat_xml_parent_obj.add_child(
                    maker=maker,
                    title=cat_xml_child.title,
                    cat_id=cat_xml_child.cat_id,
                    category_site=cat_xml_child.category_site,
                    import_fl=1
                )
                cat_xml_child_obj.save()

    # Generate a random product
    mixer = Mixer(commit=True)
    for maker in Maker.objects.all():
        product_s = mixer.cycle(50).blend(Product,
                                          maker=maker,
                                          brand=(brand for brand in
                                                 list(BrandMaker.objects.
                                                      filter(maker=maker))*100),
                                          status=Status.objects.all()[0],
                                          small_image=PRODUCT_IMAGE,
                                          big_image=PRODUCT_IMAGE,
                                          super_big_image=PRODUCT_IMAGE,
                                          code=(str(x) for x in range(1000, 10000, 2)),
                                          category_xml=(cat_xml for cat_xml in
                                                        list(CategoryXML.objects.
                                                             filter(maker=maker))*100),
                                          print_type=(print_type for print_type in
                                                      list(PrintTypeMaker.objects.
                                                           filter(maker=maker))*100),
                                          import_fl=1)

        # Generate a random product attachment
        product_attachment_s = mixer.cycle(100).blend(ProductAttachment,
                                                      maker=maker,
                                                      product=(product for product in
                                                               list(Product.objects.
                                                                    filter(maker=maker).all())*2),
                                                      file=PRODUCT_IMAGE,
                                                      image=PRODUCT_IMAGE
                                                      )
        print(Product.objects.filter(maker=maker).all())

        # Generate a random product params pack
        product_params_pack_s = mixer.cycle(300).blend(ProductParamsPack,
                                                       maker=maker,
                                                       abbr=(item for product in
                                                             list(Product.objects.filter(maker=maker).all())
                                                             for item in
                                                             ['amount',
                                                              'weight',
                                                              'volume',
                                                              'sizex',
                                                              'sizey',
                                                              'sizez']),
                                                       product=(product for product in
                                                                list(Product.objects.filter(maker=maker).all())
                                                                for i in range(0, 6)),
                                                       pack_id=0)

        # Generate a random product params stock
        product_params_stock_s = mixer.cycle(250).blend(ProductParamsStock,
                                                        maker=maker,
                                                        abbr=(item for product in
                                                              list(Product.objects.filter(maker=maker).all())
                                                              for item in
                                                              ['amount',
                                                               'free',
                                                               'inwayamount',
                                                               'inwayfree',
                                                               'enduserprice']),
                                                        product=(product for product in
                                                                 list(Product.objects.filter(maker=maker).all())
                                                                 for i in range(0, 5)))

        # Generate a random product params other
        product_params_other_s = mixer.cycle(150).blend(ProductParamsOther,
                                                        maker=maker,
                                                        abbr=(item for product in
                                                              list(Product.objects.filter(maker=maker).all())
                                                              for item in
                                                              ['product_size',
                                                               'weight',
                                                               'matherial']),
                                                        product=(product for product in
                                                                 list(Product.objects.filter(maker=maker).all())
                                                                 for i in range(0, 3)))

        # Generate a random subproduct attachment
        subproduct_s = mixer.cycle(100).blend(SubProduct,
                                              maker=maker,
                                              code=(str(x) for x in range(1000, 10000, 2)),
                                              product=(product for product in
                                                       list(Product.objects.
                                                            filter(maker=maker).all())*2))

        # Generate a random subproduct params stock
        subproduct_params_stock_s = mixer.cycle(500).blend(SubProductParamsStock,
                                                           maker=maker,
                                                           abbr=(item for subproduct in
                                                                 list(SubProduct.objects.filter(maker=maker).all())
                                                                 for item in
                                                                 ['amount',
                                                                  'free',
                                                                  'inwayamount',
                                                                  'inwayfree',
                                                                  'enduserprice']),
                                                           sub_product=(subproduct for subproduct in
                                                                        list(SubProduct.objects.
                                                                             filter(maker=maker).all())
                                                                        for i in range(0, 5)))

        # Generate a random subproduct params other
        subproduct_params_other_s = mixer.cycle(200).blend(SubProductParamsOther,
                                                           maker=maker,
                                                           abbr=(item for subproduct in
                                                                 list(SubProduct.objects.filter(maker=maker).all())
                                                                 for item in
                                                                 ['size_code',
                                                                  'weight']),
                                                           sub_product=(subproduct for subproduct in
                                                                        list(SubProduct.objects.
                                                                             filter(maker=maker).all())
                                                                        for i in range(0, 2)))

    # Generate a random settings
    settings = mixer.blend(Settings)


if __name__ == '__main__':
    args = args()
    main(args.PROJECT_PATH[0])

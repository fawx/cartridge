from __future__ import unicode_literals

from datetime import datetime

from django.template.defaultfilters import slugify
from django.db.models import Q

from mezzanine.conf import settings
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.views import paginate

from cartridge.shop.models import Category, Product


@processor_for(Category, exact_page=False)
def category_processor(request, page):
    """
    Add paging/sorting to the products for the category.
    """
    settings.use_editable()
    products = Product.objects.published(for_user=request.user
                                ).filter(page.category.filters()).distinct()
    sort_options = [(slugify(option[0]), option[1])
                    for option in settings.SHOP_PRODUCT_SORT_OPTIONS]

    sort_by = request.GET.get("sort", sort_options[0][1])
    year = request.GET.get("year")
    make = request.GET.get("make")
    model = request.GET.get("model")
    engine = request.GET.get("engine")
    price = request.GET.get("price")

    filter_make = Q(productcompatibility__make__name__iexact=make) if make else Q()
    filter_year = Q(productcompatibility__years__contains=year) if year else Q()
    filter_model = Q(productcompatibility__model__name__iexact=model) if model else Q()
    filter_engine = Q(productcompatibility__engine__name__iexact=engine) if engine else Q()
    filter_price = ( Q(unit_price__range=price.split('-'), sale_price__isnull=True) | 
                    Q(sale_price__range=price.split('-')) ) if price else Q()

    filtered_products = products.filter(filter_make & filter_model & filter_engine & 
                                        filter_year & filter_price).order_by(sort_by)
    products = paginate(filtered_products,
                        request.GET.get("page", 1),
                        settings.SHOP_PER_PAGE_CATEGORY,
                        settings.MAX_PAGING_LINKS)

    products.sort_by = sort_by
    sub_categories = page.category.children.published()
    child_categories = Category.objects.filter(id__in=sub_categories)

    return { "products": products, 
            "child_categories": child_categories }

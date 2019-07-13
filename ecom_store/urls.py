from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.conf.urls.static import static

from product import views
from ecom_store import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('regack/', views.reg_ack, name='regack'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    url(r'^cate/(?P<prod_id>[0-9]+)', views.cate, name='cate'),
    url(r'^sprod/(?P<prod_id>[0-9]+)', views.sprod, name='sprod'),

    # ---------------- Provider ------------------

    path('prohome/', views.pro_home, name='pro_home'),
    path('proProduct/', views.pro_add_Product, name='pro_add_Product'),
    path('proreport/', views.pro_report, name='pro_report'),
    path('procate/', views.pro_add_cate, name='pro_add_cate'),
    path('uview/', views.ureg_view,name='ureg_view'),
    path('delete/', views.ureg_delete,name='ureg_delete'),

    # ---------------- Customer ------------------

    path('cart/', views.cart, name='cart'),
    path('cart0/', views.cart0, name='cart0'),
    path('orders/', views.orders, name='orders'),
    path('account/', views.account, name='account'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
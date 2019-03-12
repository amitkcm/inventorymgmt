"""inventorymgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from inventory.views import invRecordList, invLoginUserToken,invLoginUser,InventoryListView, InventoryDetailView, create_inventory,inventoryList
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'inv',inventoryList, basename='inv')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token/$', invLoginUserToken),
    url(r'^login/$', invLoginUser),
    url(r'^', include(router.urls)),
    url(r'^recordlist/$', invRecordList),
    # url(r'inventory/create/$',create_inventory, name='create'),
    url(r'^recordlist/(?P<pk>[\d]+)/$', InventoryDetailView.as_view(),name='detail'),
]

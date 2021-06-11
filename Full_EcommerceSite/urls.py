
from django.contrib import admin
from django.urls import path,include


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('App_shop.urls')),
    path('account/',include('user_login.urls')),
    path('order_shop/',include('App_Order.urls')),
    path('payment/',include('App_payment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

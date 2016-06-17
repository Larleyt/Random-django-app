from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import *

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='base.html'), name="landing"),
    # url(r'^$', 'altexo.views.landing', name="landing"),
    url('', include('lugati.apps_urls')),

    # url(r'^augmented/grigorev/$', 'altexo.views.main', name="main"),
    # url(r'^augmented/lushina/$', 'altexo.views.main', name="main"),
    # url(r'^augmented/$', 'altexo.views.main', name="main"),

    # url(r'^landing/$', 'altexo.views.landing', name="landing"),
    # url(r'^streams/$', 'altexo.views.streams', name="streams"),
    # url(r'^single_stream/$', 'altexo.views.single_stream', name="single_stream"),
    # url(r'^live_stream/$', 'altexo.views.live_stream', name="live_stream"),

    # url(r'^lugati/test/$', 'altexo.views.test', name="test"),
    url(r'^lugati/get_csrf/$', 'altexo.views.get_csrf', name="get_csrf"),
    # url(r'^features/$', 'altexo.views.features', name="features"),
    # url(r'^contact/$', 'altexo.views.contact', name="contact"),

    # API
    # url(r'^$', api_root),

    url(r'^users/auth/', include('djoser.urls.authtoken'), name='user-list'),

    url(r'^invoices/?$',
        InvoiceList.as_view(),
        name='invoice-list'),
    url(r'^invoices/(?P<pk>[0-9]+)/?$',
        InvoiceDetail.as_view(),
        name='invoice-detail'),

    url(r'^services/?$',
        ServiceList.as_view(),
        name='service-list'),
    url(r'^services/(?P<pk>[0-9]+)/?$',
        ServiceDetail.as_view(),
        name='service-detail'),

    url(r'^services/(?P<service_id>[0-9]+)/subscription/?$',
        SubscriptionCreate.as_view(),
        name='subscription-create'),
    url(r'^subscriptions/?$',
        SubscriptionList.as_view(),
        name='subscription-list'),
    url(r'^subscriptions/(?P<pk>[0-9]+)/?$',
        SubscriptionDetail.as_view(),
        name='subscription-detail'),
]

if 'altexo.altexo_streams' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^', include('altexo.altexo_streams.urls', namespace="altexo_streams")),
    ]

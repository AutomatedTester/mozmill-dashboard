from django.conf.urls.defaults import *


urlpatterns = patterns('display.views',
    url(r'^foo/$', 'top_fail', name='display.top_fail'),
    url(r'^report/(?P<_id>\w+)$', 'report', name='display.report'),
    url(r'^$', 'all_reports', name='display.all_reports'),

#    url(r'^api$', 'top_fail_json', name='display.top_fail_json'),
)

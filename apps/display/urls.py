from django.conf.urls.defaults import *


urlpatterns = patterns('display.views',
    url(r'^foo/$', 'top_fail', name='display.top_fail'),
    url(r'^report/(?P<_id>\w+)$', 'report', name='display.report'),
    url(r'^$', 'reporter', {'report_type':'all'}, name='display.all_reports'),
    url(r'^functional/$', 'reporter', {'report_type':'functional'}, name='display.functional'),
    url(r'^endurance/$', 'reporter', {'report_type':'endurance'}, name='display.endurance'),
    url(r'^update/$', 'reporter', {'report_type':'update'}, name='display.update'),


#    url(r'^api$', 'top_fail_json', name='display.top_fail_json'),
)

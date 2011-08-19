from django.conf.urls.defaults import *


urlpatterns = patterns('display.views',
    url(r'^foo/$', 'reporter', {'test_type':'all','top_fail_view':True},name='display.top_fail'),
    url(r'^$', 'reporter', {'test_type':'all'}, name='display.all_reports'),
    url(r'^functional/$', 'reporter', {'test_type':'functional'}, name='display.functional'),
    url(r'^endurance/$', 'reporter', {'test_type':'endurance'}, name='display.endurance'),
    url(r'^update/$', 'reporter', {'test_type':'update'}, name='display.update'),
#    url(r'^api$', 'top_fail_json', name='display.top_fail_json'),
)

urlpatterns += patterns('display.report.views',
    url(r'^report/(?P<_id>\w+)$', 'report', name='display.report'),
)


import jingo
import simplejson as json
from copy import deepcopy
from django import http
from django.http import HttpResponse, HttpResponseForbidden

from display.queries import reports, grab_facet_response, grab_operating_systems, grabber 
from display.report.utils import parse_results


def report(request,_id):
    report=grabber('',_id)
    report = report['_source']
    results = []
    data = {
        "id":_id,
        "app_name":report['application_name'],
        "app_version":report['application_version'],
        "platform_version":report['platform_version'],
        "app_locale":report['application_locale'],
        "platform_buildId":report['platform_buildid'],
        "system":report['system_info']['system'],
        "system_version":report['system_info']['version'],
        "service_pack":report['system_info']['service_pack'],
        "cpu":report['system_info']['processor'],
        "time_start":report['time_start'],
        "time_end":report['time_end'],
        "passed":report['tests_passed'],
        "failed":report['tests_failed'],
        "skipped":report['tests_skipped'],
        "report_type":report['report_type'],
        'results':[],
    }

    #Make sure that there are no stupid argument
    try:
        request.GET['status']
    except:
        pass
    else:
        if not request.GET['status'] in ['all','failed','passed','skipped']:
            return HttpResponseForbidden()

    data['results'] = parse_results(request,report['results'],)

    if data['report_type']=='firefox-functional':
        return jingo.render(request, 'display/report/functional.html', data)
    elif data['report_type']=='firefox-update':
        return update(request,data,report)
    else:
        return HttpResponse(data['report_type'])

def update(request,data,report):
    update=report['updates'][0]
    data['pre']={
        'user_agent':update['build_pre']['user_agent'],
        'locale':update['build_pre']['locale'],
        'buildid':update['build_pre']['buildid'],
        'url_aus':update['build_pre']['url_aus'],
    }
    data['post']={
        'user_agent':update['build_post']['user_agent'],
        'locale':update['build_post']['locale'],
        'buildid':update['build_post']['buildid'],
        'url_aus':update['build_post']['url_aus'],
    }


    data['channel']=update['patch']['channel']
    data['url_mirror']=update['patch']['url_mirror']
    data['size']=update['patch']['size']
    data['download_duration']=update['patch']['download_duration']
    data['type']=update['patch']['type']
    data['disabled_addons']=update['build_post']['disabled_addons']


    if update['success']:
        data['pass_fail']='Pass'
    else:
        data['pass_fail']='Fail'

    if update['patch']['is_complete']:
        data['complete']='complete'
    else:
        data['complete']='partial'

    if update['fallback']:
        data['fallback']='fallback'
    else:
        data['fallback']='direct'


    return jingo.render(request, 'display/report/update.html', data)



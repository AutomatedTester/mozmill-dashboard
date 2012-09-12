from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Results

import simplejson as json

@csrf_exempt
def report(request):
    if request.method=="POST":
        doc = json.loads(request.raw_post_data)
        try:
            del doc['_id']
            del doc['_rev']
        except:
            # we are only clearing so rough data so ok to ignore the exception
            pass

        for (counter, function) in enumerate(doc['results']):
            if function['failed'] == 0:
                doc['results'][counter]['passed_function'] = function['name']
            else:
                doc['results'][counter]['failed_function'] = function['name']

        results = Results(results=doc)
        results.save()

        report_to_es(request.raw_post_data)

    return HttpResponse('Hello World')

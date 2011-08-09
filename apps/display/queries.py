#!/usr/bin/env python

import simplejson as json
from httplib2 import Http

class reports:
    query = {
        "size":100,
        "query": {
            "bool":{
                "must" : [
                ]
            }
        },
        "filter": {
            "range":{
                "time_upload":{
                    "from":"2011-01-16",
                    "to":"2011-01-19"
                } 
            }
        }
    }

    filters=[]
    from_date="2011-01-16"
    to_date="2011-01-19"

    def update_query(self):
        if len(self.filters)==0:
            self.query['query']={'match_all':{}}
        else:
            self.query['query']={'bool':{'must':self.filters}}

        self.query['filter']['range']['time_upload']['from']=self.from_date
        self.query['filter']['range']['time_upload']['to']=self.to_date

                
###Filter Manuplation
    def add_filter_term(self, requirement):
        self.filters.append({"text":requirement})

    def clear_filters(self):
        self.filters = []


###OUT PUT
    def dump(self):
        self.update_query()
        return json.dumps(self.query)
 
    def execute(self):
        self.update_query()
        return grabber(self.query)

    def return_reports(self):
        hits = self.execute()['hits']['hits']
        results=[]

        for hit in hits:
            hit = hit['_source']
            result={
                'date':hit['time_upload'],
                'version':hit['application_version'],
                'build':hit['platform_buildid'],
                'locale':hit['application_locale'],
                'cpu':hit['system_info']['processor'],
                'pass':hit['tests_passed'],
                'skip':hit['tests_skipped'],
                'fail':hit['tests_failed'],
                'id':hit['_id'],
            }
            results.append(result)

        return results
           

def grab_operating_systems(query):
    content = grabber(query)
    result=[]
    for term in content['facets']['tag']['terms']:
        result.append(term['term'])
    return result

def grab_facet_response(query):
    content = grabber(query)
    result=[]
    for term in content['facets']['tag']['terms']:
        result.append({'name':term['term'],'failures':term['count']})
    return result 

def parse(query, formatter):
    h=Http()
    resp, content = h.request('http://10.250.7.224:9200/filter1/doc/_search', "GET", json.dumps(query))
    if resp['status']=='200':
        content = json.loads(content)
        facets = formatter(content['facets'])
        return facets
    else:
        return {'response':resp['status']}
        
def grabber(query, _id=False):
    h=Http()


    server='http://localhost:9200/db/db/'
    if _id:
        server+=_id
    else:
        server+='_search'
    resp, content = h.request(server, "GET", json.dumps(query))
    if resp['status']=='200':
        return json.loads(content)
        #return facets
    else:#TODO: Should maybe throw an exeption on this guy
        raise
        return {'response':resp['status']}
        



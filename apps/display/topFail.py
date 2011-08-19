def top_fail(request):
    data = {}
    
    

    query = {
    'query':{
        'match_all':{}
    },
    'facets':{
        'tag':{
            "terms":{
                "field":"failed_function",
                "size":10
            }
        }
    }
}

    os_query = {
    'query':{
        'match_all':{}
    },
    'facets':{
        'tag':{
            "terms":{
                "script_field":"failed_function",
                "size":10
            }
        }
    }
}
    os_query=deepcopy(query)
    os_query['facets']['tag']['terms']['field']='system'
    oses = grab_operating_systems(os_query)

    if request.method=="POST":
        if request.POST['os'] in oses:
            query['query']={"term":{
                "system":request.POST['os']
                }
            }

    fails = grab_facet_response(query)
    data = {'fails':fails,'operating_systems':oses}
    return jingo.render(request, 'display/filtered_table.html', data)

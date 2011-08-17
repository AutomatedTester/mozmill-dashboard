
def filter_request(request,foo,key,name,options):
    #foo
    try:
        request.GET[key]
    except:
        return

    if request.GET[key]=='all':
		return

    if request.GET[key] in options:
        foo.add_filter_term({name:request.GET[key]})
    else:
		raise



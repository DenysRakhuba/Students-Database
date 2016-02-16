import endless_pagination

def students_proc(request):
	current_uri = '{scheme}://{host}'.format(scheme=request.scheme,host=request.get_host())
	return {'PORTAL_URL': current_uri}
											 

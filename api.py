from django.shortcuts import render
from django.http import HttpResponse
import xmltodict, json, html, os, hashlib, re
from collections import OrderedDict

def _json_response(data):
	return HttpResponse(json.dumps(data), content_type="application/json")

def _find_notes_path(filename):
	for entry in os.scandir('/opt/notes'):
		if entry.is_file() and entry.name == filename:
			return entry.path
	return None

def rmNotes(request, hashstr):
	if 'scanfile' not in request.session:
		return _json_response({'error': 'scan file not loaded'})

	scanfilemd5 = hashlib.md5(str(request.session['scanfile']).encode('utf-8')).hexdigest()
	if re.match('^[a-f0-9]{32,32}$', hashstr) is not None:
		notefile = _find_notes_path(scanfilemd5+'_'+hashstr+'.notes')
		if notefile is not None:
			os.remove(notefile)
			res = {'ok':'notes removed'}
		else:
			res = {'error':'notes not found'}
	else:
		res = {'error':'invalid format'}

	return _json_response(res)

def saveNotes(request):
	if request.method == "POST":
		if 'scanfile' not in request.session:
			return _json_response({'error': 'scan file not loaded'})

		if 'hashstr' not in request.POST or 'notes' not in request.POST:
			return _json_response({'error': 'missing parameters'})

		scanfilemd5 = hashlib.md5(str(request.session['scanfile']).encode('utf-8')).hexdigest()

		if re.match('^[a-f0-9]{32,32}$', request.POST['hashstr']) is not None:
			f = open('/opt/notes/'+scanfilemd5+'_'+request.POST['hashstr']+'.notes', 'w')
			f.write(request.POST['notes'])
			f.close()
			res = {'ok':'notes saved'}
		else:
			res = {'error':'invalid format'}
	else:
		res = {'error': request.method }

	return _json_response(res)

def rmlabel(request, objtype, hashstr):
	types = {
		'host':True,
		'port':True
	}

	if 'scanfile' not in request.session:
		return _json_response({'error': 'scan file not loaded'})

	if objtype not in types:
		return _json_response({'error':'invalid object type'})

	scanfilemd5 = hashlib.md5(str(request.session['scanfile']).encode('utf-8')).hexdigest()

	if re.match('^[a-f0-9]{32,32}$', hashstr) is not None:
		labelfile = _find_notes_path(scanfilemd5+'_'+hashstr+'.'+objtype+'.label')
		if labelfile is not None:
			os.remove(labelfile)
			res = {'ok':'label removed'}
		else:
			res = {'error':'label not found'}
	else:
		res = {'error':'invalid format'}

	return _json_response(res)

def label(request, objtype, label, hashstr):
	labels = {
		'Vulnerable':True,
		'Critical':True,
		'Warning':True,
		'Checked':True
	}

	types = {
		'host':True,
		'port':True
	}

	if 'scanfile' not in request.session:
		return _json_response({'error': 'scan file not loaded'})

	scanfilemd5 = hashlib.md5(str(request.session['scanfile']).encode('utf-8')).hexdigest()

	if label in labels and objtype in types:
		if re.match('^[a-f0-9]{32,32}$', hashstr) is not None:
			f = open('/opt/notes/'+scanfilemd5+'_'+hashstr+'.'+objtype+'.label', 'w')
			f.write(label)
			f.close()
			res = {'ok':'label set', 'label':str(label)}
		else:
			res = {'error':'invalid format'}
	else:
		res = {'error':'invalid label or object type'}

	return _json_response(res)

def port_details(request, address, portid):
	if 'scanfile' not in request.session:
		return _json_response({'error': 'scan file not loaded'})

	r = {}
	oo = xmltodict.parse(open('/opt/xml/'+request.session['scanfile'], 'r').read())
	r['out'] = json.dumps(oo['nmaprun'], indent=4)
	o = json.loads(r['out'])

	for ik in o['host']:

		# this fix single host report
		if type(ik) is dict:
			i = ik
		else:
			i = o['host']

		if '@addr' in i['address']:
			saddress = i['address']['@addr']
		elif type(i['address']) is list:
			for ai in i['address']:
				if ai['@addrtype'] == 'ipv4':
					saddress = ai['@addr'] 

		if str(saddress) == address:
			for pobj in i['ports']['port']:
				if type(pobj) is dict:
					p = pobj
				else:
					p = i['ports']['port']

				if p['@portid'] == portid:
					return _json_response(p)

	return _json_response({'error': 'port not found'})

def genPDF(request):
	if 'scanfile' in request.session:
		pdffile = hashlib.md5(str(request.session['scanfile']).encode('utf-8')).hexdigest()
		if os.path.exists('/opt/nmapdashboard/nmapreport/static/'+pdffile+'.pdf'):
			os.remove('/opt/nmapdashboard/nmapreport/static/'+pdffile+'.pdf')

		os.popen('/opt/wkhtmltox/bin/wkhtmltopdf --cookie sessionid '+request.session._session_key+' --enable-javascript --javascript-delay 6000 http://127.0.0.1:8000/view/pdf/ /opt/nmapdashboard/nmapreport/static/'+pdffile+'.pdf')
		res = {'ok':'PDF created', 'file':'/static/'+pdffile+'.pdf'}
		return _json_response(res)

	return _json_response({'error': 'scan file not loaded'})

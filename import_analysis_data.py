import urllib2
import click
import json




def download_cds(cds_id):
	url = 'https://cds.cern.ch/record/{}/?of=recjson'.format(cds_id)
	return  json.load(urllib2.urlopen(url))

def extract_cds(cds_id,data):
	copnames = data[0]['corporate_name']

	collaboration = None
	for cop in copnames:
		if 'collaboration' in cop:
			collaboration = cop['collaboration']
	if not collaboration:
		for cop in copnames:
			if 'name' in cop:
				name = cop['name']
				if any([x in name for x in ['collaboration','Collaboration']]):
					collaboration = name
	if not collaboration:
		raise RuntimeError('no collaboration in CDS record {}'.format(cds_id))

	title = data[0]['title']['title']
	abstracttext = data[0]['abstract']['summary']

	result = {
		'inspire_id': '',
		'collaboration':collaboration,
		'title':title,
		'abstract': abstracttext,
		'doi':'',
		'arXiv': '',
		'inspireURL': '',
		'pubtype': 'cds',
		'pubid': cds_id
	}
	verify_data(result)
	return result


def download_inspire(inspire_id):
	url = 'https://inspirehep.net/record/{}?of=recjson'.format(inspire_id)
	return  json.load(urllib2.urlopen(url))

def extract_inspire(inspire_id,data):
	url = 'http://inspirehep.net/record/{}'.format(inspire_id)
	abstract = data[0]['abstract']
	abstracttext = None
	if type(abstract)==dict and abstract['number']=='arXiv':
		abstracttext = abstract['summary']
	elif type(abstract)==list:
		for x in abstract:
			if x.get('number','')=='arXiv':
				abstracttext = x['summary']
	else:
		raise RuntimeError('not sure how to find abstract for inspire %s',inspire_id)

	title = data[0]['title']['title']
	if type(data[0]['doi'])==list:
		doi = data[0]['doi'][0]
	elif type(data[0]['doi']) in [str,unicode]:
		doi = data[0]['doi']
	else:
		raise RuntimeError('weird doi',data[0]['doi'])


	collaboration = data[0]['corporate_name'][0]['collaboration']
	arXiv = [x['value'] for x in data[0]['system_control_number'] if x['institute'] == 'arXiv'][0]
	inspire = url
	result = {
		'collaboration':collaboration,
		'title':title,
		'abstract': abstracttext,
		'doi':doi,
		'arXiv': arXiv,
		'inspireURL': inspire,
		'pubtype': 'inspire',
		'pubid': inspire_id
	}

	verify_data(result)
	return result

def verify_data(result):
	try:
		assert all([type(x) in [str,unicode] for x in result.values()])
	except AssertionError:
		print 'vvvvvv'
		for k,v in result.iteritems():
			print k,type(v),v
		raise RuntimeError('Type Problem')

if __name__ == '__main__':
	main()
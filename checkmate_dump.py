import import_analysis_data
import json

checkmatedata = json.load(open('checkmate/checkmate_to_pub.json'))

dumpdata = []
for checkmate_analysis,pubinfo in checkmatedata.iteritems():
	print '{}/{}'.format(pubinfo['pubtype'],pubinfo['pubid']) 
	if pubinfo['pubtype'] == 'cds':
		data = import_analysis_data.download_cds(pubinfo['pubid'])
		data = import_analysis_data.extract_cds(pubinfo['pubid'],data)
	if pubinfo['pubtype'] == 'inspire':
		data = import_analysis_data.download_inspire(pubinfo['pubid'])
		data = import_analysis_data.extract_inspire(pubinfo['pubid'],data)
	dumpdata.append(data)

json.dump(dumpdata,open('checkmate_dump.json','w'))

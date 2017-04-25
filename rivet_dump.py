import import_analysis_data
import json

rivetdata = json.load(open('rivet/analyses.json'))
dumpdata = []

for inspire_id,rivet_ids in rivetdata.iteritems():
	if any([('ATLAS' in x) for x in rivet_ids]):
		print inspire_id
		data = import_analysis_data.download_inspire(inspire_id)
		data = import_analysis_data.extract_inspire(inspire_id,data)
		dumpdata.append(data)

json.dump(dumpdata,open('rivet_dump.json','w'))

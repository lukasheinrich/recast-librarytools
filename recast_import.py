import recastapi.analysis.write
import json
import time
import click


@click.command()
@click.argument('inputdata')
@click.argument('returndata')
@click.option('-d','--dry',help = 'dry run')
def recast_import(inputdata,returndata,dry):
	data = json.load(open(inputdata))
	return_data = []
	print data[0].keys()
	for entry in data:
		args = [
			entry['title'],
			entry['collaboration'],
			entry['arXiv'],
			'',
			entry['doi'],
			entry['inspireURL'],
			entry['abstract'],
			'LHC pp',
			'LHC pp collisions'
		]

		return_data.append({
			'pubtype': entry['pubtype'],
			'pubid': entry['pubid'],
			'recast_info': recastapi.analysis.write.analysis(*args) if not dry else {'dry':'run'}
		})
		print 'added'
		time.sleep(0.2)
	json.dump(return_data,open(returndata,'w'))

if __name__ == '__main__':
	recast_import()
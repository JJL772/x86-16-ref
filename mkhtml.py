#!/usr/bin/env python3

import sys
import os
import json

def make_pretty_flags(flags: str) -> str:
	return ''.join([x if x in flags else '.' for x in 'oditszapc']) 

def make_mnem(entry: dict) -> list[str]:
	mnem = entry['mnem'].upper()
	r = []
	for f in entry['forms']:
		r.append(f'{mnem} {f["dst"]} {f["src"]}')
	return r

def main():
	
	f = None
	for a in sys.argv:
		f = a
	if f is None:
		print('No file specified.')
		exit(1)
	f = os.path.abspath(f)
	os.chdir(os.path.dirname(__file__))
	
	# Read all source files (for embed)
	doc = None
	search = None
	style = None
	with open('doc.html') as fp:
		doc = fp.read()
	with open('search.js') as fp:
		search = fp.read()
	with open('style.css') as fp:
		style = fp.read()
	
	doc = doc.replace('/*$$STYLE$$*/', style)
	doc = doc.replace('/*$$SCRIPT$$*/', search)
	
	# Build table
	table = {}
	output = '<table id="Table" border="0"><tr class="header"><th>Instruction<br>[INST DST SRC]</th><th>Modified Flags<br>[oditszapc]</th><th>Undefined Flags<br>[oditszapc]</th><th>Description</th></tr>'
	with open(f) as fp:
		table = json.load(fp)
	for e in table:
		for m in make_mnem(e):
			output+='<tr>'
			output+=f'<td>{m}</td>'
			output+=f'<td class="center">{make_pretty_flags(e["mflags"])}</td>'
			output+=f'<td class="center">{make_pretty_flags(e["uflags"])}</td>'
			output+=f'<td>{e["desc"]["brief"]}</td>'
			output+='</tr>\n'
	output += '</table>'

	doc = doc.replace('<!--$$TABLE$$-->', output)
	try:
		os.mkdir('build')
	except:
		pass
	with open('build/x86-16-ref.html', 'wb') as fp:
		fp.write(doc.encode('utf-8'))
	print('Successfully processed build/x86-16-ref.html!')
	

if __name__ == "__main__": 
	main()
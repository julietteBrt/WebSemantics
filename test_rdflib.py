import csv
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD, FOAF 
import pandas as pd 
import json
import rdflib

filename = 'gares-tgv.csv'
#filename = 'test.csv'
df = pd.read_csv(filename, encoding = 'UTF-8')#encoding = "ISO-8859-1") # encoding = "utf-8-sig")
print(df)
g = rdflib.Graph()
stations = Namespace('http://example.org/stations/')
region = Namespace('http://region.org/region/')
schema = Namespace('http://schema.org/')
dep = Namespace('http://departement.org/departement/')
lati = Namespace('http://latitude.org/latitude/')
longi = Namespace('http://longitude.org/longitude/')

string_col = ['Nom_Gare', 'NOM_REG', 'NOM_DEP']

for col in string_col:
	#df[col] = df[col].apply(lambda value: value.encode(encoding = 'UTF-8', errors = 'strict'))
	df[col] = df[col].apply(lambda value: value.replace(' ', '-'))

for i, row in df.iterrows():
	g.add((URIRef(stations + row['Nom_Gare']), URIRef(schema + 'station_name'), Literal(row['Nom_Gare'], datatype = XSD.string)))
	g.add((URIRef(stations + row['Nom_Gare']), URIRef(schema + 'reg_name'), Literal(row['NOM_REG'], datatype = XSD.string)))
	g.add((URIRef(stations + row['Nom_Gare']), URIRef(schema + 'dep_name'), Literal(row['NOM_DEP'], datatype = XSD.string)))
	g.add((URIRef(stations + row['Nom_Gare']), URIRef(schema + 'latitude'), Literal(row['Latitude'], datatype = XSD.float)))
	g.add((URIRef(stations + row['Nom_Gare']), URIRef(schema + 'longitude'), Literal(row['Longitude'], datatype = XSD.float)))

	#g.add((URIRef(region + row['NOM_REG']), URIRef(schema + 'reg_name'), Literal(row['NOM_REG'], datatype = XSD.string)))
	#g.add((URIRef(dep + row['NOM_DEP']), URIRef(schema + 'dep_name'), Literal(row['NOM_DEP'], datatype = XSD.string)))
	#g.add((URIRef(lati + str(row['Latitude'])), URIRef(schema + 'latitude'), Literal(row['Latitude'], datatype = XSD.float)))
	#g.add((URIRef(dep + str(row['Longitude'])), URIRef(schema + 'longitude'), Literal(row['Longitude'], datatype = XSD.float)))

print(g.serialize(format='turtle').decode('UTF-8'))

g.serialize('outgares.ttl', format='turtle')
g.serialize('outgares1.rdf', format='application/rdf+xml')

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD, FOAF 
import pandas as pd 
import json
import rdflib

df_routes = pd.read_csv('./data/routes.txt')
df_trips = pd.read_csv('./data/trips.txt')
df_stop_times = pd.read_csv('./data/stop_times.txt')
df_stops = pd.read_csv('./data/stops.txt')
df_tranfers = pd.read_csv('./data/transfers.txt')
df_agency = pd.read_csv('./data/agency.txt')

g = rdflib.Graph()
h = rdflib.Graph()

# URIs
schema = Namespace('http://schema.org/')
agencies = Namespace('http://region.org/agencies/')
transfers = Namespace('http://example.org/transfers/')
routes = Namespace('http://example.org/routes/')
stops = Namespace('http://example.org/stops/')
trips = Namespace('http://example.org/trips/')
stop_times = Namespace('http://example.org/stop_times/')

string_col_routes = ['route_long_name']
string_col_stop_times = ['stop_id']
string_col_stops = ['stop_id', 'stop_name']

string_col_transfers = ['from_stop_id', 'to_stop_id']

for col in string_col_transfers:
	df_tranfers[col] = df_tranfers[col].apply(lambda value: value.replace(' ', '_'))
	df_tranfers[col] = df_tranfers[col].apply(lambda value: value.replace('/', '-'))


for i, row in df_tranfers.iterrows():
	g.add((URIRef(transfers + row['from_stop_id']), URIRef(schema + 'from_stop_id'), Literal(row['from_stop_id'], datatype = XSD.string)))
	g.add((URIRef(transfers + row['from_stop_id']), URIRef(schema + 'to_stop_id'), Literal(row['to_stop_id'], datatype = XSD.string)))
	g.add((URIRef(transfers + row['from_stop_id']), URIRef(schema + 'transfer_type'), Literal(row['transfer_type'], datatype = XSD.integer)))
	g.add((URIRef(transfers + row['from_stop_id']), URIRef(schema + 'min_transfer_time'), Literal(row['min_transfer_time'], datatype = XSD.integer)))
	g.add((URIRef(transfers + row['from_stop_id']), URIRef(schema + 'from_route_id'), Literal(row['from_route_id'], datatype = XSD.string)))
	g.add((URIRef(transfers + row['from_stop_id']), URIRef(schema + 'to_route_id'), Literal(row['to_route_id'], datatype = XSD.string)))

g.serialize('transfers.rdf', format='application/rdf+xml')

for i, row in df_agency.iterrows():
	h.add((URIRef(agencies + row['agency_id']), URIRef(schema + 'agency_id'), Literal(row['agency_id'], datatype = XSD.string)))
	h.add((URIRef(agencies + row['agency_id']), URIRef(schema + 'agency_name'), Literal(row['agency_name'], datatype = XSD.string)))
	h.add((URIRef(agencies + row['agency_id']), URIRef(schema + 'agency_url'), Literal(row['agency_url'], datatype = XSD.string)))
	h.add((URIRef(agencies + row['agency_id']), URIRef(schema + 'agency_timezone'), Literal(row['agency_timezone'], datatype = XSD.string)))
	h.add((URIRef(agencies + row['agency_id']), URIRef(schema + 'agency_lang'), Literal(row['agency_lang'], datatype = XSD.language)))

h.serialize('agencies.rdf', format='application/rdf+xml')

g = rdflib.Graph()
h = rdflib.Graph()
ig = rdflib.Graph()
j = rdflib.Graph()

for col in string_col_routes:
	df_routes[col] = df_routes[col].apply(lambda value: value.replace(' ', '_'))
	df_routes[col] = df_routes[col].apply(lambda value: value.replace('/', '-'))

for col in string_col_stop_times:
	df_stop_times[col] = df_stop_times[col].apply(lambda value: value.replace(' ', '_'))
	df_stop_times[col] = df_stop_times[col].apply(lambda value: value.replace('/', '-'))

for col in string_col_stops:
	df_stops[col] = df_stops[col].apply(lambda value: value.replace(' ', '_'))
	df_stops[col] = df_stops[col].apply(lambda value: value.replace('/', '-'))


for i, row in df_routes.iterrows():
	g.add((URIRef(routes + row['route_id']), URIRef(schema + 'route_id'), Literal(row['route_id'], datatype = XSD.string)))
	g.add((URIRef(routes + row['route_id']), URIRef(schema + 'route_short_name'), Literal(row['route_short_name'], datatype = XSD.string)))
	g.add((URIRef(routes + row['route_id']), URIRef(schema + 'route_long_name'), Literal(row['route_long_name'], datatype = XSD.string)))
	g.add((URIRef(routes + row['route_id']), URIRef(schema + 'route_type'), Literal(row['route_type'], datatype = XSD.integer)))
	g.add((URIRef(routes + row['route_id']), URIRef(schema + 'agency_id'), Literal(row['agency_id'], datatype = XSD.string)))

g.serialize('routes.rdf', format='application/rdf+xml')

for i, row in df_stops.iterrows():
	h.add((URIRef(stops + row['stop_id']), URIRef(schema + 'stop_id'), Literal(row['stop_id'], datatype = XSD.string)))
	h.add((URIRef(stops + row['stop_id']), URIRef(schema + 'stop_name'), Literal(row['stop_name'], datatype = XSD.string)))
	h.add((URIRef(stops + row['stop_id']), URIRef(schema + 'stop_lat'), Literal(row['stop_lat'], datatype = XSD.float)))
	h.add((URIRef(stops + row['stop_id']), URIRef(schema + 'stop_lon'), Literal(row['stop_lon'], datatype = XSD.float)))
	h.add((URIRef(stops + row['stop_id']), URIRef(schema + 'location_type'), Literal(row['location_type'], datatype = XSD.integer)))

h.serialize('stops.rdf', format='application/rdf+xml')

for i, row in df_trips.iterrows():
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'route_id'), Literal(row['route_id'], datatype = XSD.string)))
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'service_id'), Literal(row['service_id'], datatype = XSD.string)))
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'trip_id'), Literal(row['trip_id'], datatype = XSD.string)))
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'trip_headsign'), Literal(row['trip_headsign'], datatype = XSD.string)))
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'direction_id'), Literal(row['direction_id'], datatype = XSD.string)))
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'block_id'), Literal(row['block_id'], datatype = XSD.string)))
	ig.add((URIRef(trips + row['route_id']), URIRef(schema + 'shape_id'), Literal(row['shape_id'], datatype = XSD.string)))

ig.serialize('trips.rdf', format='application/rdf+xml')

for i, row in df_stop_times.iterrows():
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'trip_id'), Literal(row['trip_id'], datatype = XSD.string)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'arrival_time'), Literal(row['arrival_time'], datatype = XSD.time)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'departure_time'), Literal(row['departure_time'], datatype = XSD.time)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'stop_id'), Literal(row['stop_id'], datatype = XSD.string)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'stop_sequence'), Literal(row['stop_sequence'], datatype = XSD.integer)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'stop_headsign'), Literal(row['stop_headsign'], datatype = XSD.integer)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'pickup_type'), Literal(row['pickup_type'], datatype = XSD.integer)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'drop_off_type'), Literal(row['drop_off_type'], datatype = XSD.integer)))
	j.add((URIRef(stop_times + row['trip_id']), URIRef(schema + 'shape_dist_traveled'), Literal(row['shape_dist_traveled'], datatype = XSD.integer)))

ig.serialize('stop_times.rdf', format='application/rdf+xml')
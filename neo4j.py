#!/c/Python34/python.exe

from py2neo import Graph,Node,Relationship
import csv
import time

graph = Graph()

def neo4j_import(graph, filename):
	with open(filename) as tsv:
		for line in csv.reader(tsv, delimiter="\t"):
			print(line);
			if len(line) >= 2 and len(line[0]) > 0 and line[0][0] != '#':
				left = graph.find_one('junction', property_key='id', property_value=line[0])
				right = graph.find_one('junction', property_key='id', property_value=line[1])
	
				print(left)
				print(right)
	
				if left is None:
					left = Node("junction", id=line[0])
				if right is None:
					right = Node("junction", id=line[1])
	
				left_to_right = Relationship(left, "to", right)
				graph.create(left_to_right)
		
def neo4j_neighbor_count(graph, id):
	results = graph.cypher.execute("match (ei:junction)-[:to]-() where ei.id={id} return count(*)", {"id": id})
	for record in results:
		print(record)

def neo4j_reachability_count(graph, id):
	results = graph.cypher.execute("match (ei:junction {id:{id}}),(ej:junction),p=shortestPath((ei)-[:to*]-(ej)) return count(*)", {"id": id})
	for record in results:
		print(record)

start = time.clock()
neo4j_neighbor_count(graph, '10')
end = time.clock()

print(end - start)

start = time.clock()
neo4j_reachability_count(graph, '10')
end = time.clock()

print(end - start)

#!/c/Python34/python.exe

from py2neo import Graph,Node,Relationship
import csv
import time


def neo4j_import(graph, filename):
	i = 0
	with open(filename) as tsv:
		for line in csv.reader(tsv, delimiter="\t"):
			if len(line) >= 2 and len(line[0]) > 0 and line[0][0] != '#':
				left = graph.find_one('junction', property_key='id', property_value=line[0])
				right = graph.find_one('junction', property_key='id', property_value=line[1])
	
				if left is None:
					left = Node("junction", id=line[0])
				if right is None:
					right = Node("junction", id=line[1])
	
				left_to_right = Relationship(left, "to", right)
				graph.create(left_to_right)
			i += 1

			if i >= 10000:
				return
		
def neo4j_neighbor_count(graph, id):
	results = graph.cypher.execute("match (ei:junction)-[:to]-(ej:junction) where ei.id={id} return count(ej)", {"id": id})
	for record in results:
		print(record)

def neo4j_reachability_count(graph, id):
	results = graph.cypher.execute("match (ei:junction {id:{id}}),(ej:junction),p=shortestPath((ei)-[:to*]-(ej)) return count(*)", {"id": id})
	for record in results:
		print(record)

graph = Graph()

node_count = 10

average = 0
min = 99999999999
max = 0

for i in range(0, node_count):
	start = time.clock()
	neo4j_neighbor_count(graph, str(i))
	end = time.clock()
	
	diff = end - start

	if diff < min:
		min = diff
	if diff > max:
		max = diff
	average += diff

average /= node_count

print(min)
print(max)
print(average)


average = 0
min = 9999999999
max = 0

for i in range(0, node_count):
	start = time.clock()
	neo4j_reachability_count(graph, str(i))
	end = time.clock()
	
	diff = end - start

	if diff < min:
		min = diff
	if diff > max:
		max = diff
	average += diff

average /= node_count

print(min)
print(max)
print(average)

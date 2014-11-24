#!/c/Python34/python.exe

from py2neo import Graph,Node,Relationship
import csv


graph = Graph()

with open("roadNet-CA.txt") as tsv:
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
		



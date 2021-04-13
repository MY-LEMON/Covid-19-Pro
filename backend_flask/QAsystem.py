import os
import re
from settings import NEO4J_USER,NEO4J_PASSWORD,NEO4J_HOST
from py2neo import Graph, Node, Relationship


class MedicalGraph:
    def __init__(self):
        self.graph = Graph(NEO4J_HOST, username=NEO4J_USER, password=NEO4J_PASSWORD)


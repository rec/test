    graph={ 'A':['B','C'], 'B':['D','E'], 'C':['F'], 'D':[], 'E':['F'], 'F':[] }

    def visit_all(graph, node, your_visitor_function, visited=None):
        if visited is None:
            visited = set()
        elif node in visited:
            return
        visited.add(node)

        for kid in graph[node]:
            visit_all(graph, kid, your_visitor_function, visited)
        your_visitor_function(node)


    visit_all(graph, 'A', print)

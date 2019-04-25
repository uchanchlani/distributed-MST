import sys
import graphviz
from subprocess import call

STATE_LABEL = "CHANGE_STATE"
MSG_LABEL = "TERMINATED"

class Edge:
    def __init__(self, src, dest, weight, color):
        self.src = src
        self.dest = dest
        self.weight = weight
        self.color = color

class Graph:
    def __init__(self, input_file, out_dir=None):
        f = open(input_file, "r")
        self.n = int(f.readline())
        self.out_dir = out_dir
        self.edges = []
        for i in range(0,self.n):
            node_info = f.readline().strip()
            iterator = iter(node_info.split(" "))
            for to in iterator:
                wt = int(next(iterator))
                to_int = int(to)
                if i < to_int:
                    self.edges.append(Edge(i, to_int, wt, "black"))


    def print_graph(self, file_name):
        g = graphviz.Graph(format='png', filename=file_name)
        for i in range(0,self.n):
            g.node(str(i), str(i))

        for edge in self.edges:
            g.edge(str(edge.src), str(edge.dest), str(edge.weight), color=edge.color)

        g.render(directory=self.out_dir, cleanup=True, view=False)


    def change_color(self, src, dest, color):
        if src > dest:
            src, dest = dest, src
        for edge in self.edges:
            if edge.src == src and edge.dest == dest:
                edge.color = color
                return


class ChangesStash:
    def __init__(self, n):
        self.n = n
        self.edges = set()

    def get_hash(self, src, dest):
        if src > dest:
            src, dest = dest, src
        return src * self.n + dest

    def is_present(self, src, dest):
        return self.get_hash(src, dest) in self.edges

    def pop(self, src, dest):
        self.edges.remove(self.get_hash(src, dest))

    def push(self, src, dest):
        self.edges.add(self.get_hash(src, dest))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Input output and out directory file missing")
        sys.exit(1)

    dir_name = sys.argv[3]
    g = Graph(sys.argv[1], dir_name)
    iter = 0
    g.print_graph("%03d"%iter)
    iter = iter + 1
    changes = ChangesStash(g.n)
    count_msg = 0
    with open(sys.argv[2]) as changes_file:
        for line in changes_file:

            if line.find(STATE_LABEL) > 0:
                subline = line[line.find(STATE_LABEL) + len(STATE_LABEL) + 1:]
                src = int(subline.split(" ")[0])
                dest = int(subline.split(" ")[1])
                if changes.is_present(src, dest):
                    changes.pop(src, dest)
                    g.change_color(src, dest, "red")
                    g.print_graph("%03d"%iter)
                    iter = iter + 1
                else:
                    changes.push(src, dest)

            elif line.find(MSG_LABEL) > 0:
                count_msg += int(line[line.find(MSG_LABEL) + len(MSG_LABEL) + 1:])

    cmd = [ 'convert' ]
    for i in range(0, iter):
        cmd.extend(( '-delay', str( 50 ), "%s/%03d.png"%(dir_name, i)))
    cmd.append("%s/output.gif"%dir_name)
    call(cmd)
    print("Total Messages", int(count_msg/2))

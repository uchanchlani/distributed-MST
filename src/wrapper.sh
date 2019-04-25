#! /bin/bash
python3 src/generate_graph.py ${NODES} ${EDGES}
dar src/mstProcess.da graph_${NODES}_${EDGES}_input 2> graph_${NODES}_${EDGES}_output
python3 src/graphical.py graph_${NODES}_${EDGES}_input graph_${NODES}_${EDGES}_output ${NODES}_${EDGES} > ${NODES}_${EDGES}_stats
cat ${NODES}_${EDGES}_stats


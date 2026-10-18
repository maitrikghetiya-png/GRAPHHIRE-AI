from falkordb import FalkorDB

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("GraphHire")

result = graph.query(
    "RETURN 'GraphHire connected!' AS message"
)

for row in result.result_set:
    print(row[0])
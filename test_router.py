from graph.router import route_request
test_request = ["question","summary","mcq","descriptive","maths"]

for request in test_request:
    test_state = {"request_type":request}
    result = route_request(test_state)
    print(f"Request: {request} -> Node: {result}")
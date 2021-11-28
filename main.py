import json
import flask

class Route(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        routes = {}

        path = obj['path'].lower()
        method = obj['method'].upper()

        if path not in routes:
            routes[path] = {}
        routes[path][method] = {'body': obj['body'], 'status': obj['status']}

        return routes

def read_routes(config_path: str) -> dict:
    routes = None
    with open(config_path, 'r') as f:
        routes = json.load(f, cls=Route)
    
    result = {}
    for route in routes:
        path, rest = list(route.items())[0]
        if path not in result:
            result[path] = rest
        else:
            result[path] |= rest
    return result

routes = read_routes("mock.json")
print(routes)

app = flask.Flask(__name__)

@app.route('/<path:text>', methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def all(text: str):
    method = flask.request.method
    path = "/" + text

    print(f"Recieved {method} request {path}")

    if path not in routes or method not in routes[path]:
        return "400 Bad Request", 400

    res = routes[path][method]
    return res['body'], res['status']
    
if __name__ == "__main__":
    app.run(debug=False)

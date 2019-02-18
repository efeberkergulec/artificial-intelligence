import gym
import gym_warehouse

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from six import StringIO

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

env = gym.make('multirobot-warehouse-v0')

def render():
    l = env.look()
    out = StringIO()
    out.write("\n")
    out.write("\n".join(''.join(line) for line in l)+"\n")
    return out.getvalue()

def step(a):
    r = env.step(a)
    l = []
    for e in r:
        if e is None:
            l.append(0)
        else:
            l.append(e)
    print(l)
    return l

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler,
                        allow_none=True) as server:
    server.register_introspection_functions()

    server.register_function(render)
    server.register_function(env.look)
    server.register_function(step)
    server.register_function(env.close)
    
    # Run the server's main loop
    server.serve_forever()

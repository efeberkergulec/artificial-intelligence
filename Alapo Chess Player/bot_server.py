import rpyc
import bot_player
from rpyc.utils.server import ThreadedServer

class HumanService(rpyc.Service):

    def on_connect(self, conn):
        print("Connected to Server")
        return bot_player.connected_to_server()

    def on_disconnect(self, conn):
        print("Disconnected from Server")
        return bot_player.disconnected_from_server()

    def startgame(self, env, player):
        print("Game Started")
        print("You are player " + str(player))
        return bot_player.game_started(env, player)

    def move(self, player, env):
        print('Its your order to move')
        return bot_player.move(env)

    def move_response(self, env, resultcode):
        print("You Moved")
        return bot_player.move_response(env, resultcode)

    def opponent_moved(self, env):
        print("Opponent Moved")
        return bot_player.opponent_moved(env)

    def game_ended(self, env, result, resultcode):
        print("Game ended")
        return bot_player.game_ended(env, result, resultcode)



"""
Initialize Server - Don't touch this part
"""
try:
    t = ThreadedServer(HumanService, port=8001, protocol_config={"allow_public_attrs": True})
    t.start()
    print("Server started...")
except:
    print("Error while starting server...")

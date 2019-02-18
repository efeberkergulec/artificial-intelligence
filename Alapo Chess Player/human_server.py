import rpyc
import human_player


class HumanService(rpyc.Service):

    def on_connect(self, conn):
        print("Connected to Server")
        return human_player.connected_to_server()

    def on_disconnect(self, conn):
        print("Disconnected from Server")
        return human_player.disconnected_from_server()

    def startgame(self, env, player):
        print("Game Started")
        print("You are player " + str(player))
        return human_player.game_started(env, player)

    def move(self, player, env):
        print('Its your order to move')
        return human_player.move(env)

    def move_response(self, env, resultcode):
        print("You Moved")
        return human_player.move_response(env, resultcode)

    def opponent_moved(self, env):
        print("Opponent Moved")
        return human_player.opponent_moved(env)

    def game_ended(self, env, result, resultcode):
        print("Game ended")
        return human_player.game_ended(env, result, resultcode)


"""
Initialize Server - Don't touch this part
"""
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    try:
        t = ThreadedServer(HumanService, port=8000, protocol_config={"allow_public_attrs": True})
        t.start()

        print("Server started...")
    except:
        print("Error while starting server...")


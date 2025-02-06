import sys

from gamelib import *

# See the "SampleServiceInterface" from gamelib for a bigger example
# See https://gitlab.saarsec.rocks/saarctf/gamelib/-/blob/master/docs/howto_checkers.md for documentation.


class ExampleServiceInterface(ServiceInterface):
    def check_integrity(self, team: Team, tick: int) -> None:
        # pwntools "Could not connect" exception is accepted as OFFLINE
        with remote_connection(team.ip, 31337) as conn:  # use remote_connection instead of raw "remote()" or sockets
            conn.sendline(b'id ; exit')
            data = conn.recvall()
            # check for conditions - if an assert fails the service status is MUMBLE
            assert 'exampleservice' in data.decode(), 'Please do not re-code this service!'
        # HTTP example:
        # session = Session()  # use gamelib's session
        # response = assert_requests_response(session.get(f'http://{team.ip}:31337/'), 'text/html; charset=utf-8')

    def store_flags(self, team: Team, tick: int) -> None:
        flag = self.get_flag(team, tick)
        with remote_connection(team.ip, 31337) as conn:
            conn.sendline(f"echo 'TICK {tick}: {flag}' >> data.txt ; exit".encode())
            conn.recvall()

    def retrieve_flags(self, team: Team, tick: int) -> None:
        flag = self.get_flag(team, tick)
        with remote_connection(team.ip, 31337) as conn:
            conn.sendline(f"grep 'TICK {tick}:' data.txt ; exit".encode())
            data = conn.recvall(TIMEOUT)
        if flag not in data.decode():
            # verbose error logging is always a good idea
            print('GOT:', data)
            # flag not found? Raise FlagMissingException
            raise FlagMissingException('Flag not found')


if __name__ == '__main__':
    # USAGE: python3 interface.py                      # test against localhost
    # USAGE: python3 interface.py 1.2.3.4              # test against IP
    # USAGE: python3 interface.py 1.2.3.4 retrieve     # retrieve last 10 ticks (for exploits relying on checker interaction)
    # USAGE: python3 interface.py 1.2.3.4 store        # store a few ticks (for exploits relying on checker interaction)
    # (or use gamelib/run-checkers to test against docker container)
    team = Team(1, 'TestTeam', sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1')
    service = ExampleServiceInterface()

    if len(sys.argv) > 2 and sys.argv[2] == 'retrieve':
        for tick in range(1, 10):
            try:
                service.retrieve_flags(team, tick)
            except:
                pass
        sys.exit(0)
    elif len(sys.argv) > 2 and sys.argv[2] == 'store':
        for tick in range(50, 55):
            try:
                service.store_flags(team, tick)
            except:
                pass
        sys.exit(0)

    for tick in range(1, 4):
        print(f'\n\n=== TICK {tick} ===')
        service.check_integrity(team, tick)
        service.store_flags(team, tick)
        service.retrieve_flags(team, tick)

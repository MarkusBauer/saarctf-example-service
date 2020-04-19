from gamelib import *
from pwn import remote

# See the "SampleServiceInterface" from gamelib for a bigger example
# See https://gitlab.saarsec.rocks/saarctf/gamelib/-/blob/master/docs/howto_checkers.md for documentation.

class ExampleServiceInterface(ServiceInterface):
	name = 'ExampleService'

	def check_integrity(self, team: Team, tick: int):
		# pwntools "Could not connect" exception is accepted as OFFLINE
		conn = remote(team.ip, 31337, timeout=TIMEOUT)
		try:
			conn.sendline('id ; exit')
			data = conn.recvall()
			# check for conditions - if an assert fails the service status is MUMBLE
			assert('exampleservice' in data.decode(), 'Please do not re-code this service!')
		finally:
			# closing resources is important
			conn.close()

	def store_flags(self, team: Team, tick: int):
		flag = self.get_flag(team, tick)
		conn = remote(team.ip, 31337, timeout=TIMEOUT)
		try:
			conn.sendline(f"echo 'TICK {tick}: {flag}' >> data.txt ; exit")
			conn.recvall()
		finally:
			conn.close()

	def retrieve_flags(self, team: Team, tick: int):
		flag = self.get_flag(team, tick)
		conn = remote(team.ip, 31337, timeout=TIMEOUT)
		try:
			conn.sendline(f"grep 'TICK {tick}:' data.txt ; exit")
			data = conn.recvall(TIMEOUT)
		finally:
			conn.close()
		if flag not in data.decode():
			# verbose error logging is always a good idea
			print('GOT:', data)
			# flag not found? Raise FlagMissingException
			raise FlagMissingException('Flag not found')

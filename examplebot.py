from ircbot import IrcBot

CHANNEL = '#YourChannel'
BOT_NAME = 'ExampleBot'
SERVER = 'chat.freenode.net'
PORT = 6667

def Connected():
	print 'Connected to server!'
	bot.join_channel(CHANNEL)

def OnChannelJoined(user, channel):
	if user == BOT_NAME:
		print 'I joined %s!' % (channel)
		bot.send_message(channel, "Hello.")

def OnMessage(sender, message, destination):
	if sender != BOT_NAME:
		reply = 'Cool story, bro.'
		bot.send_message(destination, reply)
	else:
		print 'I said %s to %s.' % (message, destination)

def main():
	global bot
	bot = IrcBot(BOT_NAME, SERVER, PORT)
	bot.OnServerConnect = connected
	bot.OnJoin = OnChannelJoined
	bot.OnMessage = OnMessage
	bot.run()

if __name__ == '__main__':
	main()

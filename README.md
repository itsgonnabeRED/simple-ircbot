simple-ircbot
=============

A very simple irc bot library written in python.

### Features:

* Join multiple channels
* Send and receive messages
* Hooks for events

An [example bot](examplebot.py) is included.

# Documentation
## IRC bot methods
### Constructor
The constructor takes 3 parameters: the bot name, the IRC network server address, and the IRC network server port.
### Public instance methods
`run()` - Tells the bot to begin connecting. The bot will change it's nickname to what was supplied in the constructor. This starts a blocking loop. It will run until stop() is called on the bot.

`stop()` - Sends the QUIT message to the IRC server. Closes the network connection to the server and ends the run() loop.

`change_nick(name)` - Changes the nickname of the bot in IRC.

`join_channel(channel)` - The bot will join the channel. The channel name is most often case sensitive and always must start with the # symbol.

`send_message(destination, message)` - The bot will send the message to the destination. The destination can be a channel name (#YourChannel) to send it to everyone in the channel or a user name (BillTheUser) to private message them.

## Hooks
### How-to
To take advantage of a hook, just assign a function to the hook variable in the bot. Look at the example bot for a better idea of how this works.
### Available hooks
`OnServerConnect()` - Called when the server connection succeeds.

`OnTick()` - Called every time a message can be sent.

`OnMessage(sender, message, destination)` - Called on every message. Sender is the name of the user that sent the message. message is the text that was sent. Destination is where the message was sent to. It can be one of the channels the bot is in, or a private message. For channel messages, the destination is the name of the channel. For private messages, the destination is the bot name.

`OnJoin(name, channel)` - Called whenever someone joins a channel the bot is in. Name is the person who joined. _This is also called the first time the bot joins a channel_. In this case, the name will be the bot's name.

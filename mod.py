from time import time

class ModControl():
	def __init__(self, bot):
		self.bot = bot
		pass
		
	def step(self, event):
		if event.type == "private" and event.msg == "quit()":
			print("End Program")
			quit()
		if event.type == "channel" and event.msg == self.bot.nick + " quit()":
			print("End Program")
			quit()

class ModLog():
	def __init__(self, bot):
		pass
		
	def step(self, event):
		if event.type == "channel":
			print("[{2}] {0}: {1}".format(event.nick, event.msg, event.chan))
		elif event.type == "private":
			print("[private] {0}: {1}".format(event.nick, event.msg))
				
		elif event.type == "nick":
			print("{0} changed nick to {1} in channel {2}".format(event.nick, event.msg, event.chan))
		elif event.type == "join":
			print("{0} join {1}".format(event.nick, event.chan))
		elif event.type == "quit":
			print("{0} quit {1}".format(event.nick, event.chan))
		elif event.type == "part":
			print("{0} part {1}".format(event.nick, event.chan))

class ModVote():
	class Vote():
		def __init__(self, bot, identity):
			self.identity = identity
			self.timeout = 30
			self.question = ""
			self.choice = []
			self.start = 0
			self.active = False
			self.voter = []
		
	def __init__(self, bot):
		self.bot = bot
		self.vote = []
		self.activeVote = None
		self.bot.send("Type \"/msg {0} help\" for help".format(bot.nick))
		
	def step(self, event):
		if self.activeVote != None:
			av = self.activeVote
			#if vote timed out
			if av.start+av.timeout < time():
				self.bot.send("Vote timeout : "+av.question)
				for i in range(len(av.choice)):
					count = 0
					for v in av.voter:
						if v[0] == i:
							count += 1
					self.bot.send("{0}) [{1} vote{2}] {3}".format(i+1, count, "" if count < 2 else "s", av.choice[i]))
				for i in range(len(self.vote)):
					if self.vote[i].active == True:
						self.activeVote = None
						self.vote.pop(i)
						return
				
		if event != None:
			if event.type == "private":
				m = event.msg.split()
				
				if m[0] == "help":
					self.bot.send("vote create <question>: create a new, empty vote. You can have only one vote at a time",event.nick)
					self.bot.send("vote delete : delete the vote, allowing you to create a new one",event.nick)
					self.bot.send("vote set_question <question> : set the question of your vote",event.nick)
					self.bot.send("vote add <choice> : add a new choice",event.nick)
					self.bot.send("vote cancel_choice : cancel the last choice",event.nick)
					self.bot.send("vote reset_choices : empty the choice list",event.nick)
					self.bot.send("vote send <timeout> : Send your vote in the channel (where the bot is) for 60 sec, timeout sec if precised (min: 30, max: 300)",event.nick)
				
				if m[0] == "vote" and len(m) > 1:
					m = m[1:]
					#Help
					if m[0] == "help":
						self.bot.send("vote create <question>: create a new, empty vote. You can have only one vote at a time",event.nick)
						self.bot.send("vote delete : delete the vote, allowing you to create a new one",event.nick)
						self.bot.send("vote set_question <question> : set the question of your vote",event.nick)
						self.bot.send("vote add <choice> : add a new choice",event.nick)
						self.bot.send("vote cancel_choice : cancel the last choice",event.nick)
						self.bot.send("vote reset_choices : empty the choice list",event.nick)
						self.bot.send("vote send <timeout> : Send your vote in the channel (where the bot is) for 60 sec, timeout sec if precised (min: 30, max: 300)",event.nick)
						
					#Create vote
					elif m[0] == "create":
						for vote in self.vote:
							if vote.identity == event.identity:
								self.bot.send("You already have a vote created",event.nick)
								return
						self.vote.append(self.Vote(self.bot, event.identity))
						if len(m) > 1:
							self.vote[len(self.vote)-1].question = " ".join(m[1:])
							self.bot.send("Your vote have been created : "+self.vote[len(self.vote)-1].question,event.nick)
						else:
							self.bot.send("Your vote have been created",event.nick)
						return
						
					#Delete vote
					elif m[0] == "delete":
						for i in range(len(self.vote)):
							if self.vote[i].identity == event.identity:
								if self.vote[i].active == True:
									self.bot.send("Vote deleted !")
									self.activeVote = None
								self.vote.pop(i)
								self.bot.send("Your vote have been deleted", event.nick)
								return
						self.bot.send("You have no vote created",event.nick)
						return
						
					#Set Question
					elif m[0] == "set_question":
						if len(m) > 1:
							for vote in self.vote:
								if vote.identity == event.identity:
									vote.question = " ".join(m[1:])
									self.bot.send("Your question is set to "+vote.question,event.nick)
									return
							self.bot.send("You have no vote created",event.nick)
							return
						else:
							self.bot.send("No question set. Use like this : \"set_question Does pinguins have knees ?\"",event.nick)
							return
					#Add Choice
					elif m[0] == "add":
						if len(m) > 1:
							for vote in self.vote:
								if vote.identity == event.identity:
									vote.choice.append(" ".join(m[1:]))
									self.bot.send("Choice added : "+vote.choice[len(vote.choice)-1],event.nick)
									return
							self.bot.send("You have no vote created",event.nick)
							return
						else:
							self.bot.send("No choice set. Use like this : \"add Yes\"",event.nick)
							return
					
					#Cancel last Choice
					elif m[0] == "cancel_choice":
						for vote in self.vote:
							if vote.identity == event.identity:
								if len(vote.choice) > 0:
									self.bot.send("Choice cancel : "+vote.choice.pop(),event.nick)
									return
								else:
									self.bot.send("No more choice to cancel",event.nick)
									return
						self.bot.send("You have no vote created",event.nick)
						return
						
					#Reset all Choice
					elif m[0] == "reset_choices":
						for vote in self.vote:
							if vote.identity == event.identity:
								while len(vote.choice) > 0:
									vote.choice.pop()
								self.bot.send("All choices have been deleted",event.nick)
								return
						self.bot.send("You have no vote created",event.nick)
						return
						
					#Send vote
					elif m[0] == "send":
						if self.activeVote == None:
							for vote in self.vote:
								if vote.identity == event.identity:
									if vote.question != "":
										if len(vote.choice) > 1:
											if len(m) > 1:
												try:
													vote.timeout = max(30,min(int(m[1]), 60*5))
												except:
													self.bot.send("Timeout value failed convert to int", event.nick)
											vote.active = True
											vote.start = time()
											self.activeVote = vote
											self.bot.send("[VOTE] ({0}seconds) {1}".format(vote.timeout, vote.question))
											for i in range(len(vote.choice)):
												self.bot.send(str(i+1)+") "+vote.choice[i])
											self.bot.send("Type \"/msg "+self.bot.nick+" vote <number>\" to vote !")
											self.bot.send("Your vote have been send for {} sec".format(vote.timeout), event.nick)
											return
										else:
											self.bot.send("You must have at least two choices",event.nick)
											return
									else:
										self.bot.send("Your vote have no question",event.nick)
										return
							self.bot.send("You have no vote created",event.nick)
							return
						else:
							self.bot.send("A vote is already in progress, please be patient",event.nick)
							return
					
					#If no command (a client is voting ?)
					else:
						if self.activeVote != None:
							for vote in self.activeVote.voter:
								if vote[1] == event.identity:
									try:
										v = int(m[0])
										vote = (v-1, event.identity)
										self.bot.send("Your vote is changed to {}".format(v),event.nick)
									except Exception as e:
										print(e)
									
									return
							try:
								v = int(m[0])
							except Exception as e:
								self.bot.send("{0} to int have failed for voting".format(m[0]),event.nick)
								self.bot.send("Maybe you tried to type a command and failed, please type \"/msg {0} vote help\" for help".format(self.bot.nick),event.nick)
							else:
								if v >= 1 and v <= len(self.activeVote.choice):
									self.activeVote.voter.append((v-1, event.identity))
									self.bot.send("You have voted {0} : {1}".format(v, self.activeVote.choice[v-1]),event.nick)
									return
								else:
									self.bot.send("Your choice number is note in range",event.nick)
									return
						else:
							self.bot.send("No vote in progress",event.nick)
							self.bot.send("Maybe you tried to type a command and failed, please type \"/msg {0} vote help\" for help".format(self.bot.nick),event.nick)
							return
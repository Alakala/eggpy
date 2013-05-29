import re

from .base import Command

class QuoteTrigger:
    def on_message(self, bot, event):
        msg = event.message

        if not bot.trigger.lower() in msg.lower():
            return False
        if len(bot.quotes) == 0:
            bot.respond(event, "No quotes")
        else:
            quote = random.choice(bot.quotes)
            bot.respond(event, quote)

        return True

class AddQuote(Command):
    def on_command(self, bot, event, new_quote):
        if new_quote in bot.quotes:
            bot.respond(event, "ooooold")
            return True
        bot.quotes.add(new_quote)
        topic = bot.topics[event.target]
        if topic:
            newtopic = re.sub(re.compile(str(len(bot.quotes)-1)), str(len(bot.quotes)), topic)
            if newtopic != topic:
                bot.change_topic(event.target, newtopic)
                return True
        bot.respond(event, "Quote added. "+str(len(bot.quotes))+" quotes in database")
        return True

class GetQuote:
    def __init__(self):
        self.trigger = re.compile('^#(-?[1-9]\d*)?$')

    def on_message(self, bot, event):
        msg = event.message
        result = self.trigger.match(msg)
        if result is None:
            return False
        query = result.group(1)
        if query is None:
            bot.respond(event, str(len(bot.quotes)))
            return True
        number = int(query)
        if number < 0:
            number += len(bot.quotes)+1
        if number > len(bot.quotes) or number <= 0:
            return False
        bot.respond(event, bot.quotes[number-1])
        return True

class GetY:
    def __init__(self):
        self.trigger = re.compile(r'^:Y (..*)$')

    def on_message(self, bot, event):
        msg = event.message
        result = self.trigger.match(msg)
        if result is None:
            return False
        msg = msg[3:]
        buttQuotes = []
        for q in bot.quotes:
            if msg.lower() in q.lower():
                buttQuotes.append(q)
        if len(buttQuotes) == 0:
            quote = random.choice(bot.quotes)
            bot.respond(event, quote)
        else:
            quote = random.choice(buttQuotes)
            bot.respond(event, quote)
        return True

class FindQuote(Command):
    def on_command(self, bot, event, args):
        maximum = 30
        results = []
        result = None
        i = 1
        for q in bot.quotes:
            if args.lower() in q.lower():
                results.append(i)
                result = q
            i = i + 1
            if len(results) >= maximum:
                break
        if not results:
            bot.respond(event, "Not found")
            return True
        if len(results) == 1:
            bot.respond(event, str(int(results[0]))+": "+result)
            return True
        bot.respond(event, ', '.join(map(str, results)))
        return True

class SetQuote(Command):
    def on_command(self, bot, event, args):
        bot.quotes.set_last(args)
        bot.respond(event, 'Done!')
        return True



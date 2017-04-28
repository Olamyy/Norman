import datetime
import random
import string
import time

from regex import search

from Norman.settings import RegexConfig


class NLPProcessor:
    def __init__(self, sentence, recipient_id):
        self.sentence = sentence
        self.no_response_list = ["*scratch my head* :(", "How do I respond to that... :O",
                                 "I can be not-so-smart from time to time... :(",
                                 "Err... you know I'm not human, right? :O", "I do not understand you."]
        self.error = ["Sorry I've got a little bit sick. BRB in 2 min :(", "Oops... 404 My Witty Mind Not Found :O",
                      "Oops... My brain went MIA in the cloud, BRB in 2 :(",
                      "Hmm... How should I respond to that... :O"]

        self.looking_replies = ["Sure, give me a few seconds... B-)", "Scanning the world... :D", "Zoom zoom zoom...",
                                "Going into the Food Cerebro... B-)",
                                "Believe me, I'm a foodie, not an engineer... B-)"]

        self.bad_words = ['4r5e','5h1t','5hit','a55','anal','anus','ar5e','arrse','arse','ass','ass-fucker','asses'
                            ,'assfucker','assfukka','asshole','assholes','asswhole','a_s_s','b!tch','b00bs',
                          'b17ch','b1tch','ballbag','balls','ballsack','bastard','beastial','beastiality',
                          'bellend','bestial','bestiality','bi+ch','biatch','bitch','bitcher','bitchers',
                          'bitches','bitchin','bitching','bloody','blow job','blowjob','blowjobs','boiolas',
                          'bollock','bollok','boner','boob','boobs','booobs','boooobs','booooobs','booooooobs',
                          'breasts','buceta','bugger','bum','bunny fucker','butt','butthole','buttmuch','buttplug',
                          'c0ck','c0cksucker','carpet muncher','cawk','chink','cipa','cl1t','clit','clitoris','clits'
                        ,'cnut','cock','cock-sucker','cockface','cockhead','cockmunch','cockmuncher','cocks','cocksuck '
                        ,'cocksucked ','cocksucker','cocksucking','cocksucks ','cocksuka','cocksukka','cok','cokmuncher','coksucka','coon','cox','crap','cum','cummer','cumming','cums','cumshot','cunilingus','cunillingus','cunnilingus','cunt','cuntlick ','cuntlicker ','cuntlicking ','cunts','cyalis','cyberfuc','cyberfuck ','cyberfucked ','cyberfucker','cyberfuckers','cyberfucking ','d1ck','damn','dick','dickhead','dildo','dildos','dink','dinks','dirsa','dlck','dog-fucker','doggin','dogging','donkeyribber','doosh','duche','dyke','ejaculate','ejaculated','ejaculates ','ejaculating ','ejaculatings','ejaculation','ejakulate','fu', 'f u','f u c k','f u c k e r','f4nny','fag','fagging','faggitt','faggot','faggs','fagot','fagots','fags','fanny','fannyflaps','fannyfucker','fanyy','fatass','fcuk','fcuker','fcuking','feck','fecker','felching','fellate','fellatio','fingerfuck ','fingerfucked ','fingerfucker ','fingerfuckers','fingerfucking ','fingerfucks ','fistfuck','fistfucked ','fistfucker ','fistfuckers ','fistfucking ','fistfuckings '
                        ,'fistfucks ','flange','fook','fooker','fuck','fucka','fucked','fucker','fuckers','fuckhead','fuckheads',
                          'fuckin','fucking','fuckings','fuckingshitmotherfucker','fuckme ','fucks','fuckwhit','fuckwit',
                          'fudge packer','fudgepacker','fuk','fuker','fukker','fukkin','fuks','fukwhit','fukwit','fux','fux0r',
                          'f_u_c_k','gangbang','gangbanged ','gangbangs ','gaylord','gaysex','goatse','God','god-dam','god-damned',
                          'goddamn','goddamned','hardcoresex ','hell','heshe','hoar','hoare','hoer','homo','hore','horniest','horny',
                          'hotsex','jack-off ','jackoff','jap','jerk-off ','jism','jiz ','jizm ','jizz','kawk','knob','knobead','knobed',
                          'knobend','knobhead','knobjocky','knobjokey','kock','kondum','kondums','kum','kummer','kumming','kums','kunilingus',
                          'l3i+ch','l3itch','labia','lmfao','lust','lusting','m0f0','m0fo','m45terbate','ma5terb8','ma5terbate','masochist','master-bate',
                          'masterb8','masterbat*','masterbat3','masterbate','masterbation','masterbations','masturbate',
                          'mo-fo','mof0','mofo','mothafuck','mothafucka','mothafuckas','mothafuckaz','mothafucked ','mothafucker','mothafuckers','mothafuckin','mothafucking ',
                          'mothafuckings','mothafucks','mother fucker','motherfuck','motherfucked','motherfucker','motherfuckers','motherfuckin','motherfucking','motherfuckings','motherfuckka','motherfucks','muff','mutha',
                          'muthafecker','muthafuckker','muther','mutherfucker','n1gga','n1gger','nazi','nigg3r','nigg4h','nigga','niggah','niggas','niggaz','nigger','niggers ','nob','nob jokey','nobhead','nobjocky','nobjokey','numbnuts','nutsack','orgasim ','orgasims ','orgasm','orgasms ','p0rn','pawn','pecker','penis',
                          'penisfucker','phonesex','phuck','phuk','phuked','phuking','phukked','phukking','phuks','phuq','pigfucker','pimpis','piss','pissed','pisser','pissers','pisses ','pissflaps','pissin ','pissing','pissoff ','poop','porn','porno','pornography','pornos','prick','pricks ','pron','pube','pusse','pussi','pussies','pussy','pussys ','rectum','retard','rimjaw','rimming','s hit','s.o.b.','sadist','schlong','screwing','scroat','scrote','scrotum','semen','sex','sh!+','sh!t','sh1t','shag','shagger','shaggin','shagging','shemale','shi+','shit','shitdick','shite','shited','shitey','shitfuck','shitfull','shithead','shiting','shitings','shits','shitted','shitter','shitters ','shitting','shittings','shitty ','skank','slut','sluts','smegma','smut','snatch','son-of-a-bitch','spac','spunk','s_h_i_t','t1tt1e5','t1tties','teets','teez','testical','testicle','tit','titfuck','tits','titt','tittie5','tittiefucker','titties','tittyfuck','tittywank','titwank','tosser','turd','tw4t','twat','twathead','twatty','twunt','twunter','v14gra','v1gra','vagina','viagra','vulva','w00se','wang','wank','wanker','wanky','whoar','whore','willies','willy','xrated','xxx']
        self.chunks = self.extract_chunks(self.sentence, chunk_type="NP")

    def extract_chunks(self, sentence, chunk_type):
        grp1, grp2, chunk_type = [], [], "-" + chunk_type
        for ind, (s, tp) in enumerate(sentence):
            if tp.endswith(chunk_type):
                if not tp.startswith("B"):
                    grp2.append(str(ind))
                    grp1.append(s)
                else:
                    if grp1:
                        yield " ".join(grp1), "-".join(grp2)
                    grp1, grp2 = [s], [str(ind)]
        yield " ".join(grp1), "-".join(grp2)


    # def decipher(self):
    #     if self.isAskingBotInfo():
    #         return "isAskingBotInfo"
    #     elif self.isGreetings():
    #         return "isGreeting"
    #     elif self.isGreetings():
    #         return "isGreeting"
    #     elif self.isbadWords():
    #         return "badWord"
    #     elif self.isNearBy():
    #         return "handleNearby"
    #     # elif self.
    #
    # def isbadWords(self):
    #     for word in self.sentence.split(" "):
    #         if word.lower() in self.bad_words:
    #             return True
    #     return False
    #
    # def isNearBy(self):
    #     res = ""
    #     for chunk in self.chunks:
    #         if chunk.type in ['PP', 'ADVP']:
    #             res += " ".join([w.string for w in chunk.words if w.type in ['RB', 'PRP', 'IN']])
    #             res += " "
    #     res = res.strip()
    #     if res in ['near me', 'around here', 'around', 'near here', 'nearby', 'near by', 'close by', 'close']:
    #         return True
    #     return False
    #
    # def isAskingBotInfo(self):
    #     botinfo = RegexConfig.BotInfoMatcher
    #     for match in botinfo:
    #         matcher = search(match, self.sentence)
    #         if matcher:
    #             return True
    #         return False
    #
    # def isGreetings(self):
    #     string = self.sentence.lower().split(" ")
    #     if len(string) > 3:
    #         return False
    #     greetings = RegexConfig.GreetingsMatcher
    #     for word in greetings:
    #         if word in string or word in string[:3]:
    #             return True
    #     return False
    #
    # def isGoodbye(self):
    #     string = self.sentence.lower().split(" ")
    #     byes = RegexConfig.ByeMatcher
    #     for word in byes:
    #         if word in string:
    #             return True
    #     return False
    #
    # def isYelp(self):
    #     verbs = self.find_verb()
    #     noun_phrases = self.findNounPhrase()
    #     # If match key verbs
    #     yelpVerbs = ['eat', 'drink', 'find', 'display', 'get']
    #     for verb in verbs:
    #         if verb.lower() in yelpVerbs:
    #             if "news" in noun_phrases or "information" in noun_phrases and "news stand" not in noun_phrases and "newsstand" not in noun_phrases:
    #                 return False
    #
    #             yelpNouns = ['restaurant', 'food', 'drink', 'shop', 'store', 'bar', 'pub']
    #             for noun in yelpNouns:
    #                 if noun in noun_phrases:
    #                     return True
    #
    #     # If match question/command structure
    #     # "is there" + noun phrase
    #     if "is there" in self.sentence.string \
    #             or "are there" in self.sentence.string \
    #                     and noun_phrases != "":
    #         return True
    #
    #     # noun phrase + "near by"
    #     nearby = self.isNearBy()
    #     if noun_phrases != "" and nearby:
    #         return True
    #
    #     m = search('{fine|find|get|find|show|search} { *+ }', self.sentence)
    #     # Sometimes Speech to Text misunderstood "find" as "fine"
    #     if len(m) > 0:
    #         return True
    #
    #     return False
    #
    # def findNounPhrase(self):
    #     res = ""
    #     for chunk in self.chunks:
    #         if chunk.type == 'NP':
    #             res += " ".join([w.string for w in chunk.words if w.type not in ['PRP', 'DT']])
    #             res += " "
    #     for verb in ['find', 'get', 'show', 'search']:
    #         res = res.replace(verb, "")
    #     return res
    #
    # def removePunctuations(self):
    #     return self.sentence.translate(None, string.punctuation)
    #
    # def getUserTime(self, user=None):
    #     user_tz = user.timezone
    #     offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    #     server_tz = offset / 60 / 60 * -1
    #     time_diff = user_tz - server_tz
    #     server_now = datetime.datetime.now()
    #     return server_now + datetime.timedelta(hours=time_diff)
    #
    # def find_verb(self):
    #     result = []
    #     for chunk in self.chunks:
    #         if chunk.type in ['VP']:
    #             strings = [w.string for w in chunk.words if w.type in ['VB', 'VBP']]
    #             result.extend(strings)
    #     return result
    #
    # def findProperNoun(self):
    #     for chunk in self.chunks:
    #         if chunk.type == 'NP':
    #             for w in chunk.words:
    #                 if w.type == 'NNP':
    #                     return w.string
    #     return None
    #
    # def getOneOf(self, items):
    #     rand_idx = random.randint(0, len(items) - 1)
    #     return items[rand_idx]
    #
    # def isDismissPreviousRequest(self):
    #     pass

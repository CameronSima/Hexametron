import tweepy
import re
import time
from time import strftime
from itertools import product


'''
Finds tweets that are written in Dactylic Hexameter,
the poetic meter of Classical Greek and Latin Epic
Poetry. Then, the tweets are retweeted in a rhyming
fashion to create an epic "Twitteriad". Inspired by
Pentametron.
'''


COMSUMER_KEY = x
COMSUMER_SECRET = x
ACCESS_KEY = x
ACCESS_SECRET = x
auth = tweepy.OAuthHandler(COMSUMER_KEY, COMSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



# TO DO:

# Put cmu_dict into a database. 
	
# Now, tweets will always rhyme with the same last word.
# Change so they alternate between random rhyme word and
# a rhyme.


def get_dict():
	'''Gets CMU dictionary from a txt file'''
	with open('C:\Projects\Twitter_Bots\hexametron\cmudict.txt', 'r') as f:
		text = f.readlines()	
		lines = [x for x in text if not x.startswith(";;;")]
		return lines
	
def get_stress_dict(lines):
	'''
	Creates python dictionary from CMU txt file,
	pairing each word to its stress notation.
	'''
	
	stress_dict = {}
	for line in lines:
			list = line.split('  ')
			k, v = list[0], list[1:]
			str_value2 = ""
			for x in v:
				str_value2 += x
				stress_dict[k] = remove_letters(str_value2)
	return stress_dict
	
def get_syl_dict(lines):
	'''
	Creates python dictionary from CMU txt file,
	pairing each word to its phonetic spelling
	'''
	
	syl_dict = {}
	str_val = ""
	for line in lines:
		list = line.split(' ')
		k, v = list[0], list[1:]
		v = ' '.join(v)
		syl_dict[k] = v.strip()
	return syl_dict
			
def split_on_num(string):
	'''split on stress notations'''
	string = ''.join(string)
	syls = re.split('0|1 |2 ', string)
	return syls
			
def remove_letters(string):
	'''Single out the stress notations'''
	word_stress = ""
	for x in string:
		if x.isdigit():
			word_stress += str(x)
	return word_stress
	
def remove_punctuation(word):
	punctuation = '!()-[]{};:"\,<>./?@#$%^&*_~'
	punctless = ""
	for char in word:
		if char not in punctuation:
			punctless += char
	return punctless
	
def get_stress_str(tweet):
	'''Return a string of stress notation for a given tweet'''
	punctless = remove_punctuation(tweet)
	tokens = [x.upper() for x in punctless.split()]
	stress_str = ""
	y = [STRESS_DICT[x] for x in tokens if x in tokens]
	for x in y:
		stress_str += x
	return stress_str
		
def meterizer():
	'''Return a list of all acceptable stress notations
	for Epic Hexameter meter as described in
	http://en.wikipedia.org/wiki/Dactylic_hexameter'''

	dactyl = "100"
	spondee = "11"
	trochee = "10"

	acceptable_meter = list(''.join(x) for x in product([dactyl, spondee], 
														[dactyl, spondee],
														[dactyl, spondee],
														[dactyl, spondee],
														[dactyl],
														[trochee, spondee]))
					 
	return acceptable_meter

def get_rhymes(input, level):
	'''Returns a list of words that rhyme with input word.'''
	entries = SYLLABLE_DICT.items()
	syllables = [(word, syl) for word, syl in entries if word == input.upper()]
	rhymes = []
	for (word, syllable) in syllables:
		rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
	return set(rhymes)
	
def get_word_to_rhyme():
	'''
	Gets the last word from the last tweet
	sent from the account.
	'''
	
	status = tweepy.Cursor(api.user_timeline).items(1)
	data = [s.text.encode('utf8') for s in status]
	last_tweet = data[0]
	x = last_tweet.split()
	rhyme_word = x[-1]
	rhyme_word = remove_punctuation(rhyme_word)
	print "WORD TO RHYME IS: " + rhyme_word
	return rhyme_word
	
	
def get_recent_tweets():
	'''
	Gets recent tweets and returns a list of tuples
	containing tweet-text, tweet-id
	'''
	t = []
	tups = []
	for page in tweepy.Cursor(api.home_timeline).pages(5):
		t.extend(page)
		time.sleep(10) # May need to be 60 secs to avoid ratelimit
	print str(len(t)) + " TWEETS FOUND"
	data = [s for s in t]
	for x in data:
		tup = (x.text.encode('utf8'), x.id)
		tups.append(tup)
	print str(len(tups)) + " TWEET TUPLES ADDED"
	return tups
	
def remove_nums(string):
	'''Remove digits from a given string'''
	result = ''.join([x for x in string if not x.isdigit()])
	return result.strip()	
	
# Turn the following into a class?	
def main():
	tups = get_recent_tweets()
	rhyme_word = get_word_to_rhyme()
	tweet_rhymes = []
	length = len(tups)
	tweet_rhymes.extend(get_rhymes(rhyme_word, 3))
	per_tweet_loop(tweet_rhymes, tups, length)
	
def per_tweet_loop(tweet_rhymes, tups, length):
	'''Tests a tweet for suitability to retweet'''
	
	tally = 0
	for tweet_tup in tups:
		if tally >= length:
			main()
		tally += 1
		try:
			only_twt = remove_nums(tweet_tup[0])
			x = remove_punctuation(only_twt).split()
			last_word = x[-1].upper()
			stress_str = get_stress_str(remove_punctuation(only_twt))
			if stress_str in ACCEPTABLE_METER_LIST: #and last_word in tweet_rhymes and 
				print "MATCH FOUND!"
				print tweet_tup
		except:
			pass
	time.sleep(750)
	main()
dict_line_by_line = get_dict()
STRESS_DICT = get_stress_dict(dict_line_by_line)
SYLLABLE_DICT = get_syl_dict(dict_line_by_line)
ACCEPTABLE_METER_LIST = meterizer()

if __name__ == '__main__':
	main()

import random 
import numpy as np
from collections import Counter
import requests
import json

# This function calulates the freq of the (i+1)th 
# word in the whole corpus, where i is the index of 
# the sentence or the word.

def get_rhyme_word(word, count):
	r = requests.get('https://rhymebrain.com/talk?function=getRhymes&maxResults='+str(count)+'&word='+word)
	words = []
	for data in r.json():
		words.append(data['word'])
	return words

def next_word_freq(array, sentence): 
	
	sen_len, word_list = len(sentence.split()), [] 
	
	for i in range(len(array)): 

		# If the sentence matches the sentence in the range (i, i+x) 
		# and the length is less than the length of the corpus, append 
		# the word to word_list. 
		
		if ' '.join(array[i : i + sen_len]).lower() == sentence.lower(): 

			if i + sen_len < len(array) - 1: 
				if(array[i + sen_len].isalpha()):
					word_list.append(array[i + sen_len]) 
	return dict(Counter(word_list)) 


def CDF(d): 
	
	prob_sum, sum_vals = 0, sum(d.values()) 
	
	for k, v in d.items(): 
		
		pmf = v / sum_vals 
		prob_sum += pmf 
		d[k] = prob_sum 
	
	return d 

def main(): 
	print('Loading Corpus...')
	try:
		corpus = open('./en_US.twitter.txt','r', encoding="utf8").read()
	except FileNotFoundError:
		print('Please include the dataset in the current working directory')
		exit()
	l = corpus.split()
	l.reverse()
	print('Loading Finished...')

	sent = input('Insert text here: ')
	x = len(sent)
	n = 10

	rhyme_words = get_rhyme_word(sent,5)
	
	for word in rhyme_words:
		temp_out = '' 
		out = [word]
		perplexity = 0
		logaritmic = 0
		
		for i in range(n): 
			func_out = next_word_freq(l, sent) 

			cdf_dict = CDF(func_out) 
		
			rand = random.uniform(0, 1) 

			try: key, val = zip(*cdf_dict.items()) 
			except: break

			for j in range(len(val)): 
				
				if rand <= val[j]: 
					pos = j 
					break
						
			logaritmic += np.log2(val[pos])
			temp_out = key[pos] 
			out.append(temp_out)
			sent = temp_out 

		logaritmic = logaritmic/n
		perplexity = np.power(2, logaritmic)
		out.reverse()
		print("Perplexity : {}, Output: {}".format(perplexity, ' '.join(out)))

if __name__ == '__main__': 
	main()

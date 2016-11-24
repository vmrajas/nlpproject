import pickle
import sys
import os

start_tag = '<s>' 
end_tag = '<\s>'
main_map = {}

def ngram_cal(count_word, n_of_word, n_of_tag, gram):

	for i in range(len(count_word) - gram + 1):
		ngram_tags = ''
		ngram_word = ''
		for j in range(gram):
			ngram_word += count_word[i + j][0] + ' '
			ngram_tags += count_word[i + j][1] + ' '
			
                if ngram_tags[:len(ngram_tags) - 1] in n_of_tag:
                    n_of_tag[ngram_tags[:len(ngram_tags) - 1]] += 1
	        else:
                    n_of_tag[ngram_tags[:len(ngram_tags) - 1]] = 1
                
                if ngram_word[:len(ngram_word) - 1] in n_of_word:
                    n_of_word[ngram_word[:len(ngram_word) - 1]] += 1
	        else:
                    n_of_word[ngram_word[:len(ngram_word) - 1]] = 1

	return n_of_word, n_of_tag

def accumulate(file, count_word):
	finput = open(file, 'r')

	count_word.append([start_tag, start_tag])
	hindi = {}
	eng = {}

	for line in finput:
                if line != '\n':
			tokens = line.split()
			var = [tokens[0], tokens[2]]
			count_word.append(var)
                else:
			count_word.append([end_tag, end_tag])
			count_word.append([start_tag, start_tag])

	count_word.append([end_tag, end_tag])
	return count_word, hindi, eng

def accumulate1(file, count_word):
	finput = open(file, 'r')

	count_word.append([start_tag, start_tag])
	hindi = {}
	eng = {}

	for line in finput:
                if line != '\n':
			tokens = line.split()
			var = [tokens[1], main_map[tokens[4]]]
			count_word.append(var)
                else:
			count_word.append([end_tag, end_tag])
			count_word.append([start_tag, start_tag])

	count_word.append([end_tag, end_tag])
	return count_word, hindi, eng


if __name__=="__main__":

	map_f = open('mapping.txt')
	a = map_f.readlines()
	for i in a:
		main_map[i.split(':')[0]] = i.split(':')[1].strip()

	file = sys.argv[1]
	file2 = sys.argv[2]
	n_of_word = {} # structure - {'ngram of words':[cnt of n,cnt of n-1]}
	n_of_tag = {} # structure - {'ngram of tags':[cnt of n,cnt of n-1]}
	count_word = [] # structure - [[word,tag],[word,tag]...]


	count_word, hindi, eng = accumulate(file, count_word)
	count_word, hindi, eng = accumulate1(file2, count_word)
        #print count_word 
	for gram in range(2,4):
		n_of_word, n_of_tag = ngram_cal(count_word, n_of_word, n_of_tag, gram)
        print n_of_word
	pickle.dump(n_of_tag,open('monotag.pkl','wb'))
	pickle.dump(n_of_word,open('monoword.pkl','wb'))

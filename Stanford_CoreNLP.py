#call relevant functions
import nltk
import random 
import stanfordcorenlp
import os
import glob
from random import sample
from nltk.tokenize import sent_tokenize
from stanfordcorenlp import StanfordCoreNLP

#tokenize sentences and sample sentences randomly
sentence_list = sent_tokenize (input_file)
selected_number = round(len(sentence_list)/10)
selected_sentence_list = sample (sentence_list, selected_number)#random selection on sentences

#locate the StanfordCoreNLP package
nlp = StanfordCoreNLP(r'C:\Users\Ge Lan\Desktop\pyspace\stanford-corenlp-full-2018-02-27')

#tag and parse sampled sentences
sentence_id=0
for selected_sentence in selected_sentence_list:
    sentence_id=sentence_id+1
    print ('>>>>> sentence',sentence_id,'\n',selected_sentence,'\n')

sentence_id=0
for selected_sentence in selected_sentence_list:
    sentence_id=sentence_id+1
    named_sentences= nlp.ner(selected_sentence)
    print ('>>>>> sentence',sentence_id,' the namerecognizing result is:', '\n', named_sentences,'\n')

sentence_id=0
for selected_sentence in selected_sentence_list:
    sentence_id=sentence_id+1
    tagged_sentences= nlp.pos_tag(selected_sentence)
    print ('>>>>> sentence',sentence_id,' the tagging result is:', '\n', tagged_sentences,'\n')

sentence_id=0    
for selected_sentence in selected_sentence_list:
    sentence_id=sentence_id+1
    parsed_sentences= nlp.parse(selected_sentence)
    print ('>>>>> sentence',sentence_id,' the parsing result is:','\n', parsed_sentences,'\n')

sentence_id=0    
for selected_sentence in selected_sentence_list:
    sentence_id=sentence_id+1
    dependency_sentences= nlp.dependency_parse(selected_sentence)
    print ('>>>>> sentence',sentence_id,' the dependecy result is:','\n', dependency_sentences,'\n')


print ("Done..........")   
nlp.close()

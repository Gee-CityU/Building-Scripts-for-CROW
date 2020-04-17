#run: python script_name.py **/**/*.txt
#purpose: to match a grammatical pattern: noun followed by a preposition, and then to output a concordance line for each case  
#steps to be done: 
#(1) for each file in the dir, make a output corresponding output file to store concordance lines
#(2) process POS tagged files (tagged by Biber tagger); examples are also attached
#(3) build a two-way list based on word and tag; example--> [(customers, nns+nom+++=customers),(word1, tag1), (word2, tag2)...]
#(4) build a three-way list based on word and each tagfield; example -->{[customer,("nns", "nom", "", "", "=customers")] ,[word1,(t11, t12, t13, t14, t15)], [word2, (t21, t22, t23, t24, t25)] ... }
#(5) extract a noun followed by a preposition based on the three-way list; output concordance line for each matched case
#(6) move on to next file in the dir

import sys 
import os 
import glob 
import re 
	
if __name__== '__main__':#initialize the main bock of code
	file_number = 0
	if len(sys.argv) > 1: #if there are arguments given in a command line (example: python test.py **/**/*.txt)
		for arg in sys.argv[1:]:# pass the second argument to this program
			for file in glob.iglob(arg):
				if os.path.isdir(file): # change*
					continue
				with open(file, 'r') as f:# open the file one by one
					file_number = file_number + 1
					try:
						#Question1: why a filename is printed three times? It should just print one time for each file
						print ("Filename: "+f.name) #print whole file name (example: C:/Input/L1/0001a.txt)
						
						file_name = re.sub(r'\.txt',r'',f.name) #remove extension name
						file_name = re.sub(r'\.TXT',r'',file_name)#remove extension name
												
						matches = re.findall('[\w\s]+\/', file_name) #match all filename parts (example: "C:/","Input/", "L1/")
						path = '' #initalize a string variable for path
						for m in matches:
							path = path + m #put all matched filename parts together (example: "C:/Input/L1/")
						
						path = os.path.join(path, "output")# change* #create output path (example: "C:/Input/L1/output/")
						if not os.path.exists(path):
							os.makedirs(path) #make an output dir based on the path
						
						file_name = re.sub(r'[\w\s]+\/',r'',file_name)# get file's name w/o extension (example: 0001a)
						
						output_file_name = os.path.join(path, file_name + ".txt") # change* #output file path + file's name w/o extension + extension (example: C:/Input/L1/output/0001a.txt)
						output_file = open(output_file_name, "w")#open the output file with the exact path from output_file_name
						
						output_file.write("Filename: " + str (file_name) + "\n")
					
						# The extraction of noun phrase patterns starts here ----------------------------------------------------------------------------------------------------------------
						#step 1 (re-)initialize variables 
						lines = []
						line_parts=[]
						word = ''
						tag = ''
						word_tag_unit = []
						word_tag_list=[]	
						word_tagfield_list = []
						tagfields = []
						wordcount = 0
						output_string=''
						
						
						#step 2: try to build a two-way list 
						lines= f.read().split('\n') #build a line list based on the current file (line example: customers ^nns+nom+++=customers)
						for line in lines:
							line_parts = line.split(" ^")#split the word and tag in each line to two parts (example: "customers" "nns+nom+++=customers")
							if (len(line_parts) > 1): # change*
								word = line_parts[0] # "customers"
								tag = line_parts[1] # "nns+nom+++=customers"
							else:
								# The line did not contain an " ^" match
								continue
							
							# Question 2: why it got a problem on "index out of range" here!
							word_tag_unit = (word, tag) # build a word-and-tag unit(customers, nns+nom+++=customers)
							word_tag_list.append(word_tag_unit) #build a two-way list; example [(customers, nns+nom+++=customers),(word1, tag1), (word2, tag2)...]
						
						#Question3: why the (word_tag_list) can only be output to in first file in the current working directory? 
						#output_file.write(str(word_tag_list)) #try to debug here but failed 
							
						
						#step 3: count word in a file 
							#try to count word in the file 
							if not re.match("\.|\,|\:|\;|\`|\"|\'|\?|\!", word): #count word if it is not punctuations
								wordcount = wordcount + 1
						print ("Total token: ", wordcount)
						output_file.write("Total token: " + str (wordcount) + "\n") # change*
						
					
						#step 4: build a three-way list 
						word_tagfield_list = [] #this is a variable to store three-way list 
						x = 0 #the case number for element in the two-way array build in step 2
						
						for each in word_tag_list: #each element in the two-way list [(customers, nns+nom+++=customers),(word1, tag1), (word2, tag2),...]
							tagfields = word_tag_list[x][1].split("+") #example: split the tag "nns+nom+++=customers" to five tagfields: "nns", "nom", "", "", "=customers"
							word_tag_unit_new = (word_tag_list[x][0], tagfields) # [customer,("nns", "nom", "", "", "=customers")] 
							word_tagfield_list.append(word_tag_unit_new)# {[customer,("nns", "nom", "", "", "=customers")] ,[word1,(t11, t12, t13, t14, t15)], [word2, (t21, t22, t23, t24, t25)] ... }
							x = x +1 #move from the first element in the two-way list to the next one
						
						#step 5: match a specific noun phrase pattern (noun followed by a preposition), and output concordanceline in a output file to manual check.
						i=0 #case number for element in the three-way list
						for eachone in word_tagfield_list: #for each element in the three_D array 
						
							# 1-ADJ
							if re.match('jj(b|r|t)?', word_tagfield_list[i][1][0]) and re.match('atrb', word_tagfield_list[i][1][1]): 
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_ADJ:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4:
									output_array = ["NOUN_ADJ:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_ADJ:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0] + ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array) 
								output_file.write(output_string + "\n")
							
							# 2-Noun-noun sequence
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match('nn|nns|nvbg', word_tagfield_list[i+1][1][0]):
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_NOUN:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_NOUN:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_NOUN:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0] + ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array) 
								output_file.write(output_string + "\n")
							
							# 3-PP-of as postmodifier
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("in", word_tagfield_list[i+1][1][0]) and re.match("of|Of|OF", word_tagfield_list[i+1][0]):
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_PP_OF:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: # for the last five elements, only output the five words before the noun
									output_array = ["NOUN_PP_OF:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_PP_OF:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0] + ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")
							
							# 4-PP-Other as postmodifier
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("in", word_tagfield_list[i+1][1][0]) and not re.match("of|Of|OF", word_tagfield_list[i+1][0]):
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_PP_OTHER:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4:
									output_array = ["NOUN_PP_OTHER:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_PP_OTHER:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0] + ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")
							
							# 5-ed clause as postmodifier
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("vwbn", word_tagfield_list[i+1][1][0]) and re.match("xvbn", word_tagfield_list[i+1][1][3]): 
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_ED:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_ED:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_ED:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0] + ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")
							
							# 6-ing clause as postmodifier
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("vwbg", word_tagfield_list[i+1][1][0]) and re.match("xvbg", word_tagfield_list[i+1][1][3]): 
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_ING:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_ING:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_ING:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0] + ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")
								
							# 7-restrictive relative clause
							# nonrestrictive -->regex 
							# zero-relativiser --> manual 
							if re.match("rel", word_tagfield_list[i][1][1]): 
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_REL:", "<<<" + word_tagfield_list[i][0]+ ">>>", word_tagfield_list[i+1][0], word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_REL:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" +word_tagfield_list[i-1][0], word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_REL:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], "<<<" + word_tagfield_list[i-1][0], word_tagfield_list[i][0]+ ">>>", 
									word_tagfield_list[i+1][0], word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")	
							
							# 8-Noun complement clause
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("tht", word_tagfield_list[i+1][1][0]) and re.match("ncmp", word_tagfield_list[i+1][1][1]): #match a pattern based on the tags "noun + preposition"; (nn, ns, np --> nouns)(in --> preposition)	
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_COMP:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_COMP:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0],word_tagfield_list[i-1][0], "<<<" +word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_COMP:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")		
							
							# 9-Infinitive clause 
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("to", word_tagfield_list[i+1][1][0]): 
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_TO:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_TO:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0],word_tagfield_list[i-1][0], "<<<" +word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_TO:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0]+ ">>>", word_tagfield_list[i+2][0], word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")		
							
							# 10-Prepostion + -ing clause as postmodifier
							if re.match('nn|nns|nvbg', word_tagfield_list[i][1][0]) and re.match("in", word_tagfield_list[i+1][1][0]) and re.match('(\w+)ing', word_tagfield_list[i+2][0]): 
								if i==0 or i==1 or i==2 or i==3 or i==4: 
									output_array = ["NOUN_PPING:", "<<<" + word_tagfield_list[i][0], word_tagfield_list[i+1][0], word_tagfield_list[i+2][0]+ ">>>", word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0]]
								
								elif i == wordcount or i == wordcount-1 or i == wordcount-2 or i == wordcount-3 or i == wordcount-4: 
									output_array = ["NOUN_PPING:", word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0],word_tagfield_list[i-1][0], "<<<" +word_tagfield_list[i][0] + ">>>"]
								
								else: 
									output_array = ["NOUN_PPING:", word_tagfield_list[i-8][0], word_tagfield_list[i-7][0], word_tagfield_list[i-6][0], word_tagfield_list[i-5][0], word_tagfield_list[i-4][0], word_tagfield_list[i-3][0], word_tagfield_list[i-2][0], word_tagfield_list[i-1][0], "<<<" + word_tagfield_list[i][0], 
									word_tagfield_list[i+1][0], word_tagfield_list[i+2][0]+ ">>>", word_tagfield_list[i+3][0], word_tagfield_list[i+4][0], word_tagfield_list[i+5][0],word_tagfield_list[i+6][0], word_tagfield_list[i+7][0], word_tagfield_list[i+8][0], word_tagfield_list[i+9][0], word_tagfield_list[i+10][0]]
								
								output_string = " ".join(output_array)
								output_file.write(output_string + "\n")
							
							i = i+1 #go to the next element in the three-way list 
					
					except:
						print ("something got wrong?")
						print(f.name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))

print ("\n")
print ("There are ", file_number, " files in the corpus.")
print ("Done")
			



			

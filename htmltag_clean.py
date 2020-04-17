import sys 
import os 
import glob 
import re 
		
if __name__== '__main__':
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			for file in glob.iglob(arg):  
				if os.path.isdir(file):
					continue
				with open(file, 'r') as f
					try:
						print ("The file name is: "+f.name)
						
						file_name = re.sub(r'\.txt',r'',f.name)
						file_name = re.sub(r'\.TXT',r'',file_name)
												
						matches = re.findall('[\w\s]+\/', file_name) 
						path = '' #initalize a string variable for path
						for m in matches:
							path = path + m
						
						path = os.path.join(path, "HTML_Cleaned")
						if not os.path.exists(path):
							os.makedirs(path)
						
						file_name = re.sub(r'[\w\s]+\/',r'',file_name)
						
						output_file_name = os.path.join(path, file_name + ".txt")
						output_file = open(output_file_name, "w")
						
						#cleaning HTML tags
						text = f.read() 
						text_clean = re.sub("<[^>]*>", "" ,text)
						output_file.write(text_clean)
							
					except:
						print ("something got wrong?")
						print(f.name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))
print ("done")
			



			

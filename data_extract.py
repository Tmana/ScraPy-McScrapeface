import os, glob, re, string, copy, sys
from tqdm import tqdm

hard_path = "C:/Users/trobart/Desktop/Deeds/extracted_data/"
# data_path = input("Please enter filepath to OCR CSV:")

os.chdir(hard_path)


instrument_regex = r'^[^0-9]*([0-9]+).*$|\1|'
date_regex = r"\d{1,2}\/\d{1,2}\/\d{4}" 
consideration_regex = r'\$?\d+[(,|\.| )\d]+'
#test2_parcel_regex = r"\w[^"]\d(?:[^"][^ ]\d[^"](?:[^"]\d[^ ]++)++)++"
parcel_regex = re.compile('\w[^"]\d(?:[^"][^ ]\d[^"](?:[^"]\d[^ ]+)+)+')
alphanum_regex = re.compile('[\W_]+')

inputs = input("enter new identifier for output file: ")
file = 'C:/Users/trobart/Desktop/Deeds/final_deed_data/final_data{0}.csv'.format(inputs)
output = open(file, 'w')

# Create headers for output file
instrument_num =  "Instrument Number" 
date 		   =  "Date of Record"
title_agent    =  "Title Agent"
title_company  =  "Title Company"
company_address = "Title Co. Address"
parcel_num     =  "Parcel ID Number"
consideration  =  "Consideration"
deed_type 	   =  "Deed Type"
county 		   =  ""
agent_exists   =  ""
next_line	   =  ""
last_num 	   =  ""



# counts for data presence out of total writes
total_count = 0
hit_count = 0


try:
	for filename in glob.glob("*.csv"):
		county = re.findall(r'\s(\w+)$', filename)[0]
		file = open(hard_path + filename)
		num_lines = sum(1 for line in file)
	
		file = open(hard_path + filename)
		# instantiate progress bar
		with tqdm(total = num_lines) as pbar:

			# main loop
			for line in file:

				#update progress bar
				pbar.update(1)


				# next line cases
				if next_line == "Parcel Number" and "inst. number" not in line.lower() and "$" not in line.lower() and len(line) < 50:
					if not not re.findall(parcel_regex, line) and ")" not in re.findall(parcel_regex, line) and re.findall(parcel_regex, line)[0][0:4] != "2015" and re.findall(parcel_regex, line)[0][0:4] != "2016" and re.findall(parcel_regex, line)[0][0:4] != "2017":
						parcel_num = re.findall(parcel_regex, line)
						#print("boop1", parcel_num, line)
						hit_count += 1
						last_num = parcel_num

				elif next_line == "Title Company":
					if "attn" in line.lower(): 
						title_company = title_agent
						title_agent = line.split(": ")[-1]
						# next_line = 'Title Company Address'
						agent_exists = 'present'
					else:
						title_company = line
						# next_line = 'Title Company Address'

				elif next_line == 'Title Agent' and ":" not in line and agent_exists == '':
					if "address below" in line.lower():
						next_line = 'Title Agent'
					elif "grantee" not in line.lower():
						title_agent = line.lower().rstrip().replace(",", "")
						agent_exists = 'present'
						next_line = "Title Company"

				elif next_line == 'Title Agent' and ":" in line:
					if "address below" in line.lower():
						next_line = 'Title Agent'
					elif len(line.split(": ")) > 1 and len(line.split(": ")[1]) < 20:
						if "title" in line.split(": ")[0].lower():
							title_agent = line
						else:
							title_agent = line.split(": ")[1]
							agent_exists = 'present'
							next_line = "Title Company"
					else:
						next_line = 'Title Agent'


				next_line = ''


				# check for start of a new record
				if "inst. number" in line.lower() or (("number" in line.lower() and "book" in line.lower() and "page" in line.lower() ) or ("bk" in line.lower() and "pg" in line.lower() and "number" in line.lower()) or 'instrument#' in line.lower()):
					
					
					if not not parcel_num: 
						#cleaning the strings, and remove non-alphanumeric characters
						cleaned_parcel = alphanum_regex.sub('', re.sub( r'^[a-z]','', re.sub( r'^[a-z]\s' , '', str(parcel_num).lower().strip('[]\'.-_').replace("\\n", ""), 1))).replace('o', '0')
					
					if not not consideration:
						clean_consideration = alphanum_regex.sub('',str(consideration).replace('.00', ''))
						if any(s == clean_consideration for s in ("10", "100", "1000", "1", "0")):
							clean_consideration = ""

					############################
					# writing new line to file #
					############################

					output.write("\"" + instrument_num + "\"" + ',' + date + ',' + cleaned_parcel + ',' + clean_consideration.rstrip() + ',' + title_agent.rstrip().replace(",","") + ',' + title_company.rstrip().replace(",", "") + ',' + county + ',' + deed_type + '\n')
					total_count += 1

					############################



					# clearing values for next line (to prevent repeats)
					instrument_num = date = title_agent = title_company = parcel_num = consideration = next_line = deed_type = agent_exists = next_line = cleaned_parcel = clean_consideration = ''
						
					if not not re.findall(instrument_regex, line)[0]:
						instrument_num = re.findall(instrument_regex, line)[0]

					if re.findall(date_regex, line):
						date = re.findall(date_regex, line)[0]	
					# now pull instrument number and date from this new record
				

				# Parcel ID number extraction handling
				elif ("tax id" in line.lower() or "pi#" in line.lower() or "pin" in line.lower() or "id #" in line.lower() or "id#" in line.lower() or "parcel" in line.lower() or 'folio' in line.lower()) and (not not re.findall(parcel_regex, line.lower())):
					#print("foo5", not not re.findall(parcel_regex, line.lower()) , re.findall(parcel_regex, line))
					parcel_num = re.findall(parcel_regex, line)
					hit_count += 1
					next_line = ''
				elif ("tax id" in line.lower() or "pi#" in line.lower() or "pin" in line.lower() or "id #" in line.lower() or "id#" in line.lower() or "parcel" in line.lower() or 'folio' in line.lower()):
					next_line = "Parcel Number"
				else:
					# final bin for selecting edge cases and filtering out junk
					if last_num != re.findall(parcel_regex, line) and ":" not in line.lower() and "com" not in line.lower() and "fl-ft" not in line.lower() and "ftpa" not in line.lower() and not not re.findall(parcel_regex, line.lower()) and len(re.findall(parcel_regex, line.lower())) == 1 and len(re.findall(parcel_regex, line.lower())[0]) > 17 and len(line) < 50:
						parcel_num = re.findall(parcel_regex, line)
						#print("boop 2!", parcel_num, line)
						hit_count += 1
						last_num = parcel_num					
						next_line = ''



				## Title Agent/ Agency extraction handling ##
				if (("prepared by" in line.lower() or "prepared bv" in line.lower()) or "return to" in line.lower()) and (":" in line and len(line) < 60): # exception for common mis-read by OCR of 'by' as 'bv'
					if len(line.split(": ")) > 1 and len(line.split(": ")[-1]) < 20:
						
						#testing line, remove
						
						if agent_exists == '':
							if "address below" in line.lower():
								next_line = 'Title Agent'
							elif line.split(": ")[1].lower().rstrip().replace(",", "") != "grantee":
								title_agent = line.split(": ")[1].lower().rstrip().replace(",", "")
								agent_exists = 'present'
								next_line = "Title Company"
					else:
						next_line = 'Title Agent'

				if "attention: " in line.lower() or ("name: " in line.lower() and  "printed" not in line.lower()) and len(line) < 60:

					if agent_exists == '':
						title_agent = line.split(": ")[1].lower().rstrip().replace(",", "")
						agent_exists = 'present'
						next_line = ''
					



				## consideration extraction ##
				if "consideration:" in line.lower() or "purchase price:" in line.lower() and (not not re.findall(consideration_regex, line) and '10.00' not in line.lower()):
					if '10.00' not in line.lower():
						try:
							if len(max(re.findall(consideration_regex, line))) > 4:
								consideration = max(re.findall(consideration_regex, line))
						except:
							pass
				elif "consideration" in line.lower()  or "sales price" in line.lower() and (not not re.findall(consideration_regex, line) and '10.00' not in line.lower()):
					if '10.00' not in line.lower():
						try:
							if len(max(re.findall(consideration_regex, line))) > 4:
								consideration = max(re.findall(consideration_regex, line))
						except:
							pass
				
				## Deed type extraction handling ##
				if "deed" in line.lower():
					if "special" in line.lower():
						deed_type = "Special Warranty"
					elif "warranty" in line.lower():
						deed_type = "Warranty"
					elif "quit" in line.lower():
						deed_type = "Quit Claim"
					elif "tax" in line.lower():
						deed_type = "Tax Deed"
					else:
						deed_type = "Unknown"

				if 'deceased' in line.lower() or 'certificate of release' in line.lower():
					deed_type = "Release/Legal Transfer"

				if "certificate of title" in line.lower():
					deed_type = "Certificate of Title"
		file.close()	


except KeyboardInterrupt:
		print("[*] Exiting...")
		sys.exit(1)


print("Extraction Complete!", "Proportion of records with parcel extracted = " , hit_count , "/", total_count, "=" , hit_count/total_count )
output.close()

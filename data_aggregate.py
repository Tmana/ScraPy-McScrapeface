import os, glob, re, string

# Pulls the fields we want from the processed and OCR'ed csv files, and put them in a tidy data format
# Currently pulls the following fields:

# Instrument Number, Title Agent, Title Company/Agency, Date of closing, Listing Agent, Buying Agent, Parcel Number, and consideration/purchase amount.

hard_path = "C:/Users/trobart/Desktop/Deeds/extracted_data/"
# data_path = input("Please enter filepath to OCR CSV:")

os.chdir(hard_path)

#regex to pull fields from specific lines
printable_char_regex = r"[ -~]"
instrument_regex = r"s|^[^0-9]*([0-9]+).*$|\1|"
date_regex = r"\d\d/[^ ]+" 
parcel_regex = r"[\d\.,/]+"



# Choose filepath for output
output = open('C:/Users/trobart/Desktop/Deeds/final_deed_data/final_data{1}.csv', 'w').format(input("enter new identifier for output file: "))

# Create headers for output file
instrument_num =  "Instrument Number" 
date 		   =  "Date of Record"
title_agent    =  "Title Agent"
title_company  =  "Title Company"
company_address = "Title Co. Address"
parcel_num     =  "Parcel ID Number"
consideration  =  "Consideration"
deed_type 	   =  "Deed Type"
agent_exists   =  ""
next_line	   =  ""



try:
	for filename in glob.glob("*.csv"):
		data = open(hard_path + filename)
		# data = file.read()
		# file.close()

		for line in data:
			# check for start of a new record
			if "inst. number" in line.lower() or ("number" in line.lower() and "book" in line.lower() and "page" in line.lower() ) or 'instrument#' in line.lower():

				# write current line to file, and clear current values
				output.write(instrument_num + ',' + date + ',' + title_agent.rstrip() + ',' + title_company.rstrip()  + ',' + company_address.rstrip() +','+ parcel_num.replace(',', '.').rstrip() + ',' + consideration.rstrip().replace(",","") + ',' + deed_type + '\n' )
				instrument_num = date = title_agent = title_company = parcel_num = consideration = next_line = deed_type = agent_exists = ''

				# now pull instrument number and date from this new record
				instrument_num = re.findall(instrument_regex, line)[0]

				# Note: This pulls date of when record was filed in clerk, not sure if deed signature date is desired instead.
				if re.findall(date_regex, line):
					date = re.findall(date_regex, line)[0]

			# check for "next_line" variable

			if next_line == "Title Company":
				if "attn" in line.lower(): 
					title_company = title_agent
					title_agent = line.split(": ")[-1]
					next_line = 'Title Company Address'
					agent_exists = 'present'
				else:
					title_company = line
					next_line = 'Title Company Address'

			elif next_line == 'Title Agent' and ":" not in line and agent_exists == '':
				
				title_agent = line
				agent_exists = 'present'
				next_line = "Title Company"

			elif next_line == 'Title Agent' and ":" in line:
				if len(line.split(": ")) > 1 and len(line.split(": ")[-1]) < 20:
					title_agent = line.split(": ")[1]
					agent_exists = 'present'
					next_line = "Title Company"
				else:
					next_line = 'Title Agent'

			elif next_line == 'Title Company Address':
				company_address = line
				next_line = ' '
			elif next_line == "Parcel Number":
				if not not re.findall(parcel_regex, line) and re.findall(parcel_regex, line)[0] != '.':
					parcel_num = re.findall(parcel_regex, line)[0]
				elif not not re.findall(parcel_regex,line) and re.findall(parcel_regex, line)[0] == '.':
					if len(re.findall(parcel_regex, line)) > 1:
						if len(re.findall(parcel_regex, line)[1]) > 6:
							parcel_num = re.findall(parcel_regex, line)[1]
				next_line = ' '



			if ("prepared by" in line.lower() or "prepared bv" in line.lower()) or "return to" in line.lower() and ":" in line and agent_exists == '': # exception for common mis-read by OCR of 'by' as 'bv'
				if len(line.split(": ")) > 1 and len(line.split(": ")[-1]) < 20:
					title_agent = line.split(": ")[1]
					agent_exists = 'present'
					next_line = "Title Company"
				else:
					next_line = 'Title Agent'

			if "attention: " in line.lower() or ("name: " in line.lower() and "printed" not in line.lower()) and agent_exists == '':
				title_agent = line.split(": ")[1]
				agent_exists = 'present'
				next_line = ' '

			if "address: " in line.lower():
				company_address = line.split(": ")[1]

			if "consideration:" in line.lower() or "purchase price:" in line.lower():
				consideration = line.split(":")[-1]
			elif "consideration" == line.split(" ")[0].lower()  or "sales price" in line.lower() and line.split("$")[-1][0].isdigit():
				consideration = line.split("$")[-1]

  



			#Parcel # extraction handling
			if "parcel" in line.lower() and not not re.findall(parcel_regex, line) and re.findall(parcel_regex, line)[0] != '.': # checks that the parcel number is present in the current line.
				if len(re.findall(parcel_regex, line)) > 1:
					if len(re.findall(parcel_regex, line)[1]) > 5:
						parcel_num = re.findall(parcel_regex, line)[1]
					
				elif len(re.findall(parcel_regex, line)[0]) > 5:
					parcel_num = re.findall(parcel_regex, line)[0]
				
			elif "parcel" in line.lower() and not not re.findall(parcel_regex, line) and re.findall(parcel_regex, line)[0] == '.':
				if len(re.findall(parcel_regex, line)) > 1:
					if len(re.findall(parcel_regex, line)[1]) > 5:
						parcel_num = re.findall(parcel_regex, line)[1]
				else:
					next_line = "Parcel Number" # parcel number is on next line instead

			if "pi#" in line.lower() or "id #" in line.lower() or "id#" in line.lower():
				parcel_num = line.split("#")[1]
			elif "parcel id" in line.lower():
				if len(re.findall(parcel_regex, line)) > 1:
					if len(re.findall(parcel_regex, line)[1]) > 5:
						parcel_num = re.findall(parcel_regex, line)[1]
					
				elif not not re.findall(parcel_regex, line) and len(re.findall(parcel_regex, line)[0]) > 5:
					parcel_num = re.findall(parcel_regex, line)[0]


			#Deed type extraction handling
			if "deed" in line.lower():
				if "special" in line.lower():
					deed_type = "Special Warranty"
				elif "warranty" in line.lower():
					deed_type = "Warranty"
				elif "quit" in line.lower():
					deed_type = "Quit Claim"
				elif "tax" in line.lower():
					deed_type = "Tax"
				else:
					deed_type = "Unknown"

			if 'deceased' in line.lower() or 'certificate of release' in line.lower():
				deed_type = "Release/Legal Transfer"

			if "certificate of title" in line.lower():
				deed_type = "Certificate of Title"

except KeyboardInterrupt:
		print("[*] Exiting...")
		sys.exit(1)


print("Extraction Complete!")
output.close()
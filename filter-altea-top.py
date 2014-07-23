

f_domains = open('domains.txt' , 'r')
f_filter = open('alexa-top-1000.txt', 'r')
filter_arr = f_filter.readlines()
f_out = open('domains-filtered.txt' , 'w')

filtered = False
for line_domain in f_domains.readlines():
	for line_filter in filter_arr:
		if(line_domain.find(line_filter) != -1):
			filtered = True
			break
	
	if(filtered != True):
		f_out.write(line_domain)

	filtered = False
			

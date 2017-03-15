#!/usr/bin/env python

class History:
	fname = "downloaded.txt"

	def init_downloaded_title(self):

		with open(self.fname) as f:
			content = f.readlines()
			content = [x.strip() for x in content]
			f.close

		print ('Historical downloaded titles: ', content)
		
		return content

	def add_downloaded_title(self, title):
		print ('updating downloaded.txt... ', title)
		
		with open(self.fname, "a") as f:
			f.write(title + '\n')
			f.close

		print ('updating downloaded.txt...done!')

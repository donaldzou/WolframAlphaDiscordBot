from urllib.parse import urldefrag, urlencode, urlparse


def poc(question):

	import requests
	from hashlib import md5
	from urllib.parse import urlsplit, urlencode, unquote_plus

	headers = {"User-Agent": "Wolfram Android App"}
	APPID = "3H4296-5YPAGQUJK7" # Mobile app AppId
	SERVER = "api.wolframalpha.com"
	SIG_SALT = "vFdeaRwBTVqdc5CL" # Mobile app salt

	s = requests.Session()
	s.headers.update(headers)

	def calc_sig(query):
		"""
		Calculates WA sig value(md5(salt + concatenated_query)) with pre-known salt
		
		@query
		In format of "input=...&arg1=...&arg2=..."
		"""
		

		params = list(filter(lambda x: len(x) > 1, list(map(lambda x: x.split("="), query.split("&"))))) # split string by & and = and remove empty strings
		params.append(["podstate", "Show+all+steps"])
		params.sort(key = lambda x: x[0]) # sort by the key

		s = SIG_SALT
		# Concatenate query together

		for key, val in params:
				s += key + val

		s = s.encode("utf-8")
		return md5(s).hexdigest().upper()

	def craft_signed_url(url):
		"""
		Craft valid signed URL if parameters known
		
		@query
		In format of "https://server/path?input=...&arg1=...&arg2=..."
		"""

		(scheme, netloc, path, query, _) = urlsplit(url)
		_query = {"appid": APPID}

		_query.update(dict(list(filter(lambda x: len(x) > 1, list(map(lambda x: list(map(lambda y: unquote_plus(y), x.split("="))), query.split("&")))))))
		query = urlencode(_query)
		_query.update({"sig": calc_sig(query)}) # Calculate signature of all query before we set "sig" up.

		final = f"{scheme}://{netloc}{path}?{urlencode(_query)}"
		final = final.replace("Step-by-step", "Step-by-step&podstate=Show+all+steps")
		print("Final+Sig: "+final)
		return final

	def basic_test(query_part):
		"""
		Simple PoC

		@query_part
		Example is "input=%url_encoded_string%&arg1=...&arg2=..."
		https://products.wolframalpha.com/api/documentation/#formatting-input
		"""
		link = f"https://{SERVER}/v2/query?{query_part}"
		
		r = s.get(craft_signed_url(f"https://{SERVER}/v2/query?{query_part}"))
		if r.status_code == 200:
			return r.text
		else:
			raise Exception(f"Error({r.status_code}) happened!\n{r.text}")

	data = basic_test(question)
	return data
	# basic_test("input=y%27+%3D+y%2F%28x%2By%5E3%29&podstate=Solution__Step-by-step+solution&format=plaintext&output=json")
print(poc("input=oxidation+states+of+chromium%28III%29+chloride&podstate=Step-by-step&scantime=20.0&&format=image&ip=8.8.8.8&output=json"))


# print(("https:\/\/www5a.wolframalpha.com\/api\/v1\/recalc.jsp?id=MSPa143130ff5g79d90015600004gg4ci29f06bcf7d7360937098865079620&output=JSON"))
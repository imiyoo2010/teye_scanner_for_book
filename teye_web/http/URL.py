#coding=utf-8
'''
URL.py
'''
import os
import urlparse
import urllib
import cgi
import re
import copy
import sys

from misc.common import is_equal_list
from querystring import querystring

from encodings import DEFAULT_ENCODING


# last upd: 14 Jul 2011
# taken from http:#en.wikipedia.org/wiki/List_of_Internet_top-level_domains
GTOP_LEVEL_DOMAINS = set(('ac','ad','ae','aero','af','ag','ai','al','am',
	'an','ao','aq','ar','arpa','as','asia','at','au','aw','ax','az','ba',
	'bb','bd','be','bf','bg','bh','bi','biz','bj','bm','bn','bo','br','bs',
	'bt','bv','bw','by','bz','ca','cat','cc','cd','cf','cg','ch','ci','ck',
	'cl','cm','cn','co','com','coop','cr','cs','cu','cv','cx','cy','cz',
	'dd','de','dj','dk','dm','do','dz','ec','edu','ee','eg','er','es','et',
	'eu','fi','fj','fk','fm','fo','fr','ga','gb','gd','ge','gf','gg','gh',
	'gi','gl','gm','gn','gov','gp','gq','gr','gs','gt','gu','gw','gy','hk',
	'hm','hn','hr','ht','hu','id','ie','il','im','in','info','int','io',
	'iq','ir','is','it','je','jm','jo','jobs','jp','ke','kg','kh','ki',
	'km','kn','kp','kr','kw','ky','kz','la','lb','lc','li','lk','lr','ls',
	'lt','lu','lv','ly','ma','mc','md','me','mg','mh','mil','mk','ml',
	'mm','mn','mo','mobi','mp','mq','mr','ms','mt','mu','museum','mv','mw',
	'mx','my','mz','na','name','nc','ne','net','nf','ng','ni','nl','no',
	'np','nr','nu','nz','om','org','pa','pe','pf','pg','ph','pk','pl','pm',
	'pn','pr','pro','ps','pt','pw','py','qa','re','ro','rs','ru','rw','sa',
	'sb','sc','sd','se','sg','sh','si','sj','sk','sl','sm','sn','so','sr',
	'st','su','sv','sy','sz','tc','td','tel','tf','tg','th','tj','tk','tl',
	'tm','tn','to','tp','tr','travel','tt','tv','tw','tz','ua','ug','uk',
	'us','uy','uz','va','vc','ve','vg','vi','vn','vu','wf','ws','xxx','ye',
	'yt','za','zm','zw'))

def parse_qs(url_encoded_string, ignoreExceptions=True,encoding=DEFAULT_ENCODING):
	'''
	'''
	parsed_qs = None
	result = querystring(encoding=encoding)

	if url_encoded_string:
		try:
			parsed_qs = cgi.parse_qs(url_encoded_string,keep_blank_values=True,strict_parsing=False)
		except Exception:
			if not ignoreExceptions:
				raise 'Strange things found when parsing query string: "%s"' % url_encoded_string
		else:
			for p, v in parsed_qs.iteritems():
				if type(v) is not list:
					v = [v]
				result[p] = v

	return result

class URL(object):
	'''
	'''
	ALWAYS_SAFE = "%/:=&?~#+!$,;'@()*[]|"
	
	def __init__(self,url,encoding=DEFAULT_ENCODING):
		'''
		'''
		self._already_calculated_url = None
		self._changed = True
		self._encoding = encoding
		'''
		当URL没有协议的时候，urlparse不能准确识别，因此需要区分处理
		1.www.watscan.com
		2.www.watscan.com/index.php?id=1=====>error
		'''
		if not url.startswith("https://") and not url.startswith("http://"):
			#默认设置为http
			url = "http://" + url

		urlres= urlparse.urlparse(url)

		self.scheme 	= urlres.scheme
		if urlres.port is None:
			self.port = 80
		else:
			self.port 		= urlres.port
		#www.watscan.com:80
		if urlres.netloc.find(":")>-1:
			self.netloc 	= urlres.netloc
		else:
			self.netloc = urlres.netloc+":"+str(self.port)
		self.path 		= urlres.path
		self.params 	= urlres.params
		self.qs 		= urlres.query
		self.fragment 	= urlres.fragment

		if not self.netloc:
				raise ValueError, 'Invalid URL "%s"' % url

	@classmethod
	def from_parts(cls, scheme, netloc, path, params, qs, fragment, encoding=DEFAULT_ENCODING):
		"""
		"""
		data = (scheme, netloc, path, params, qs, fragment)
		url_str = urlparse.urlunparse(data)
		return cls(url_str, encoding)

	def urljoin(self,relative):
		'''
		'''
		jurl =  urlparse.urljoin( self.url_string, relative )
		jurl_obj = URL(jurl, self._encoding)

		return jurl_obj

	def normalize_url(self):
		'''
		'''
		path = os.path.normpath(self.path)
		if path == '/':
			normal_path = '/'
		else:
			flag = path.endswith('/')
			tokens = []
			for p in path.split('/'):
				if not p:
					continue
				elif p != '..':
					tokens.append(p)
				else:
					if tokens:
						tokens.pop()
				normal_path = '/' + '/'.join(tokens) + ('/' if flag else '')

		return URL.from_parts(self.scheme, self.netloc, normal_path, '', '', '', encoding=self._encoding)

	def get_scheme(self):
		'''
		'''
		return self.scheme

	def get_netloc(self):
		'''
		'''
		return self.netloc

	def get_port(self):
		'''
		'''
		return self.port

	def get_host(self):
		'''
		'''
		return self.netloc.split(":")[0]

	def get_domain(self):
		'''
		'''
		return self.netloc.split(":")[0]

	def get_path(self):
		'''
		'''
		return self.path

	def get_fragment(self):
		'''
		'''
		return self.fragment

	def get_uri_string(self):
		'''
		'''
		return URL.from_parts(self.scheme, self.netloc, self.path,None, None, None, encoding=self._encoding).url_string

	def get_param_list(self):
		'''
		'''
		parsedData = None

		parsedData = self.get_querystring().keys()

		return parsedData


	def get_root_domain(self):
		'''
		'''
		def splitAuthority(aAuthority):
			# walk down from right, stop at (but include) first non-toplevel domain
			chunks = re.split("\.",aAuthority)
			chunks.reverse()
			baseAuthority=""
			subdomain=""
			foundBreak = 0

			for chunk in chunks:
				if (not foundBreak):
						baseAuthority = chunk + (".","")[baseAuthority==""] + baseAuthority
				else:
						subdomain = chunk  + (".","")[subdomain==""] + subdomain
				if chunk not in GTOP_LEVEL_DOMAINS:
						foundBreak=1
			return ([subdomain,baseAuthority])

		# def to split URI into its parts, returned as URI object
		def root_domain():
				return splitAuthority(self.get_domain())[1]

		if self.is_ip_address(self.netloc):
			# An IP address has no "root domain"
				return self.netloc
		else:
				return root_domain()
	
	def is_ip_address(self,address):
		'''
		'''
		parts = address.split(".")
		if len(parts) != 4:
				return False

		for item in parts:
				try:
					if not 0 <= int(item) <= 255:
						return False
				except:
					return False

		return True

	@property
	def url_string(self):
		'''
		'''
		calc = self._already_calculated_url

		if self._changed or calc is None:
			data = (self.scheme, self.netloc, self.path,self.params, self.qs, self.fragment)
			dataurl = urlparse.urlunparse(data)
			#https://docs.python.org/2/howto/unicode.html
			try:
				calc = unicode(dataurl)
			except UnicodeDecodeError:
				calc = unicode(dataurl, self._encoding, 'replace')

			self._already_calculated_url = calc
			self._changed = False

		return calc

	def get_url_string(self):
		'''
		'''
		return self.url_string

	def get_baseurl(self):
		'''
		'''
		params = (self.scheme, self.netloc, '', '', '', '')
		return URL.from_parts(*params, encoding=self._encoding)

	def get_querystring( self, ignoreExceptions=True ):
		'''
		'''
		return parse_qs(self.qs, ignoreExceptions=True,encoding=self._encoding)


	def get_filename(self):
		'''
		'''
		return self.path[self.path.rfind('/')+1:]

	def get_ext(self):
		'''
		'''
		fname = self.get_filename()
		extension = fname[ fname.rfind('.') +1 :]
		if extension == fname:
			return ''
		else:
			return extension

	def get_domain_url(self):
		'''
		'''
		res = self.scheme + '://' + self.netloc + '/'
		return URL(res,self._encoding)

	def get_domain_path(self):
		'''
		'''
		if self.path:
			res = self.scheme + '://' + self.netloc + self.path[:self.path.rfind('/') + 1]
		else:
			res = self.scheme + '://' + self.netloc + '/'
		return URL(res, self._encoding)

	def get_dirs(self):
		'''
		Get a list of all directories and subdirectories.
		'''
		res = []
		copy_url =copy.deepcopy(self)

		current_url = copy_url.normalize_url()
		res.append(current_url.get_domain_path())

		if current_url.get_path().count('/')!=0:
			count = 0
			while current_url.get_path().count('/') != 1:
				#此处容易陷入死循环，保证稳定性，限制最大目录深度
				if count >5:
					break
				count = count + 1
				current_url = current_url.urljoin( '../' )
				res.append( current_url )

		return res

	def __eq__(self, other):
		'''
		'''
		self_url	= self.url_string
		other_url	= other.url_string

		if self_url == other_url:

			return True
		else:

			return False

	def __str__(self):
		'''
		'''
		return "%s" % (self.url_string.encode(self._encoding))

	def __repr__(self):
		'''
		'''
		return '<URL for "%s">' % self.url_string.encode(self._encoding)

if __name__=="__main__":
	pass

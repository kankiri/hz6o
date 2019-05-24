class Index:
	def __init__(self, data):
		self.title = data['title'].strip()
		self.subtitle = data['subtitle'].strip()
		self.about = data['about-me'].strip()
		self.email = data['email'].strip()
		self.buttons = data['buttons']
		self.posts = list()
		self.theme = None
		self.section_theme = None
	
	def as_html(self, links):
		indent = self.theme[0].strip('#\n')
		section_theme_string = (u'\u000A' + indent).join(line.rstrip()
			for line in self.section_theme if line[0] != '#')
		sections = list()
		self.posts.sort(key=lambda x: x.order, reverse=True)
		for idx, post in enumerate(self.posts):
			if not post.order:
				continue
			section = section_theme_string.replace('#-lange', post.language)
			if post.language == 'de':
				section = section.replace('#-ltext', 'Mehr...')
			else:
				section = section.replace('#-ltext', 'More...')
			section = section.replace('#-title', post.title)
			section = section.replace('#-imdes', post.image_description)
			section = section.replace('#-arlnk', '/post/' + post.name)
			section = section.replace('#-atype', post.type)
			section = section.replace('#-short', post.teaser)
			if idx <= 5:
				tmp = post.image[:post.image.rfind('.')] + \
						'-s' + post.image[post.image.rfind('.'):]
			else:
				tmp = post.image[:post.image.rfind('.')] + \
						'-xs' + post.image[post.image.rfind('.'):]
			section = section.replace('#-image', tmp)
			sections.append(section)
		result = u'\u000A'.join(line.rstrip() for line
				in self.theme if line[0] != '#')
		result = result.replace('#-descr', self.subtitle)
		result = result.replace('#-title', self.title)
		result = result.replace('#-abtme', self.about)
		result = result.replace('#-btons', u'\u2003'.join(self.buttons))
		result = result.replace('#-email', '@: ' +
				self.email[0:self.email.index('@')] + 
				u'\u00A0' + '+' + u'\u00A0' +
				self.email[self.email.index('@')+1:self.email.rfind('.')] +
				'·' + self.email[self.email.rfind('.')+1:])
		if len(sections) > 0:
			result = result.replace('#-sect1', sections[0])
		if len(sections) > 1:
			result = result.replace('#-sect2', (u'\u000A'+indent).join(sections[1:]))
		else:
			result = result.replace('#-sect2', '')
		if links == 'local':
			result = result.replace('href="//', 'href="http://')
			return result.replace('#-link:', '.').replace('-##', '/index.html').replace('..//', '../')
		else:
			return result.replace('#-link:', '').replace('-##', '')

class Post:
	def __init__(self, name, text=None):
		self.name = name
		self.title = None
		self.language = None
		self.description = None
		self.image = None
		self.image_description = None
		self.teaser = None
		self.draft = None
		self.order = None
		self.type = None
		self.content = list()
		self.theme = None
		self.theme_data = None
		if text is not None:
			self._parse(text)
	
	def _parse(self, text):
		for count, line in enumerate(text):
			if count < 7 and (line.strip()+' ')[0] != '#':
				raise ValueError
			if '<h1>' in line:
				self.title = line.replace('<h1>', '').replace('</h1>', '').strip()
			if 'class="article-type"' in line:
				self.type = line.strip()
			if line.strip() and line[0] != '#':
				self.content.append(line.rstrip())
		self.image = text[0][1:].strip()
		self.image_description = text[1][1:].strip()
		self.description = text[2][1:].strip()
		self.language = text[3][1:].strip()
		self.draft = text[4][1:].strip()
		self.order = text[5][1:].strip()
		self.teaser = text[6][1:].strip()
	
	def as_html(self, links):
		indent = self.theme[0].strip('#\n')
		result = u'\u000A'.join(line.rstrip() for line
				in self.theme if line[0] != '#')
		result = result.replace('#-idscr', self.theme_data['subtitle'])
		result = result.replace('#-ititl', self.theme_data['title'])
		result = result.replace('#-abtme', self.theme_data['about-me'])
		result = result.replace('#-btons', u'\u2003'.join(self.theme_data['buttons']))
		result = result.replace('#-email', '@: ' +
				self.theme_data['email'][0:self.theme_data['email'].index('@')] + 
				u'\u00A0' + '+' + u'\u00A0' +
				self.theme_data['email'][self.theme_data['email'].index('@')+1:self.theme_data['email'].rfind('.')] +
				'·' + self.theme_data['email'][self.theme_data['email'].rfind('.')+1:])
		result = result.replace('#-artcl', (u'\u000A'+indent).join(self.content))
		result = result.replace('#-title', self.title.replace('&shy;', ''))
		result = result.replace('#-descr', self.description)
		result = result.replace('#-imdes', self.image_description)
		result = result.replace('#-image', self.image)
		result = result.replace('#-lange', self.language)
		if links == 'local':
			result = result.replace('href="//', 'href="http://')
			return result.replace('#-link:', '.').replace('-##', '/index.html').replace('..//', '../')
		else:
			return result.replace('#-link:', '').replace('-##', '')

#!/usr/bin/env python3

from app.blog import Post, Index

import json
import logging
import os
import shutil

def copy(src, dst):
	if os.path.isfile(src):
		shutil.copy2(src, dst)
		return None
	if not os.path.exists(dst):
		os.makedirs(dst)
	for elem in os.listdir(src):
		if os.path.isdir(os.path.join(src, elem)):
			copy(os.path.join(src, elem), os.path.join(dst, elem))
		else:
			shutil.copy2(os.path.join(src, elem), os.path.join(dst, elem))

def create_bones(name):
	if os.path.exists(name):
		shutil.rmtree(name)
	os.makedirs(name)
	copy('static', name)
	copy('images', os.path.join(name, 'img'))

def read_file(filename):
	with open(filename, encoding='utf-8') as f:
		return f.readlines()
	logging.debug('Read post ' + filename)

def write_post(post, dir_names):
	for name in dir_names:
		path = os.path.join(name, 'post', post.name)
		os.makedirs(path)
		with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8', newline='') as f:
			f.write(post.as_html(name))

def write_index(index, dir_names):
	for name in dir_names:
		with open(os.path.join(name, 'index.html'), 'w', encoding='utf-8', newline='') as f:
			f.write(index.as_html(name))

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	
	with open('config.json', encoding='utf-8') as config_file:    
		config = json.load(config_file)
	with open(os.path.join('static', 'html', 'blog.html'), encoding='utf-8') as f:
		blog_theme = f.readlines()
	with open(os.path.join('static', 'html', 'post.html'), encoding='utf-8') as f:
		post_theme = f.readlines()
	with open(os.path.join('static', 'html', 'section.html'), encoding='utf-8') as f:
		section_theme = f.readlines()
	
	create_bones('local')
	logging.debug('Created local folder')
	create_bones('public')
	logging.debug('Created public folder')
	
	post_files = os.listdir('posts')
	if 'duplicate-and-overwrite.html' in post_files:
		post_files.remove('duplicate-and-overwrite.html')
	posts = [Post(fn.replace('.html', ''), read_file(os.path.join('posts', fn)))
			for fn in post_files if fn.endswith('.html')]
	for post in posts:
		post.theme = post_theme
		post.theme_data = config
		if post.draft:
			write_post(post, ['local'])
		else:
			write_post(post, ['local', 'public'])
		logging.debug('Written post ' + post.name)
	
	index = Index(config)
	index.theme = blog_theme
	index.section_theme = section_theme
	index.posts = posts
	write_index(index, ['local', 'public'])

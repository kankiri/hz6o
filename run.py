#!/usr/bin/env python3

from app.blog import Post, Index

import json
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
	os.makedirs(os.path.join(name,'css'))
	os.makedirs(os.path.join(name,'img'))
	os.makedirs(os.path.join(name,'js'))
	os.makedirs(os.path.join(name,'post'))
	copy(os.path.join('static','css', 'blog.css'), os.path.join(name, 'css', 'blog.css'))
	copy(os.path.join('static','css', 'post.css'), os.path.join(name, 'css', 'post.css'))
	copy(os.path.join('static','js', 'code.js'), os.path.join(name, 'js', 'code.js'))
	copy('images', os.path.join(name, 'img'))

def read_file(filename):
	with open(filename) as f:
		return f.readlines()

def write_post(post, dir_names):
	for name in dir_names:
		path = os.path.join(name, 'post', post.name)
		os.makedirs(path)
		with open(os.path.join(path, 'index.html'), 'w', newline='') as f:
			f.write(post.as_html(name))

def write_index(index, dir_names):
	for name in dir_names:
		with open(os.path.join(name, 'index.html'), 'w', newline='') as f:
			f.write(index.as_html(name))

if __name__ == '__main__':
	with open('config.json') as config_file:    
		config = json.load(config_file)
	with open(os.path.join('static', 'html', 'blog.html')) as f:
		blog_theme = f.readlines()
	with open(os.path.join('static', 'html', 'post.html')) as f:
		post_theme = f.readlines()
	with open(os.path.join('static', 'html', 'section.html')) as f:
		section_theme = f.readlines()
	
	create_bones('local')
	create_bones('public')
	
	post_files = os.listdir('posts')
	if 'duplicate-and-overwrite.html' in post_files:
		post_files.remove('duplicate-and-overwrite.html')
	posts = [Post(fn.replace('.html', ''), read_file(os.path.join('posts', fn)))
			for fn in post_files if fn.endswith('.html')]
	for post in posts:
		post.theme = post_theme
		if post.draft:
			write_post(post, ['local'])
		else:
			write_post(post, ['local', 'public'])
	
	index = Index()
	index.theme = blog_theme
	index.section_theme = section_theme
	index.posts = posts
	write_index(index, ['local', 'public'])

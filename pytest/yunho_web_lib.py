#-*- coding: utf-8 -*-
import re

def getStringIn(pattern_start,pattern_end,source):
	#정규식으로 값 추출 pattern_start 원하는 값 pattern_end 순으로 돼어 있으면 원하는 값 추출 가
	regular = ""
	
	regular += add_slash(pattern_start)
	regular += "(.*?)"
	regular += add_slash(pattern_end)
	
	return re.search(regular, source).group(1)

def add_slash(str):
	#정규식으로 활용하기위해 앞에 역슬래쉬를 붙여준다
	expectPattern = ['[',']','<','>','/','"','=','&']
	result = ""
	for c in str:
		tf = False
		for e in expectPattern:
			if c == e:
				result += '\\'+c
				tf = True
		if tf == False:
			result +=c
	return result

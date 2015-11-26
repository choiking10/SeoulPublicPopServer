#-*- coding: utf-8 -*-
from yunho_web_lib import *
import urllib2
import sys
import xml.etree.ElementTree as ET
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect( 	host="localhost",
						user="root",
						port=3306,
						passwd="ruinpikapika123",
						db="service")

API_ID ="566d71727563686f38346554465848"
OPENAPI_FORMAT = "xml"
OPENAPI_MAX_REQUEST = 1000

SERVICE_NMS = [
	["종로구","JNListPublicReservationDetail","JNListPublicReservationInstitution",""],
    ["중구","JGListPublicReservationDetail","JGListPublicReservationInstitution",""],
    ["용산구","YSListPublicReservationDetail","YSListPublicReservationInstitution",""],
    ["성동구","SDListPublicReservationDetail","SDListPublicReservationInstitution",""],
    ["광진구","GJListPublicReservationDetail","GJListPublicReservationInstitution",""],
    ["동대문구","DDMListPublicReservationDetail","DDMListPublicReservationInstitution",""],
    ["중랑구","JRListPublicReservationDetail","JRListPublicReservationInstitution",""],
    ["성북구","SBListPublicReservationDetail","SBListPublicReservationInstitution",""],
    ["강북구","GBListPublicReservationDetail","GBListPublicReservationInstitution",""],
    ["도봉구","DBListPublicReservationDetail","DBListPublicReservationInstitution",""],
    ["노원구","NWListPublicReservationDetail","NWListPublicReservationInstitution",""],
    ["은평구","EPListPublicReservationDetail","EPListPublicReservationInstitution",""],
    ["서대문구","SDMListPublicReservationDetail","SDMListPublicReservationInstitution",""],
    ["마포구","MPListPublicReservationDetail","MPListPublicReservationInstitution","MapoYngbgsCnter"],
    ["양천구","YCListPublicReservationDetail","YCListPublicReservationInstitution",""],
    ["강서구","GSListPublicReservationDetail","GSListPublicReservationInstitution",""],
    ["구로구","GRListPublicReservationDetail","GRListPublicReservationInstitution",""],
    ["금천구","GCListPublicReservationDetail","GCListPublicReservationInstitution",""],
    ["영등포구","YDPListPublicReservationDetail","YDPListPublicReservationInstitution",""],
    ["동작구","DJListPublicReservationDetail","DJListPublicReservationInstitution",""],
    ["관악구","GAListPublicReservationDetail","GAListPublicReservationInstitution",""],
    ["서초구","SCListPublicReservationDetail","SCListPublicReservationInstitution",""],
    ["강남구","GNListPublicReservationDetail","GNListPublicReservationInstitution",""],
    ["송파구","SPListPublicReservationDetail","SPListPublicReservationInstitution",""],
    ["강동구","GDListPublicReservationDetail","GDListPublicReservationInstitution",""]
]


#define CATEGOTY
CATEGORY_NMS = {
	"체육시설" 		: ["체육","탁구","축구","농구","배구","배드민턴","테니스","경기장","에어로빅","요가","스포츠"],
	"다목적실" 		: ["강당","다목적","복합","다기능","동아리","다용도","사무","쉼터","커뮤니티",],
	"세미나실" 		: ["회의","세미나","강좌","강의","사랑","교육","스터디","배움","주민대화","주민자치","주민토론","학습","공부","상담","교실","실"],
	"실습실" 		: ["컴퓨터","자연","취미","복합","캠핑","바둑","바베큐","바비큐","창작","멀티학습","프로그램","시청각","정원","정보","음악","공원","농장","실습","체험","옥상","숲","농업","인터넷"],
	"문화공연전시" 	: ["전시","극장","스튜디오","공연","영화","녹화","아트","문화","카페","까페","연습","행사","문고","도서관","무대"],
	"화장실" 		: ["화장실"]
}

def makeServiceElement(SEV_ID,CATEGORY,LOCAL,NAME,POSX,POSY,LENTSITE,ADDRESS,PHONE):
	result = {}
	
	result["SVC_ID"] 	= SEV_ID
	result["SVC_NM"]	= NAME
	result["CATEGORY"] 	= CATEGORY
	result["LOCAL"] 	= LOCAL
	result["POSX"] 		= POSX
	result["POSY"] 		= POSY
	result["LENTSITE"]	= LENTSITE
	result["ADDRESS"]	= ADDRESS
	result["PHONE" ]	= PHONE
	
	return result

def makeServiceDetailElement(r):
	result = {}

	result["SVCID"]			= getValueFromXml(r,"SVCID") 		#서비스 아이디
	result["SVCNM"]			= getValueFromXml(r,"SVCNM") 		#서비스 이름
	result["SVCBEGINDT"]	= getValueFromXml(r,"SVCBEGINDT") 	#서비스시작날짜
	result["SVCENDDT"]		= getValueFromXml(r,"SVCENDDT") 	#서비스종료날짜
	result["PLACENM"]		= getValueFromXml(r,"PLACENM") 		#장소이름
	result["PAYAT"]			= getValueFromXml(r,"PAYAT") 		#유료여부
	result["RCEP_NM"]		= getValueFromXml(r,"RCEPTMTH_NM") 	#접수방법명
	result["USELIMMINOP"]	= getValueFromXml(r,"USELIMMINOP") 	#사용최소인원
	result["USELIMMAXOP"]	= getValueFromXml(r,"USELIMMAXOP") 	#사용최대인원
	result["EXTINFO"]		= getValueFromXml(r,"EXTINFO") 		#면적
	result["POSX"]			= getValueFromXml(r,"X") 			#x좌표
	result["POSY"]			= getValueFromXml(r,"Y") 			#y좌표
	result["ADRES"]			= getValueFromXml(r,"ADRES") 		#주소정보
	result["TELNO"]			= getValueFromXml(r,"TELNO") 		#전화번호정보
	result["AREANM"]		= getValueFromXml(r,"AREANM") 		#구 정보

	return result

def getValueFromXml(r,s):
	if r.find(s) == None :
		return ""
	return r.find(s).text

def pushServiceToDb(tablename,e):
	cur = db.cursor()
	cur.execute("set names utf8")
	
	query = "INSERT INTO %s (" % tablename
	start = 0
	for key in e.keys():
		if start != 0 :
			query +=","
		start+=1
		query += add_slash(key)

	query += ") VALUES ("

	start = 0

	for value in e.values():
		if start != 0 :
			query+=","
		start+=1
		if value is None:
			query += "\"\""
		elif re.match("^\d+?\.\d+?$",value)  is None:
			query+= "\""+add_slash(value)+"\""
		else :
			query+= "%.5f"%float(value)

	query +=")"
	
	#print query.encode("UTF-8")
	cur.execute(query.encode("UTF-8"))

def updateDbCategory():
	
	for category in CATEGORY_NMS.keys():
		query = "UPDATE LENDSERVICE SET CATEGORY = '%s' WHERE SVC_NM like " %(category);
		first = 0
		for val in CATEGORY_NMS[category]:
			if first != 0:
				query += "or SVC_NM like "
			first+=1
			query += "'%%%s%%' " % (val.encode("UTF-8"))

		cur = db.cursor()
		cur.execute("set names utf8")
		cur.execute(query.encode("UTF-8"))
	db.commit()

def getToiletFromXml(tree):
	result = []
	for r in tree.findall("row"):
		result.append(makeServiceElement(
				"NONE",
				"화장실",#r.find("NONE").text,
				r.find("GU_NM").text,
				"화장실",
				r.find("X").text,
				r.find("Y").text,
				"NONE",
				"NONE",#r.find("NONE").text,
				"NONE"#r.find("NONE").text
		))
	return result

def getLendFromXml(tree):
	result = []
	for r in tree.findall("row"):
		result.append(makeServiceElement(
				r.find("SVCID").text,
				"NONE",#r.find("NONE").text,
				r.find("AREANM").text,
				r.find("SVCNM").text,
				r.find("X").text,
				r.find("Y").text,
				r.find("SVCURL").text,
				"NONE",#r.find("NONE").text,
				"NONE"#r.find("NONE").text
		))
	return result

def getDetailElementFromXml(tree) :
	result = []
	for r in tree.findall("row"):
		result.append(makeServiceDetailElement(r));

	return result


def getServiceElementFromApi(kind,service_NM,start,end):
	count = 1
	target_url = "http://openAPI.seoul.go.kr:8088/%s/%s/%s/%d/%d" % (API_ID,OPENAPI_FORMAT,service_NM,start,end)
	print target_url
	response = urllib2.urlopen(target_url)
	xmls = response.read()
	tree = ET.fromstring(xmls)
	result = []
	if kind == 'Toilet':
		result.extend(getToiletFromXml(tree))
	if kind == 'Lent':
		result.extend(getLendFromXml(tree))
	return result

def getServiceDetailElementFromApi(service_NM,svcid):

	target_url = "http://openAPI.seoul.go.kr:8088/%s/%s/%s/1/5/%s/" % (
									API_ID, OPENAPI_FORMAT, service_NM,svcid)
#	print target_url
	response = urllib2.urlopen(target_url)
	xmls = response.read()
	tree = ET.fromstring(xmls)
	result = []
	result.extend(getDetailElementFromXml(tree))
	return result


def getDataFromSeoulOpenApi():
	result = []
	resultDetail = []
	print "----- 대관 정보 끌어오는 중 -----"
	count = 0.0
	SERVICE_NMS.reverse()
	for i in SERVICE_NMS:
		print "%f%%" % (count / len(SERVICE_NMS) * 100.0);
		count+=1;
		result.extend(getServiceElementFromApi("Lent",i[2],1,1000))
		for j in result :
			resultDetail.extend(getServiceDetailElementFromApi(i[1],j["SVC_ID"]))
	print "---- 화장실 정보 끌어오는 중 ----"
	for i in range(0,6):
		result.extend(getServiceElementFromApi("Toilet","GeoInfoPublicToilet",i*1000+1,(i+1)*1000))
	for i in result :
		pushServiceToDb("LENDSERVICE",i)
	for i in resultDetail:
		pushServiceToDb("ServiceDetail",i)
	
	db.commit()


if __name__ == "__main__":
	getDataFromSeoulOpenApi()
	updateDbCategory()

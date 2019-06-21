#note **** 1 page จะโหลดได้สูงสุดแค่ 100 รูปเท่านั้นสำหรับ code นี้
import json
import uuid
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup #pip install beautifulsoup4

#header ที่ต้องส่งไปให้ server
REQUEST_HEADER = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

if __name__ == '__main__':
	search = 'cat dog' #คำค้นหา
	number = 100    #จำนวนรูปที่ต้องการ
	directory = './images' #ที่เก็บไฟล์
	query = '+'.join(search.split()) #เปลี่ยนช่องว่างให้เป็น +
	#print(query);exit()
	url ="https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query #สร้างลิงค์ค้นหา
	#print(url);exit()
	response = urlopen(Request(url, headers=REQUEST_HEADER)) #เรียกหน้าเว็บไปที่ลิงค์ที่สร้าง
	#print(response.read());exit()
	soup     = BeautifulSoup(response, 'html.parser') #จัดการหน้าเว็บ html ให้ทำงานได้ง่ายขึ้น
	#print(soup);exit()
	image_elements = soup.find_all("div", {"class": "rg_meta"}) #ค้นหา elements รูปภาพ
	#print(image_elements);exit()

	#นำ image_elements ที่ได้แต่ล่ะตัวมาแปลงให้อยู่ในรูปแบบ dict
	metadata_dicts = [] 
	for e in image_elements:
		#print(e)
		#print('-----------------------------------------')
		metadata_dicts.append(json.loads(e.text))
	#exit()
	#แยกลิงค์กับ type ของรูปออกจากสิ่งที่ไม่ต้องการ
	link_type_records = []
	for d in metadata_dicts:
		 link_type_records.append((d["ou"],d["ity"]))

	#ตัดตัวแปรที่ไม่ต้องการทิ้ง
	images_link = link_type_records[0:number]
	#print(len(images))
	for i, (url, _type) in enumerate(images_link):#enumerate คือใส่ index ให้กับ ตัวแปร 
		if _type == None or ' ':
			_type = 'jpg'
		#try คือ เมื่อเกิด error จะแจ้งว่าเป็น error อะไร แล้วโปรแกรมยังทำงานต่อไป
		try:
			image = urlopen(Request(url, headers=REQUEST_HEADER)).read() #โหลดรูปจาก url
			fileName = uuid.uuid4().hex + "." + _type #uuid.uuid4().hex สร้งตัวหนังสือให้ไม่ซ้ำกัน.hex คือให้อยู่ในรูปแบบของ hex
			save_path = '%s/%s' % (directory,fileName)#;print(save_path) #สร้าง path สำหรับ save ไฟล์
			print(save_path)
			#save file
			with open(save_path, 'wb') as imageFile:
				imageFile.write(image)#เขียนไฟล์ลงเครื่อง
		except Exception as e:
			print(e)
    

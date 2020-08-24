'''
Author: your name
Date: 2020-08-24 22:25:35
LastEditTime: 2020-08-24 22:25:37
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /WZX-web/test_git/process_UnetBinJson/process_UnetBinJson.py
'''

"""处理UnetBin.json文件，将其中每个图片的信息存储为json文件 """

import json
import os
from base64 import b64encode


"""该函数用来将图片进行转码，返回转码后得到的字符串"""
def  img_to_json(image_name):
    ENCODING = 'utf-8'
    image_path= process_pic_path + image_name
    with open(image_path, 'rb') as jpg_file:
        byte_content = jpg_file.read()
        # 把原始字节码编码成 base64 字节码
    base64_bytes = b64encode(byte_content)
    # 将 base64 字节码解码成 utf-8 格式的字符串
    base64_string = base64_bytes.decode(ENCODING)
    return base64_string

"""该函数用来处理UnetBin.json文件
将其中每个图片的信息存储为名为图片名的json文件 """
def process_UnetBinJson():
    #将UnetBin.json中的内容读取到字典data中
    with open(process_file_path,mode='r') as fr:  
        data=json.load(fr)

    #读取字典data中的数据 
    #将其中每个图片的信息存为一个名为图片名的json文件
    for i in range(len(data)):      
        current_pic_name=data[i]['ImageNum'] #当前图片名称
        newDict={}
        newDict['version']='3.15.2'
        newDict['flags']={}
        newDict['lineColor']=[0,255,0,128]
        newDict['fillColor']=[255,0,0,128]
        newDict['imagePath']=current_pic_name
        newDict['shapes']=[]
        newDict['imageHeight']=1024
        newDict['imageWidth']=1024
        newDict['imageData']=img_to_json(current_pic_name) #将图片进行转码

        #从字典中获取新字典newDict['shapes']字段的信息
        for j in range(len(data[i]['Label'])):
            labelInfor={}
            labelInfor['label']=str(data[i]['Label'][j])
            labelInfor['line_color']=None
            labelInfor['fill_color']=None
            labelInfor['shape_type']='rectangle'
            labelInfor['flags']={}
            labelInfor['points']=[]
            points_0=[]
            points_1=[]
            x=data[i]['Rects'][j][0]
            y=data[i]['Rects'][j][1]
            w=data[i]['Rects'][j][2]
            h=data[i]['Rects'][j][3]
            points_0.append(x)
            points_0.append(y)
            points_1.append(x+w)
            points_1.append(y+h)
            labelInfor['points'].append(points_0)
            labelInfor['points'].append(points_1)

            newDict['shapes'].append(labelInfor)

        """将新字典newDict存为json文件并保存到本地"""
        js=json.dumps(newDict) 
        current_file_savedPath = out_file_path + os.path.splitext(current_pic_name)[0] + '.json'
        with open(current_file_savedPath,'w',encoding='utf-8') as f: 
            f.write(js)
            f.close()




if __name__ =="__main__":
    #UnetBin.json的读取路径
    process_file_path = 'E:/VsCode/process_UnetBinJson/160515716L/UnetBin.json'   
    #要进行转码的图片的读取路径
    process_pic_path = 'E:/VsCode/process_UnetBinJson/160515716L/img/'   
    #处理UnetBin.json文件后，得到的新文件的保存路径
    out_file_path= 'E:/VsCode/process_UnetBinJson/160515716L/newJsonFiles/' 
    #处理UnetBin.json文件，将其中每个图片的信息存储为json文件
    process_UnetBinJson()   

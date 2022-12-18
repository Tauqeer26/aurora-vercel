from importlib.resources import contents
from multiprocessing import context
from django.shortcuts import render
from django.urls import include, re_path
from django.urls import re_path as url
# Create your views here.

from django.core.files.storage import FileSystemStorage

from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import json
from tensorflow import Graph
import cv2

img_height, img_width=500,500
with open('./models/label.json','r') as f:
    labelInfo=f.read()

labelInfo=json.loads(labelInfo)


model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model=load_model('./models/Skin_26.h5')#Final_2.h5


def index(request):

    context={'a':1}
    return render(request,'index.html',context)

def index(request):

    if request.method == 'POST':
        name = request.POST['Skin']
        #context={'filepath':filePathName, 'predictedLabel':c}
        print(name)
        if name == '1':
            
            print('Great')
            #content='Radiant Plump Soap  \n Sandal Mist  \n Natural Dewy Face Mist  \n Botanical Repair Mist  \n Radiant Plump Moisturizer \n Gold Serum \n Plump Lip Balm' 
            context={'Radiant Plump Soap':'radiant-plump-soap','Sandal Mist':'','Natural Dewy Face Mist':'','Botanical Repair Mist':'botanical-repair-mist','Radiant Plump Moisturizer':'radiant-plump-moisturize','Gold Serum':'gold-serum','Plump Lip Balm':'light-lip-balm'}
            #context='Great'
        elif name == '0':
            #content='Intensive Skin Repair Sandal Lotion  \nGold Serum \n Night Repair Vit C Oil Based \n Laveneder Soothing Lotion \n Soothing Lavender FaceWash  \n Almond & Honey Soap / Baby Soap  \n Plump Lip Balm '
            context={'Intensive Skin Repair Sandal Lotion':'sandal-moisturiser','Gold Serum':'gold-serum','Night Repair Vit C Oil Based':'','Laveneder Soothing Lotion':'lavender-soothing-lotion','Soothing Lavender FaceWash':'lavender-foaming-soothing-anti-acne-cleanser','Gold Serum':'gold-serum','Plump Lip Balm':'light-lip-balm'}
            
        elif name == '2':
            context={'Lavender Foaming Face Wash':'lavender-foaming-soothing-anti-acne-cleanser', 'Charcoal Detox Soap':'charcoal-detox-soap' , 'Botanical Repair Mist':'botanical-repair-mist',  'Soothing Lavender FaceWash':'lavender-soothing-lotion' }
        elif name == '3':
            context={'Radiant Plump Soap':'radiant-plump-soap', 'Sandal Mist':'', 'Detox Sandal Scrub':'detox-sandal-scrub', 'Charcoal Detox Soap':'charcoal-detox-soap'}

            #print(content)
        elif name == '4':
            context={'Lavender Foaming Face Wash':'lavender-foaming-soothing-anti-acne-cleanser','Charcoal Detox Soap':'charcoal-detox-soap', 'Botanical Repair Mist':'botanical-repair-mist' ,'Soothing Lavender FaceWash':'lavender-soothing-lotion' }
        #context={'content':content}
        print(context)



    return render(request,'index.html',{'context':context})

    
    #context={'filepath':filePathName, 'predictedLabel':c}

def predictImage(request):
    #print (request)
    # o=request.POST.dict()
    # l=o.values()
    # u=list(l)
    # print('U Predict',u[2])
    print ('POST.dict',request.POST.dict())
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    print('fs',fs)
    filePathName=fs.save(fileObj.name,fileObj)
    print('filePathName',filePathName)
    filePathName=fs.url(filePathName)
    print('filePathName',filePathName)
    print(filePathName)
    testimage='.'+filePathName

    #img = image.load_img(testimage, target_size=(img_height, img_width))
    try:
        img = cv2.imread(testimage)
        
        if img=='None':
            print('No picture')
            predictedLabel='Please select your skin condition BELOW  to receive the finest products'


            
        img = cv2.resize(img,(img_height, img_width))
 

    except:
        c="Upload image without spacing in file name for e.g 'GREAT.jpg' / 'NICE.png' "
        print("picture")
        context={'filepath':filePathName, 'predictedLabel':c}
        print(context)
        return render(request,'index.html',context) 



    
    #x = image.img_to_array(img)
    #x=x/255
    #x=cv2.resize(1,img_height, img_width,3)
    with model_graph.as_default():
        with tf_session.as_default():
            import numpy as np
            #img = cv2.resize(img,(img_height, img_width))
            predi=model.predict(np.array([img]).astype(np.float32))
            print('Now',predi[0])


    import numpy as np


    
    a=np.max(predi[0])
    print('val',a)
    if a>=0.97:
         
        predictedLabel=labelInfo[str(np.argmax(predi[0]))]
    else:
        predictedLabel='Please select your skin condition BELOW  to receive the finest products'

    print('nownew',predictedLabel)


    context={'filepath':filePathName, 'predictedLabel':predictedLabel}
    print(context)
    return render(request,'index.html',context) 

def viewDataBase(request):
    import os
    listOfImages=os.listdir('./media/')
    listOfImagesPath=['./media/'+i for i in listOfImages]
    context={'listOfImagesPath':listOfImagesPath}
    return render(request,'viewDB.html',context) 
def check(request):
    return render(request,'index.html')

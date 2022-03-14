import boto3
import streamlit as st
from PIL import Image
import os
def load_image(image_file):
    img=Image.open(image_file)
    return img
st.header("Face Matching project using AWS")
col1,col2= st.columns(2)
col1.subheader('Enter Source Image')
src_image_file=col1.file_uploader("upload Images",type=["png","jpg","jpeg"],key=1)
col2.subheader('Enter Target Image')
target_image_file=col2.file_uploader("upload Image",type=["png","jpg","jpeg"],key=2)
if src_image_file is not None:
    file_details={"filename":src_image_file,"filetype":src_image_file.type,"filesize":src_image_file.size}
    col1.write(file_details)
    col1.image(load_image(src_image_file),width=250)
    with open(os.path.join("uploads","src.jpg"),"wb")as f:
        f.write(src_image_file.getbuffer())
        col1.success('file saved')
if target_image_file is not None:
    file_details={"filename":target_image_file,"filetype":target_image_file.type,"filesize":target_image_file.size}
    col2.write(file_details)
    col2.image(load_image(target_image_file),width=250)
    with open(os.path.join("uploads","target.jpg"),"wb")as f:
        f.write(target_image_file.getbuffer())
        col2.success('file saved')
if st.button("compare faces"):
    imagesource=open("uploads/src.jpg","rb")
    imagetarget=open("uploads/target.jpg","rb")
    client=boto3.client('rekognition')
    response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imagesource.read()},TargetImage={'Bytes':imagetarget.read()})
    #print(response)
    try:
        print(response['FaceMatches'][0]) 
        st.success('Faces Matched')
    except:
        st.error('Faces are not matched')
#print(response)

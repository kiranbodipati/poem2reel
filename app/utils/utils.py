import os
import openai
import PIL
from app.settings import *
import requests
from keyphrase_vectorizers import KeyphraseCountVectorizer
import urllib.request
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
from keybert import KeyBERT
import cv2
import glob
import contextlib
from PIL import Image
from contextlib import contextmanager
from contextlib import ExitStack
from tempfile import NamedTemporaryFile

# Loading APIs, Setting models & environments
openai.api_key = OPENAI_API_KEY
vectorizer = KeyphraseCountVectorizer()
kw_model = KeyBERT()

def generate_image_array(prompt, num=3, art=True):
    """ Use OpenAI to  generate artwork or realistic image according to prompt entered

    Args:
        prompt (str): Prompt to generate images on
        num (int): Number of outputs to generate. Default = 3 
        art (bool): True - artistic, False- Realistic, Default = True
    Returns:
        list:list of image urls of generated images.
    """
    if art==True:
        prompt= "an artwork of " + prompt
    if num>10:
        num=10
    response = openai.Image.create(
      prompt=prompt,
      n=num,
      size="1024x1024"
    )
    print(response)
    image_url_array= num*[""]
    for i, item in enumerate(response["data"]):
        image_url_array[i]= item["url"]
    return image_url_array

def generate_text_prompt(poem):
    docs=[poem]
    keywords=kw_model.extract_keywords(docs=docs, vectorizer=KeyphraseCountVectorizer(), use_maxsum=True,nr_candidates=20, top_n=7)
    keyword_string=""
    for word_prob in keywords:
        keyword_string=keyword_string+word_prob[0]+" "
    return keyword_string

def generate_advanced_text_prompt(poem):
    pass    

def save_images(poem_name, path, image_url, index_num):
    """ save images from url to file

    Args:
        poem_name (str): name of poem
        path (str): output path
        image_url (str): URL of poem
        index_num (int): index for saving file
    """
    
    img_name=poem_name+str(index_num) +".png"
    image_path=os.path.join(path, img_name) 
    urllib.request.urlretrieve(image_url, image_path)


def load_images_from_folder(folder):
    images = []
    print(folder)
    for filename in os.listdir(folder):
        img = Image.open(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

###################################################################################################################

def image_gen_pipeline(poem_name, prompt_type=0, art=True,regenerate=False, prompt="", poem=""):
    """Pipeline for generating images

    Args:
        poem_name (str): name of poem
        prompt_type (int): 0=Use Poem Name as prompt, 1=Use contextual extraction model, 2= Custom prompt. Defaultw to 0
        image_type (bool, optional): Image output type- art (True) or real(False). Defaults to True.
        regenerate (bool, optional): Regenerate images if already existing. Defaults to False.
        prompt (str, optional): Prompt to use if custom prompt. Defaults to "".
        poem=poem text, defaults to ""
    """
    path = os.path.join(IMAGE_ROOT_DIR, poem_name)
    # if image_type=='art':
    #     art=True
    # else:
    #     art=False
    if not os.path.exists(path):
        os.mkdir(path)
        if prompt_type==0: #USE Title
            image_url_array=generate_image_array(prompt=poem_name, num=3, art=art)
        elif prompt_type==1: #USE Context extraction model
            gen_prompt=generate_text_prompt(poem)
            image_url_array=generate_image_array(prompt=gen_prompt, num=3, art=art)
        elif prompt_type==2: #Custom Image Prompt
            image_url_array=generate_image_array(prompt=prompt, num=3, art=art)
            
        for index_num, image_url in enumerate(image_url_array):
            save_images(poem_name, path, image_url, index_num)
    elif regenerate==True:
        existing_files=len(os.listdir(path))
        if prompt_type==0: #USE Title
            image_url_array=generate_image_array(prompt=poem_name, num=3, art=art)
        elif prompt_type==1: #USE Context extraction model
            gen_prompt=generate_text_prompt(poem)
            image_url_array=generate_image_array(prompt=gen_prompt, num=3, art=art)
        elif prompt_type==2:
            image_url_array=generate_image_array(prompt=prompt, num=3, art=art)
            
        for index_num, image_url in enumerate(image_url_array):
            save_images(poem_name, path, image_url, existing_files+index_num)

##########################################################################################

def write_text_image(img, text_arr, output_path, color="White" ):
    # img=Image.open(image_path)
    if len(text_arr[0])<40:
        font_size=72
    elif len(text_arr[0])<60:
        font_size=58
    else:
        font_size=48
    enhancer = ImageEnhance.Brightness(img)
    if color=="Black":
        factor = 1.7 #Brightens the image
    if color=="White":
        factor = 0.3 #darkens the image
    img = enhancer.enhance(factor)
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("fonts/AlexBrush-Regular.ttf", font_size, encoding="unic")
    w=60
    h=250
    for i in text_arr:
        h=h+80
        draw.text((w, h), i, font = font, fill=color)
    img.save(output_path)
    return img 
    
def auto_split(text):
    split_text=text.splitlines()
    main_list=[]
    sub_list=[]
    for i in split_text:
        if i.strip() =="":
            main_list.append(sub_list)
            sub_list=[]
        else:
            sub_list.append(i.strip())
    # main_list.append(sub_list)
    return main_list

def manual_split(text, n=4):
    split_text=text.splitlines()
    main_list=[]
    sub_list=[]
    for i in split_text:
        if i =="":
            continue
        else:
            sub_list.append(i.strip())
            if len(sub_list)==n:
                main_list.append(sub_list)
                sub_list=[]
    return main_list

def split_text_and_write_img(poem, poem_name, image, split_type='auto', split_line=4, color="White"):
    if split_type=='auto':
        split_text=auto_split(poem)
    else:
        split_text=manual_split(poem, split_line)
    print(split_text)
    path=os.path.join(OUTPUT_ROOT_DIR, poem_name)
    if not os.path.exists(path):
        os.mkdir(path)
    images_output=[""]*len(split_text)
    for i, text in enumerate(split_text):
        img_path=os.path.join(path, poem_name+str(i)+".png")
        images_output.append(write_text_image(image, text, img_path, color=color ))

    return path
            
#####################################################################################################            
            
            
        
        
        
def extract_emotions(text):
    for c in [';', '&', '#', '{', '}']: text = text.replace(c, ':')
    label = str(requests.get(SENTIC_API_URL + text).content)[2:-3]
    print(label) 
            
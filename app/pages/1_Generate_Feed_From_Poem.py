from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))  # adds the app folder to path, all relative imports made w/ that
import streamlit as st
from utils.utils import *
from settings import *

with st.expander("Poem Details", expanded=True):
    st.title('Generate Image from New Poem')
    poem_title=""
    poem_title=st.text_input("Name of Poem", value=poem_title, placeholder="Stopping By The Woods on a Snowy Evening")
    poem_txt=""
    poem_txt = st.text_area("Poem Text", value=poem_txt, height=500, placeholder="""
    Whose woods these are I think I know.   
    His house is in the village though;   
    He will not see me stopping here   
    To watch his woods fill up with snow.   

    My little horse must think it queer   
    To stop without a farmhouse near   
    Between the woods and frozen lake   
    The darkest evening of the year.   

    He gives his harness bells a shake   
    To ask if there is some mistake.   
    The only other sound’s the sweep   
    Of easy wind and downy flake.   

    The woods are lovely, dark and deep,   
    But I have promises to keep,   
    And miles to go before I sleep,   
    And miles to go before I sleep.
    """)
    # print(poem_txt)
if poem_title!="":
    with st.expander("Background Image Selection", expanded=True):
        art=st.checkbox("Artistic", value=True, help="Check the box if the images to be generated are artistic. If unchecked, realistic images are generated.", key="art")
        select_options=('Poem Title', 'Contextual Prompt generated from Poem', 'Custom Prompt')
        index = st.selectbox(
        'What prompt do you want to use to generate Images?',
        range(len(select_options)),format_func=lambda x: select_options[x], index=0)
        regenerate=st.checkbox("Regenerate", value=False, help="Regenerate additional images",key="regenerate")
        path=os.path.join(IMAGE_ROOT_DIR, poem_title) 
        if os.path.exists(path) and regenerate==False:
            st.write("Background Images already generated for this Poem, selecting existing")

        else:
            with st.spinner(text="In progress..."):
                image_gen_pipeline(poem_title, prompt_type=index, art=art, regenerate=regenerate, prompt="", poem=poem_txt)
        if os.path.exists(path):
            images=load_images_from_folder(path)
            captions=len(images)*['']
            for i in range(len(images)):
                captions[i]="Image "+str(i)
                
            
            col1, col2, col3 = st.columns(3)
            i=0
            while i<len(images):
                with col1: 
                    st.image(images[i], captions[i])
                    i=i+1
                if i<len(images)-1:
                    with col2:
                        st.image(images[i], captions[i])
                        i=i+1
                    with col3: 
                        st.image(images[i], captions[i])
                        i=i+1
                st.write("")
            st.write("")
            index_image = st.selectbox(
            'Select Image to make reel ',
            range(len(captions)),format_func=lambda x:captions[x], index=1)
            img_selected=images[index_image]

if img_selected:          
    with st.expander("Select Feed Settings"):
        spl_type = st.radio(
        "How Do you want to Split the Poem?",
        ("auto", 'manual'), index=0, help="Auto uses paragraph detection, manual involves user specifying where to break.", key="split_type")
        color = st.radio(
        "Colour of Text",
        ("White", 'Black'), index=0, help="Select text colour", key="color")
        split_line=4
        if spl_type=='manual':
            split_line = st.slider('Where should the poem be split', 0, 6, 4)
        output_path=split_text_and_write_img(poem_txt, poem_title, img_selected, spl_type, split_line=split_line, color=color, )
        images_output=load_images_from_folder(output_path)
        
        captions=len(images)*['']
        for i in range(len(images)):
            captions[i]="Image "+str(i)
        import time

        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)         
        if len(images_output)!=0:        
            col1, col2 = st.columns(2)
            i=0
            while i<len(images_output):
                with col1: 
                    st.image(images_output[i], captions[i])
                    i=i+1
                if i<len(images_output)-1:
                    with col2:
                        st.image(images_output[i], captions[i])
                        i=i+1
                st.write("")
            st.write("")


with st.expander("Reel Creation"):
    if not os.path.exists(os.path.join(output_path, "gif_output.gif")):
        gif_fp=generate_gif(output_path)
    st.image(os.path.join(output_path, "gif_output.gif"), caption=poem_title)
    st.header("The emotions detected in the poem are:")
    col1, col2 = st.columns(2)
    emotions=extract_emotions(poem_txt)
    
    with col1:
        st.subheader(emotions[0])
    with col2:
        st.subheader(emotions[1])
    audio_list=get_audio(poem_txt)
    for file in audio_list:
        audio_file = open(file, 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/ogg')   



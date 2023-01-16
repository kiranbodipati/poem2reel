# poem2reel

## Setup and Usage
### Installation

Install dependencies using the `requirements.txt` file. We recommend using a virtual environment with `python>=3.9.0` for smooth execution. 

```
pip install -r requirements.txt 
```

create a settings.py file in `app.py` directory with all your private API Keys and root directories of input/output folders. The sample can be found in settings.txt

### Streamlit App

The Streamlit app contains the source for the final dashboard of the product. The files can be found in the `app` directory.
To execute the app, navigate to the `app` folder and execute `Home.py`.

```
cd app
streamlit run Home.py
```

## Inspiration
As a Poet and writer, I've always wanted to present my content to the world through social media, be it my personal website or Instagram, Tiktok, etc. Being bad at Art, I had to beg multiple artistic friends of mine to create digital designs for me. After receiving no response from them for over a year, I've come to realise that I can harness the power of AI to create aesthetic Instagrammable content for my poetry. 

## What it does
Poem2Reels is a software that can take a poem as an input, and create aesthetic backgrounds for the poem depending on the contextual indicators extracted from the poem. The AI can be prompted through custom prompts and titles in addition to contextual extraction from the poem. Upon generating the images, the tool uses OpenCV to scribe the poem text onto the generated background image that the user likes. 

The tool also uses a 24 dimensional sentiment analysis (the hourglass model) to analyse the sentiment of the poem, and provide background scores using (partially) AI driven technologies that can be used for reels.

## How I built it
### Contextual extraction from poems
Trained and fit my data on the `Keyphrase Count Vectoriser` and `KeyBERT`. Further Finetuned these models using the `DaVinci3 model` (OpenAI)to provide text that is useful as a prompt for the Image gen model.

### Image Generation
Harnessed the power of GAN and OpenAI's DALL-E model to generate images based on prompt extracted from contextual/title/custom prompts. 

### Scribing Text
Utilised PIL and OpenCV to scribe text onto the background Images.

### GIF Generation
Utilised OpenCV to generate GIFs from the poetry images. 

### Sentiment Analyisis
Utilised SenticNet's Hourglass Emotion Analyser to analyse a 24 dimensional emotional analysis on the poem. This required additional NLP Pre processing steps to generate the emotions correctly. 

### Music Generation
Partially used MuBERT's training algorithm to train a partial model for music generation. Due to limitations of time, the training data (Creative Commons Music) was used for music recommendation using classification based on the sentiments extracted. 

## Challenges I ran into
Dependency issues - the ffmpeg package was throwing issues which hindered the integration into an MP4 video. 

Additionally my API's are limited to the speed of the internet.

## Accomplishments that I'm proud of
- Solo Hack
- I now have my poetry portfolio ready to post on Instagram
- I've integrated a bunch of AI to create a novel tool that doesn't exist anywhere else on the internet in less than 24 hours ( There are no poetry based repositories available publically)

## What I learned
AI Art generation, AI Music Generation, Multi dimensional sentiment analyisis

## What's next for Poem2Reel
Complete the Instagram pipeline, and synchronise beats and score with the text on a finer level, as compared to the current overall analysis

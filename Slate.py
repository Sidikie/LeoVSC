from flask import Flask, render_template, request, url_for
from nltk.stem import WordNetLemmatizer
import nltk
import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_bootstrap import Bootstrap

warnings.filterwarnings('ignore')
nltk.download('popular', quiet=True)

app = Flask(__name__)

Bootstrap(app)


# Read file from document
with open('Raw.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Pre - processing the raw text

# WordkNet is a semantically-oriented dictionary of English words included in NLTK
lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello",
                   "hi",
                   "greetings",
                   "sup",
                   "what's up",
                   "hey",
                   "wats up",
                   )


# random_GREETING_RESPONSES = random.choice(GREETING_INPUTS)
GREETING_RESPONSES = ["hi",
                      "hey",
                      "*nods*",
                      "hi there",
                      "hello",
                      "I am glad! You are talking to me. How may I help you today?",
                      "Hi there – What services are you looking for today?",
                      "Hi - How can I help you today?",
                      "Hi - Welcome to Slate Web & Graphics. How can I help you today?",
                      "Hi there! You want that perfect website? You're just a few clicks away to get started",
                      "Hi - what are you looking for today?",
                      ]


SLANG_INPUTS = ("hii",
                "hiii",
                "hiiii",
                "hiiiii",
                "hiiiiii",
                "yo",
                "yoo",
                "yooo",
                "hola",
                "holla",
                )


SLANG_RESPONSES = ["hi",
                   "hey",
                   "hi there",
                   "hello",
                   "I am glad! You are talking to me. How may I help you today?",
                   "Hi there – What services are you looking for today?",
                   "Hi - How can I help you today?",
                   "Hi - Welcome to Slate Web & Graphics. How can I help you today?",
                   "Hi there! You want that perfect website? You're just a few clicks away to get started",
                   "Hi - what are you looking for today?",
                   ]


SLANG1_INPUTS = ("grazie",
                 "morning",
                 "afternoon",
                 "evening",
                 "hi buddy",
                 )


SLANG1_RESPONSES = ["hey",
                    "hi there",
                    "hello",
                    "I am glad! You are talking to me. How may I help you today?",
                    "Hi there – What services are you looking for today?",
                    "Hi - How can I help you today?",
                    "Hi - Welcome to Slate Web & Graphics. How can I help you today?",
                    "Hi there! You want that perfect website? You're just a few clicks away to get started",
                    "Hi - what are you looking for today?",
                    ]


# Random Test Inputs
DEMO_INPUTS = ("awesome",

               "wonderful",
               "great",
               "amazing",
               "fantastic",
               "cool",
               "nice",
               "that sounds good",
               )


DEMO_RESPONSES = ["no problem, anytime  And if you need further details on one of our services, please do not hesitate to drop us an email @ or give us a call on 0208",
                  "thank you for visiting Slate today",
                  "thanks buddy",
                  ]


def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""

    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def slang(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in SLANG_INPUTS:
            return random.choice(SLANG_RESPONSES)


def slang1(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in SLANG1_INPUTS:
            return random.choice(SLANG1_RESPONSES)


def demo(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in DEMO_INPUTS:
            return random.choice(DEMO_RESPONSES)


# Generating Response
def response(user_response):
    LEO_response = ''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf == 0):
        LEO_response = LEO_response+"I am sorry! I do not understand you"
        return LEO_response
    else:
        LEO_response = LEO_response+sent_tokens[idx]
        return LEO_response

    # Lines fed into the bot for interactions
# flag = True
# print(
#     "Hi, I'm LEO, Slate's Virtual agent. We're specialised in WordPress.org for SEO, MAINTENANCE, HOSTING, DEVELOPMENT, SOCIAL MEDIA, DESIGN & UX and DIGITAL MARKETING. Let's chat! To exit, type Bye"
# )
# while(flag == True):
#     user_response = input()
#     user_response = user_response.lower()
#     if(user_response != 'bye'):
#         if(user_response == 'thanks' or user_response == 'thank you'):
#             flag = False
#             print(
#                 "LEO: You are welcome. For more details, please contact our support team on 0208 to get a quote today."
#             )
#         else:
#             if(greeting(user_response) != None):
#                 print("LEO: "+greeting(user_response))
#             else:
#                 if(demo(user_response) != None):
#                     print("LEO: "+demo(user_response))
#                 else:
#                     if(slang(user_response) != None):
#                         print("LEO: "+slang(user_response))
#                     else:
#                         if(slang1(user_response) != None):
#                             print("LEO: "+slang1(user_response))
#                         else:
#                             print("LEO: ", end="")
#                             print(response(user_response))
#                             sent_tokens.remove(user_response)
#     else:
#         flag = False
#         print(
#             "LEO: Bye! take care. For more info, please contact our support team on 0208 to get a quote today."
#         )


@app.route('/')
def index():
    greet = "Hi, I'm LEO, Slate's Virtual agent. We're specialised in WordPress.org for SEO, MAINTENANCE, HOSTING, DEVELOPMENT, SOCIAL MEDIA, DESIGN & UX and DIGITAL MARKETING. Let's chat! To exit, type Bye"

    return render_template('bot.html')


@app.route('/result', methods=['GET', 'POST'])
def processdata():
    if request.method == 'POST':
        txt = request.form['rawtext']
        print(txt, '============')
        flag = True
        output = "Hi, I'm LEO, Slate's Virtual agent. We're specialised in WordPress.org for SEO, MAINTENANCE, HOSTING, DEVELOPMENT, SOCIAL MEDIA, DESIGN & UX and DIGITAL MARKETING. Let's chat! To exit, type Bye"
        while(flag == True):
            user_response = txt
            user_response = user_response.lower()
            if(user_response != 'bye'):
                if(user_response == 'thanks' or user_response == 'thank you'):
                    flag = False

                    output = "LEO: You are welcome. For more details, please contact our support team on 0208 to get a quote today."
                    render_template('bot.html', ctext=output, inp=txt)
                else:
                    if(greeting(user_response) != None):
                        output = greeting(user_response)
                        print(user_response, '::::', output)
                        return render_template('bot.html', ctext=output, inp=txt)
                    else:
                        if(demo(user_response) != None):
                            output = demo(user_response)
                            print(user_response, '::::', output)
                            return render_template('bot.html', ctext=output, inp=txt)
                        else:
                            if(slang(user_response) != None):
                                output = slang(user_response)
                                print(user_response, '::::', output)
                                return render_template('bot.html', ctext=output, inp=txt)
                            else:
                                if(slang1(user_response) != None):
                                    output = slang1(user_response)
                                    print(user_response, '::::', output)
                                    return render_template('bot.html', ctext=output, inp=txt)
                                else:

                                    output = response(user_response)
                                    print(user_response, '::::', output)
                                    return render_template('bot.html', ctext=output, inp=txt)

            else:
                flag = False

                output = "LEO: Bye! take care. For more info, please contact our support team on 0208 to get a quote today."

    return render_template('bot.html', ctext=output, inp=txt)


if __name__ == "__main__":
    app.run(debug=True)

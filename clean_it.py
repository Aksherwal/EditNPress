from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
from collections import Counter
import urllib
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('udhr2')
import re

def clean_it(url):
    #accessing html part of the given url using urllib.requests
    html=urllib.request.urlopen(url).read().decode('utf8')
    #scraping the html
    soup=BeautifulSoup(html,'html.parser')
    #find the content of all h1 tags, which is a heading
    head=soup.find_all('h1')
    #finding the main div tag where all the relevent text is present
    main_div=soup.find("div", id="pcl-full-content")
    #removing unwanted tags from the content of our main div
    unwanted1=main_div.find_all('blockquote')
    for tag in unwanted1:
        tag.decompose()
    unwanted2=main_div.find_all('em')
    for tag in unwanted2:
        tag.decompose()
    unwanted3=main_div.find_all('strong')
    for tag in unwanted3:
        tag.decompose()
    #here the actual plain text is
    main_cont=main_div.find_all('p')
    #combinig heading and paragraphs information after removing all the tags using regular expression
    All_text=head+main_cont
    clean_text_result=''
    for i in All_text:
        raw_html=str(i)
        cleantext=re.sub(r'<.*?>|Advertisement', '',raw_html)
        clean_text_result+=' '+cleantext
    
    # Analyze the text
    words_list=word_tokenize(clean_text_result) #list of all words in the text
    sent_list=sent_tokenize(clean_text_result) #list of all sentences in the text
    #counting stop words
    count_stop_words=0
    for i in words_list:
        if i.lower() in nltk.corpus.stopwords.words('english'):
            count_stop_words+=1
    #removing all the punctuation from the list of words to count the actual number of words
    punc_list=['.',',','!','?']   
    for i in words_list:
        if i in punc_list:
            words_list.remove(i)
    #making dictionary of all pos tags
    dict_upos={}
    list_new=[x for x in nltk.pos_tag(words_list, tagset='universal')]
    for i in list_new:
        if i[1] not in dict_upos.keys():
            dict_upos[i[1]]=1
        else:
            dict_upos[i[1]]+=1

    sent_count=len(sent_list)
    words_count=len(words_list)
    upos_text=str(dict_upos)
    #function for finding most frequent atleast 5 words from a paragraph
    def most_frequent_words(paragraph, n=5): 
        # Get the list of English stopwords
        stop_words = set(nltk.corpus.stopwords.words('english'))

        # Convert paragraph to lowercase and remove punctuation
        paragraph = re.sub(r'[^\w\s]', '', paragraph.lower()) #removing unnecessory symbols, spaces
        list_words = paragraph.split() #list of words
        words = [x for x in list_words if x not in stop_words] # without stopwords

        # Count the frequency of each word
        word_counts = Counter(words)

        # Get the n most frequent words
        most_common_words = word_counts.most_common(n)

        # Return the most frequent words as a string
        most_common_words_string = ', '.join(word for word, _ in most_common_words)
        return most_common_words_string
    
    most_freq_words=most_frequent_words(clean_text_result)

    return url,clean_text_result,words_count,sent_count,count_stop_words,upos_text,most_freq_words

from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
from collections import Counter
import urllib
import nltk
import re

def clean_it(url):
    html=urllib.request.urlopen(url).read().decode('utf8')

    soup=BeautifulSoup(html,'html.parser')

    head=soup.find_all('h1')

    # sub_head=soup.find_all('h2')

    main_div=soup.find("div", id="pcl-full-content")
    unwanted1=main_div.find_all('blockquote')
    for tag in unwanted1:
        tag.decompose()
    unwanted2=main_div.find_all('em')
    for tag in unwanted2:
        tag.decompose()
    unwanted3=main_div.find_all('strong')
    for tag in unwanted3:
        tag.decompose()
    
    main_cont=main_div.find_all('p')

    All_text=head+main_cont
    clean_text_result=''
    for i in All_text:
        raw_html=str(i)
        cleantext=re.sub(r'<.*?>|Advertisement', '',raw_html)
        clean_text_result+=' '+cleantext
    
    # Analyze the text
    
    words_list=word_tokenize(clean_text_result)
    sent_list=sent_tokenize(clean_text_result)

    count_stop_words=0
    for i in words_list:
        if i.lower() in nltk.corpus.stopwords.words('english'):
            count_stop_words+=1

    punc_list=['.',',','!','?']   
    for i in words_list:
        if i in punc_list:
            words_list.remove(i)

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
    
    def most_frequent_words(paragraph, n=5): 
        # Get the list of English stopwords
        stop_words = set(nltk.corpus.stopwords.words('english'))

        # Convert paragraph to lowercase and remove punctuation
        paragraph = re.sub(r'[^\w\s]', '', paragraph.lower())
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
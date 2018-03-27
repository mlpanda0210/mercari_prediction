import pandas as pd
import numpy as np
from natto import MeCab
import MeCab
import sys


def remove_identifical_word(text):
    try:
        list_text= text.split(" ")
        ng_word_list=["専用"]
        for ng_word in ng_word_list:
            if ng_word in list_text:
                ng_index=list_text.index(ng_word)
                del list_text[ng_index]
                try:
                    del list_text[ng_index-1]
                except:
                    pass

        ng2_word_list=["♡","★","☆","◇","❤","■","◆","○","●","♥","♪","(",")","[","]","✩","!","?","◀︎","▶︎"]
        for ng2_word in ng2_word_list:
            for i in range(20):
                if ng2_word in list_text:
                    ng2_index=list_text.index(ng2_word)
                    del list_text[ng2_index]

        text_total = str()
        for text in list_text:
            text_total = text_total + text +" "
        return text_total
    except:
        return text

def ex_sentence(text):
    try:
        with MeCab('-F%m,%f[0],%f[1],%f[2]') as nm:
            word_sequence = str()
            for n in nm.parse(text, as_nodes=True):
                list_feature = n.feature.split(",")
                if list_feature[1] == "名詞":
                    word_sequence = word_sequence + list_feature[0]+" "
        return word_sequence
    except:
        return word_sequence
    
def ex_sentence_mecab_ipadic_neologd(text):
    word_sequence = str()
    try:
        mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        
        mecab.parse('')#文字列がGCされるのを防ぐ
        node = mecab.parseToNode(text)  
        
        while node:
            #単語を取得
            word = node.surface
            #品詞を取得
            pos = node.feature.split(",")[1]
            if pos in ["一般","固有名詞","サ変接続"]:
                word_sequence = word_sequence + word+" "
            #次の単語に進める
            node = node.next
        return word_sequence
    except:
        return word_sequence

# from nltk.tokenize.stanford_segmenter import StanfordSegmenter
# segmenter = StanfordSegmenter(path_to_jar="stanford-segmenter-3.4.1.jar", path_to_sihan_corpora_dict="./data", path_to_model="./data/pku.gz", path_to_dict="./data/dict-chris6.ser.gz")
# sentence = u"这是斯坦福中文分词器测试"
# segmenter.segment(sentence)
#  # u'\u8fd9 \u662f \u65af\u5766\u798f \u4e2d\u6587 \u5206\u8bcd\u5668 \u6d4b\u8bd5\n'
# segmenter.segment_file("test.simp.utf8")
# # u'\u9762\u5bf9 \u65b0 \u4e16\u7eaa \uff0c \u4e16\u754c \u5404\u56fd ...
##下载
# import nltk
# nltk.download()

from nltk.tokenize.stanford_segmenter import StanfordSegmenter
segmenter = StanfordSegmenter(
     path_to_jar="stanford-segmenter-3.6.0.jar",
     path_to_slf4j = "slf4j-api.jar",
     path_to_sihan_corpora_dict="./data",
     path_to_model="./data/pku.gz",
     path_to_dict="./data/dict-chris6.ser.gz")
sentence = u"这是斯坦福中文分词器测试"
segmenter.segment(sentence)
# >>> u'\u8fd9 \u662f \u65af\u5766\u798f \u4e2d\u6587 \u5206\u8bcd\u5668 \u6d4b\u8bd5\n'
segmenter.segment_file("test.simp.utf8")
# >>> u'\u9762\u5bf9 \u65b0 \u4e16\u7eaa \uff0c \u4e16\u754c \u5404\u56fd ...

# 英文测试
# import nltk
# text = 'i am a good boy.you are a bad girl'
# sens = nltk.sent_tokenize(text)
# print(sens)
# words = []
# for sent in sens:
#     words.append(nltk.word_tokenize(sent))
# for line in words:
#     print(line)
#
# tags = []
# for tokens in words:
#     tags.append(nltk.pos_tag(tokens))
#
# for tag in tags:
#     ners = nltk.ne_chunk(tag)
#     print(ners)

import re
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
text = '''黄永玉: 明确的爱，直接的厌恶，真诚的喜欢，
站在太阳底下的坦荡，还有被坚定的选择'''
# 分词预处理
clean_text = re.sub(r'[^\u4e00-\u9fff]','', text)
# 分词
t1 = jieba.lcut(clean_text)
# 生成词云
t2 = ' '.join(t1)
t2_wc = WordCloud(font_path='/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc').generate(t2)
t2_wc.to_file('wordcloud1.png')
# 显示词云图片
plt.imshow(t2_wc)
plt.axis('off')
plt.show()
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pytagcloud
import webbrowser


# matplotlib 그래프

from numpy.ma import size


def show_graph_bar(dictwords, pagename):

    # 한글처리
    font_filename = 'c:/Windows/fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    print(font_name)
    plt.rc('font',family=font_name)

    # 라벨처리
    plt.xlabel("주요단어")
    plt.ylabel("빈도수")
    plt.grid(True)

    # 데이타 대입
    dict_keys = dictwords.keys()  # key=>명사들, 단어들
    dict_values = dictwords.values()

    plt.bar(range(len(dictwords)),dict_values,align='center')  # bar그래프를 주고 안에 옵션을 준다.
    plt.xticks(range(len(dictwords)), list(dict_keys), rotation=70)

    save_filename = "D:/JavaStudy/imformation/%s_bar_graph.png" %pagename
    plt.savefig(save_filename, dpi=400, bbox_inches='tight')

    plt.show()





# 워드 클라우드
def wordcloud(dictwords, pagename):
    taglist = pytagcloud.make_tags(dictwords.items(), maxsize=80)

    save_filename = "D:/JavaStudy/imformation/%s_wordcloud.jpg" % pagename

    pytagcloud.create_tag_image(
        taglist,
        save_filename,
        size=(800,600),
        fontname = 'korea',
        rectangular=False
    )

    webbrowser.open(save_filename)



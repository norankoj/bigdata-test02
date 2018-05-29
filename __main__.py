from collect import crawler
from analysis import analizer
from visualize import visualizer

pagename = "chosun"
from_date ="2018-05-22"
to_date = "2018-05-24"

if __name__ == "__main__":
    # #수집
    # postList = crawler.fb_get_post_list(pagename,from_date,to_date)
    # print(postList)

    #분석
    dataString = analizer.json_to_str("D:/JavaStudy/imformation/chosun.json","message_str")
    count_data = analizer.count_wordfreq(dataString)
    print(count_data)
    dictword = dict(count_data.most_common(20))


    # 그래프
    visualizer.show_graph_bar(dictword,pagename)

    # 워드클라우드
    visualizer.wordcloud(dictword,pagename)
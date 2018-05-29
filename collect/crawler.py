import requests
from datetime import datetime, timedelta
import json

# 변수는 위로
BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBAMJJ9A0jAGh9N5UBPTWqhUNfZBsUqH0JErLZBJaUOLqJK4vOPhFfZAZBGBkcqCtDbRPnV73yEMRvZC9QCtuN1CkIMEsASAQZA0A8lXKH9WjVWxFRRgSlRYEtuelNrnbERu8kz5ZBALByilCaZA4fKAUfx7QUSCiRMy562DEkLIv3cPkiNGAbAeaS9ZBlWtdA2FQZDZD"
LIMIT_REQUEST = 20


# url 을 주면 json 데이타를 리턴해준다.
def get_json_result(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return "%s : Error for request [%s]" % (datetime.now(),url)  # 모듈안에 now함수



# 페이스북 페이지네임을 주면 페이지 id값을 리턴해준다.
def fb_name_to_id(pagename):

    # url ="http://graph.facebook.com/v3.0/jtbcnews/?access_token=268523"
    base = BASE_URL_FB_API
    node = "/%s" %pagename
    params = "/?access_token=%s" %ACCESS_TOKEN
    url = base + node + params

    json_result = get_json_result(url)
    return json_result ["id"]



# 페이스북 페이지네임, 시작날짜 , 끝날짜를 주면 json 형태로 데이타를 리턴해준다.

# url ="http://graph.facebook.com/v3.0/[node,edge]/?parameters"
def fb_get_post_list(pagename,from_date,to_date):

    page_id = fb_name_to_id(pagename)
    base = BASE_URL_FB_API
    node = "/%s/posts" %page_id
    fields = '/?fields=id,message,link,name,type,shares,' + \
             'created_time,comments.limit(0).summary(true),'+\
             'reactions.limit(0).summary(true)'
    duration = '&since=%s&until=%s' % (from_date, to_date)
    parameters = '&limit=%s&access_token=%s' % (LIMIT_REQUEST, ACCESS_TOKEN)

    url = base + node + fields + duration + parameters

    postList = []
    isNext = True
    while isNext :
        tempPostList = get_json_result(url)
        for post in tempPostList["data"]:
            postVo = preprocess_post(post)
            postList.append(postVo)

        paging = tempPostList.get("paging").get("next")
        #paging = tempPostList["paging"]["next"]
        if paging != None:
            url = paging
        else:
            isNext = False
    # save results to file

    with open("d:/javaStudy/imformation/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return postList

def preprocess_post(post):

    #작성일 +9시간 해줘야 함
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')


    #공유 수
    if "shares" not in post :
        shares_count = 0
    else :
        shares_count = post["shares"]["count"]  # shares,count 내가 정한게 아니라 정해준 거로 써야합니다.

    #리액션 수
    if "reactions" not in post :
        reactions_count = 0
    else :
        reactions_count = post["reactions"]["summary"]["total_count"]

    # 댓글 수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]

    # 메세지 수
    if "message" not in post:
        message_str = 0
    else:
        message_str = post["message"]

    postVo = {
        "created_time": created_time,
        "shares_count": shares_count,
        "reactions_count": reactions_count,
        "comments_count": comments_count,
        "message_str": message_str

    }

    return postVo


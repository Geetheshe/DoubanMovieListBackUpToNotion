import re
import random
from bs4 import BeautifulSoup
from UploadToNotionDatabase import *


class MovieList:
    def __init__(self, user_cookies, database_id, status, token):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
        self.cookies = user_cookies
        self.database_id = database_id
        self.status = status
        self.fail = []
        self.token = token

    def req(self, url, start_number):
        r1 = requests.request("GET", url=url, headers=self.headers, cookies=self.cookies)
        page_number = start_number / 15 + 1
        if r1.status_code == 200:
            print(f'第{int(page_number)}页访问成功，正在进行同步……')
            list_soup = BeautifulSoup(r1.text, 'lxml')
            movies_list = list_soup.find_all("div", class_="item")
            for movie in movies_list:
                # 条目看过、想看、在看
                movie_status = {"name": self.status}

                # 条目名称
                movie_title = movie.find("em").get_text()

                # 条目评分
                try:
                    rating = movie.find("span", class_=re.compile("rating"))["class"]
                    if rating == ['rating1-t']:
                        movie_rate = "⭐"
                    elif rating == ['rating2-t']:
                        movie_rate = "⭐⭐"
                    elif rating == ['rating3-t']:
                        movie_rate = "⭐⭐⭐"
                    elif rating == ['rating4-t']:
                        movie_rate = "⭐⭐⭐⭐"
                    elif rating == ['rating5-t']:
                        movie_rate = "⭐⭐⭐⭐⭐"
                    else:
                        movie_rate = "暂无打分信息"
                except TypeError:
                    movie_rate = "暂无打分信息"

                # 条目短评
                try:
                    movie_comment = movie.find("span", class_="comment").get_text()
                except AttributeError:
                    movie_comment = "暂无评价"

                # 条目标记时间
                movie_date = movie.find("span", class_="date").get_text()

                # 条目豆瓣链接
                movie_link = movie.find("a", href=True)["href"]

                # 获取条目详情中的导演、类型、制片国家/地区、IMDB链接
                r2 = requests.request("GET", url=movie_link, headers=self.headers, cookies=self.cookies)
                if r2.status_code == 200:
                    print(f'《{movie_title}》的详情页访问访问成功，正在备份。')
                    detail_soup = BeautifulSoup(r2.text, 'lxml')

                    # 条目导演，多个导演需要拆分后获得字典
                    try:
                        movie_director = []
                        directors = detail_soup.find("span", class_="attrs").get_text().split(" / ")
                        for director in directors:
                            director_dict = {}
                            director_dict["name"] = director
                            movie_director.append(director_dict)
                    except AttributeError:
                        movie_director = [{"name": "暂无导演信息"}]

                    # 条目类型
                    try:
                        movie_genre = []
                        genres = detail_soup.find_all("span", property="v:genre")
                        for genre in genres:
                            genre_dict = {}
                            genre_dict["name"] = genre.get_text()
                            movie_genre.append(genre_dict)
                    except AttributeError:
                        movie_genre = [{"name": "暂无类型信息"}]

                    # 条目制片国家/地区
                    try:
                        movie_country = []
                        countries = detail_soup.find("span", class_="pl", text=re.compile("制片国家")).next_sibling.lstrip().split(" / ")
                        for country in countries:
                            country_dict = {}
                            country_dict["name"] = country
                            movie_country.append(country_dict)
                    except AttributeError:
                        movie_country = [{"name": "暂无制片国家/地区信息"}]

                    # 条目imdb链接
                    try:
                        imdb_id = detail_soup.find("span", class_="pl", text=re.compile("IMDb")).next_sibling.lstrip()
                        imdb_link = f"https://www.imdb.com/title/{imdb_id}/"
                    except AttributeError:
                        imdb_link = "暂无IMDb链接"

                    # 条目封面
                    try:
                        poster_origin_url = detail_soup.find("img", rel="v:image")["src"]
                        poster_l_url = poster_origin_url.replace("s_ratio_poster", "l")
                        if poster_origin_url.count("webp") == 1:
                            poster_l_url = poster_l_url.replace("webp", "jpg")
                    except TypeError:
                        poster_l_url = "暂无封面"

                    # 条目上映年份
                    try:
                        movie_year = {}
                        find_year = detail_soup.find("span", class_="year").get_text().replace("(", "").replace(")", "")
                        movie_year["name"] = find_year
                    except AttributeError:
                        movie_year = {"name": "暂无上映年份信息"}
                else:
                    imdb_link = "访问失败，暂无IMDb链接"
                    poster_l_url = "访问失败，暂无封面"
                    movie_director = [{"name": "访问失败，暂无导演信息"}]
                    movie_country = [{"name": "访问失败，暂无制片国家/地区信息"}]
                    movie_genre = [{"name": "访问失败，暂无类型信息"}]
                    movie_year = {"name": "访问失败，暂无上映年份信息"}
                    self.fail.append(f"《{movie_title}》")

                create_page = NotionDatabase(token=self.token)
                failure = create_page.create_a_page(database_id=self.database_id,
                                                    movie_title=movie_title,
                                                    movie_rate=movie_rate,
                                                    movie_comment=movie_comment,
                                                    movie_date=movie_date,
                                                    movie_link=movie_link,
                                                    imdb_link=imdb_link,
                                                    poster_l_url=poster_l_url,
                                                    movie_director=movie_director,
                                                    movie_country=movie_country,
                                                    movie_genre=movie_genre,
                                                    movie_year=movie_year,
                                                    movie_status=movie_status)
                if failure != "":
                    self.fail.append(failure)

                # 每个条目进行反爬休息
                time.sleep(random.randint(5, 10))

        else:
            print(f'第{int(page_number)}页访问不成功，正在跳转下一页。')
            self.fail.append(f"第{int(page_number)}页全部条目")
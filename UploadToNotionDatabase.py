import requests
import json
import time


class NotionDatabase:
    def __init__(self, token):
        self.database_url = "https://api.notion.com/v1/databases"
        self.page_url = "https://api.notion.com/v1/pages"
        self.headers = {'Authorization': f'Bearer {token}',
                        'Notion-Version': '2021-08-16',
                        "Content-Type": "application/json"}

    def create_a_database(self, page_id):
        create_database_data = {
            "parent": {"type": "page_id", "page_id": page_id},
            "title": [{"type": "text", "text": {"content": "电影标记列表"}}],
            "icon": {"type": "emoji", "emoji": "🎬"},
            "properties": {
                "条目名称": {"title": {}},
                "评分": {"select": {"options": [
                    {"name": "⭐", "color": "yellow"},
                    {"name": "⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐⭐", "color": "yellow"},
                ]}},
                "短评": {"rich_text": {}},
                "标记时间": {"date": {}},
                "豆瓣链接": {"url": {}},
                "导演": {"multi_select": {}},
                "类型": {"multi_select": {}},
                "制片国家/地区": {"multi_select": {}},
                "IMDb链接": {"url": {}},
                "封面": {"files": {}},
                "上映年份": {"select": {}},
                "标记状态": {"select": {}}
            }
        }

        data = json.dumps(create_database_data)

        r = requests.request("POST", url=self.database_url, headers=self.headers, data=data)
        if r.status_code == 200:
            database_id = eval(r.text.replace(":null", ":'null'").replace(":false", ":'false'"))["id"]
            return database_id
        else:
            print("创建数据库失败，请检查是否页面有授权给集成使用，再重新使用本程序~")
            input("请按Enter回车键退出。")
            exit()

    def create_a_page(self,
                      database_id,
                      movie_title,
                      movie_rate,
                      movie_comment,
                      movie_date,
                      movie_link,
                      imdb_link,
                      poster_l_url,
                      movie_director,
                      movie_country,
                      movie_genre,
                      movie_year,
                      movie_status):
        create_page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "条目名称": {"title": [{"text": {"content": movie_title}}]},
                "评分": {"select": {"name": movie_rate}},
                "短评": {"rich_text": [{"text": {"content": movie_comment}}]},
                "标记时间": {"date": {"start": movie_date}},
                "豆瓣链接": {"url": movie_link},
                "IMDb链接": {"url": imdb_link},
                "封面": {"files": [{"name": poster_l_url, "external": {"url": poster_l_url}}]},
                "导演": {"multi_select": movie_director},
                "制片国家/地区": {"multi_select": movie_country},
                "类型": {"multi_select": movie_genre},
                "上映年份": {"select": movie_year},
                "标记状态": {"select": movie_status}
            }
        }

        data = json.dumps(create_page_data)
        r = requests.request("POST", url=self.page_url, headers=self.headers, data=data)
        if r.status_code == 200:
            print(f"《{movie_title}》详情上传至Notion成功。")
            failure = ""
            return failure
        else:
            print(f"《{movie_title}》详情上传至Notion失败。")
            failure = f"《{movie_title}》"
            return failure

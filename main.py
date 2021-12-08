from DoubanSpider import *
from UploadToNotionDatabase import *


def main():
    print("●●●●●●●●●●●●●●●●●●●●●●●●●●\n"
          "本程序的功能是将你的豆瓣观影记录进行备份，并同步至你的Notion数据库中。\n"
          "需要你提供的数据包括：\n"
          "1. 豆瓣用户id\n"
          "2. 豆瓣用户cookies\n"
          "3. Notion集成密钥（并非Notion密码）\n"
          "4. Notion页面链接或数据库链接\n"
          "●●●●●●●●●●●●●●●●●●●●●●●●●●\n")
    user_id = input("----------------------------------------------------\n"
                    "请输入豆瓣用户id：")
    user_cookies = add_cookies()
    token = input("----------------------------------------------------\n"
                  "请输入Notion集成密钥：")

    choice = int(input("----------------------------------------------------\n"
                       "备份看过的电影列表，请按1；\n"
                       "备份正在看的电影列表，请按2；\n"
                       "备份想看的电影列表，请按3；\n"
                       "退出程序，请按4。\n"
                       "请在此处输入："))

    if choice == 1:
        database_id, start_number, end_number = first_or_not(token=token)

        watched_to_notion = MovieList(user_cookies=user_cookies, database_id=database_id, status="看过", token=token)

        while start_number <= end_number:
            watched_url = f"https://movie.douban.com/people/{user_id}/collect?start={start_number}&sort=time&rating=all&filter=all&mode=grid"
            watched_to_notion.req(url=watched_url, start_number=start_number)
            start_number += 15
        if len(watched_to_notion.fail) == 0:
            print(f'同步已完成。')
        else:
            print(f"同步已完成，其中同步失败的条目有{watched_to_notion.fail}")
    elif choice == 2:
        database_id, start_number, end_number = first_or_not(token=token)

        watched_to_notion = MovieList(user_cookies=user_cookies, database_id=database_id, status="正在看", token=token)

        while start_number <= end_number:
            watched_url = f"https://movie.douban.com/people/{user_id}/do?start={start_number}&sort=time&rating=all&filter=all&mode=grid"
            watched_to_notion.req(url=watched_url, start_number=start_number)
            start_number += 15
        if len(watched_to_notion.fail) == 0:
            print(f'同步已完成。')
        else:
            print(f"同步已完成，其中同步失败的条目有{watched_to_notion.fail}")
    elif choice == 3:
        database_id, start_number, end_number = first_or_not(token=token)

        watched_to_notion = MovieList(user_cookies=user_cookies, database_id=database_id, status="想看", token=token)

        while start_number <= end_number:
            watched_url = f"https://movie.douban.com/people/{user_id}/wish?start={start_number}&sort=time&rating=all&filter=all&mode=grid"
            watched_to_notion.req(url=watched_url, start_number=start_number)
            start_number += 15
        if len(watched_to_notion.fail) == 0:
            print(f'同步已完成。')
        else:
            print(f"同步已完成，其中同步失败的条目有{watched_to_notion.fail}")
    elif choice == 4:
        exit()
    else:
        print("----------------------------------------------------\n"
              "输入有误，请重新输入。")
        main()


def first_or_not(token):
    choice = int(input("----------------------------------------------------\n"
                       "如果你是第一次使用，还未创建数据库，请按1；\n"
                       "如果你不是第一次使用本程序，想要继续沿用上次使用的数据库，请按2;\n"
                       "退出程序，请按3。\n"
                       "请在此处输入："))
    if choice == 1:
        create_database = NotionDatabase(token=token)
        database_id = create_database.create_a_database(page_id=find_page_id())

        start_page_number = int(input("----------------------------------------------------\n"
                                      "请输入从第几页开始备份（输入数字即可）："))
        start_number = (start_page_number - 1) * 15
        end_page_number = int(input("----------------------------------------------------\n"
                                    "请输入备份到第几页（输入数字即可）："))
        end_number = (end_page_number - 1) * 15

        return database_id, start_number, end_number
    elif choice == 2:
        database_id = find_database_id()

        start_page_number = int(input("----------------------------------------------------\n"
                                      "请输入从第几页开始备份（输入数字即可）："))
        start_number = (start_page_number - 1) * 15
        end_page_number = int(input("----------------------------------------------------\n"
                                    "请输入备份到第几页（输入数字即可）："))
        end_number = (end_page_number - 1) * 15

        return database_id, start_number, end_number
    elif choice == 3:
        exit()
    else:
        print("----------------------------------------------------\n"
              "输入有误，请重新输入。")
        first_or_not(token=token)


def find_page_id():
    notion_page_url = input("----------------------------------------------------\n"
                            "请输入一个Notion Page的链接。\n"
                            "注意事项1：这个Page须先授权给集成，否则将会创建数据库失败。\n"
                            "注意事项2：请输入Notion Page链接，而非Notion Database链接。\n"
                            "请在此处输入链接：")

    if notion_page_url[0:22] == "https://www.notion.so/":
        if notion_page_url.count("?v=") == 0:
            if notion_page_url.count("#") == 0:
                page_id = notion_page_url[len(notion_page_url) - 32:len(notion_page_url) - 24] + '-' \
                          + notion_page_url[len(notion_page_url) - 24:len(notion_page_url) - 20] + '-' \
                          + notion_page_url[len(notion_page_url) - 20:len(notion_page_url) - 16] + '-' \
                          + notion_page_url[len(notion_page_url) - 16:len(notion_page_url) - 12] + '-' \
                          + notion_page_url[len(notion_page_url) - 12:len(notion_page_url)]
                return page_id
            elif notion_page_url.count("#") != 0:
                last_hash = notion_page_url.index("#")
                page_id = notion_page_url[last_hash - 32:last_hash - 24] + "-" \
                          + notion_page_url[last_hash - 24:last_hash - 20] + "-" \
                          + notion_page_url[last_hash - 20:last_hash - 16] + "-" \
                          + notion_page_url[last_hash - 16:last_hash - 12] + "-" \
                          + notion_page_url[last_hash - 12:last_hash]
                return page_id
        elif notion_page_url.count("?v=") != 0:
            print("----------------------------------------------------\n"
                  "你输入的链接可能是Notion数据库链接，不适用于创建数据库，再重新试试吧！")
            try_to_find_page_id()
    else:
        print("----------------------------------------------------\n"
              "你输入的链接可能不是Notion链接，请重试吧！")
        try_to_find_page_id()


def try_to_find_page_id():
    choice = int(input("----------------------------------------------------\n"
                       "重新查找Page ID请按1，退出请按2："))

    if choice == 1:
        find_page_id()
    elif choice == 2:
        exit()
    else:
        print("----------------------------------------------------\n"
              "你好像输错啦，再来一次吧！")
        try_to_find_page_id()


def find_database_id():
    notion_database_url = input("----------------------------------------------------\n"
                                "请输入已存在的Notion Database链接:")

    if notion_database_url[0:22] == "https://www.notion.so/":
        if notion_database_url.count("?v=") == 1:
            last_slash = notion_database_url.rfind("/")
            database_id = notion_database_url[last_slash + 1:last_slash + 33]
            return database_id
        elif notion_database_url.count("?v=") == 0:
            print("----------------------------------------------------\n"
                  "你输入的链接不是Notion数据库链接，请查看是否输入成了Notion Page链接，再重新试试吧！")
            try_to_find_database_id()
    else:
        print("----------------------------------------------------\n"
              "你输入的链接可能不是Notion链接，请再重新试试吧！")
        try_to_find_database_id()


def try_to_find_database_id():
    choice = int(input("----------------------------------------------------\n"
                       "重新查找Database ID请按1，退出请按2"))

    if choice == 1:
        find_database_id()
    elif choice == 2:
        exit()
    else:
        print("----------------------------------------------------\n"
              "你好像输错啦，再来一次吧！")
        try_to_find_database_id()


def add_cookies():
    cookies_str = input('----------------------------------------------------\n'
                        '请输入你的豆瓣cookies:')
    if cookies_str[0:3] == "ll=":
        cookies_dict = {}
        cookies_list = cookies_str.replace('"', "").split('; ')
        for i in cookies_list:
            name, value = i.split('=', 1)
            cookies_dict[f'{name}'] = value
        return cookies_dict
    else:
        print("你输入的豆瓣cookies可能有误，请再重新试试吧！")
        add_cookies()


if __name__ == "__main__":
    main()
# DoubanMovieListBackUpToNotion

## 说明
将豆瓣电影标记记录（看过/想看/在看）爬取下来，爬取内容包括条目标题、IMDb链接、上映年份、制片国家/地区、导演、封面、标记时间、标记状态、短评、类型、评分、豆瓣链接，并备份至Notion数据库。

## 使用方法
### 方法一
- 直接使用打包好的main.exe文件
### 方法二
- 安装python3环境
- pip安装requests、beautifulsoup4和lxml这三个第三方库
- 运行main.py

## 流程
图文并茂流程：https://www.douban.com/note/821382787/
1. 填写豆瓣用户id
2. 填写豆瓣用户cookies
3. 根据自身情况填写Integration token
    - 若是第一次使用，请先自行在Notion设置中创建一个Notion Integration，复制这个Integration的密钥（即token），填写入程序
    - 若非第一次使用，请将上次使用的Integration密钥，填写入程序
4. 选择备份哪个列表（看过/在看/想看）的电影条目
5. 选择是否为第一次使用本程序
    - 若是第一次使用，请先选择一个Notion Page授权给刚填写入token的Notion Integration，并将此Notion Page的链接填写入程序，程序将在这个页面中创建一个Notion数据库
        - 如何授权：在Notion Page右上角选择Share，邀请此Notion Integration，即为授权成功。
    - 若不是第一次使用，请填写入上一次由程序创建出来的数据库链接
6. 选择从第几页备份至第几页
    - 为了防止爬虫被发现导致IP地址被禁，爬虫速度设置得很慢，所以建议每次备份页数少一点，可以多次备份，但一次性备份1000多条也不是不可以。
7. Notion数据库开始备份，请等待备份完成。

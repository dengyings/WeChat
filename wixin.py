# coding: utf-8
from DyWeixin import DyWeixin
from WriteDB import save_json
import time

if __name__ == '__main__':
    official_cookie = "noticeLoginFlag=1; remember_acct=964785023%40qq.com; pgv_pvi=2290823168; pgv_pvid=6620647204; ptui_loginuin=773890355; pt2gguin=o0773890355; RK=9AhptXwFPG; ptcz=3c29279ecd3cdd8285766106bebdd919ec3ee08b1a6e6d565c48b77abf3b4171; ua_id=8GOaoVhdR1LbHgldAAAAAJz4aQp8qa5V8X1niAGYyaE=; mm_lang=zh_CN; noticeLoginFlag=1; remember_acct=964785023%40qq.com; xid=34e6828fbbdb9b0d588ebc2713e05fb2; pgv_si=s9479197696; uuid=a75548cef55abcd4ea0bcd64b6d20d18; bizuin=3576798592; ticket=10171718c4a126bd81d13dd47906507de46ae373; ticket_id=gh_92d602076e73; cert=UhcvGgET4o_bIa975eSny_r6l7xjMJcU; data_bizuin=3576798592; data_ticket=hmrXTZfQNjK4wHLVpCx1GkFw8yWSeV4h2mphPYgHDKAjFplA8+2g/7ZVx/1/Ue/R; slave_sid=XzIyWDVaaVRVWjdsX3lxYVVpeWxiRk1EdDFVRHNZMlQzemhuMUVZOGZwc1pVd0x0TWNNZkVIelN4U1EzQUxWdDhERkZNejRxQVJfVGhJTDlBNWhXaVk1eklNdG5UVEhzNkVSUkR0YW5TM2NIUHNTNVZmRTB2aERKY0h1eEo2V0UxbUtneWNGdGt2RUdvaVBu; slave_user=gh_92d602076e73; openid2ticket_ogJ0x1SS4OqLCLlo_UzW8sqM9lE0=YbP6XcrAjSeT2PS5ImmvTg68Ppf0h5D6Inly7TmszrI=; rewardsn=; wxtokenkey=777"
    token = "621560127"
    wechat_cookie = "rewardsn=; wxuin=1723124627; devicetype=Windows7; version=62060619; lang=zh_CN; pass_ticket=bSSOOBYMttQ3rethJqnlrF4ZhCy3grtSZOYYfVEf8qkYUQqFzi9tnGr07GGF+Rgm; wap_sid2=CJOX07UGElxSLXFSX0tZSjJueE8tRjQ2N0w0VFVsa2MzdVdKUFNCWEJtSmZta2Z6ZFZHZk5ELUpvZlBTa3Vxc0lmZWxHVlNwMWl2WGNWUzh2UHhaSWxpZjRqOWJCdHdEQUFBfjDRt+7gBTgNQAE=; wxtokenkey=777"
    nickname = "中原地产"

    test = DyWeixin(
        official_cookie=official_cookie,
        token=token,
        wechat_cookie=wechat_cookie)
    for i in range(100):
        time.sleep(10)
        try:
            data = test.complete_info(nickname=nickname, begin=i*5)
            save_json("test.json", data)
        except Exception as e:
            print("已爬取完成")
            break

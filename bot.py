import datetime
import discord
from discord.ext import commands
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from table2ascii import table2ascii
import os
app = commands.Bot(command_prefix= '!')
token =os.environ['token']

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("사장님 모르게 귤까먹기")
    await app.change_presence(status=discord.Status.online, activity=game)
    every_day_report()
@tasks.loop(seconds=1)
async def every_day_report(self):
    channel =app.get_channel(937884630474956872)
    now = datetime.datetime.now()
    print(now)
    if now.hour == 23 and nowminute == 0 and now.second < 10:
        await channel.send(now)
        url = "https://debtolee.pe.kr/cityserver/task/report/list_today.php"
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table')
            tr = table.find_all('tr')

            head = table.find_all('th')
            headli = list()
            tdli = list()
            for h in head:
                headli.append(h.text)
            for r in tr:
                li = list()
                r = r.find_all('td')
                for d in r:
                    li.append(d.text)
                tdli.append(li)
            tdli = tdli[1:]
            headli.pop()
            headli.pop()
            df = pd.DataFrame(tdli, columns=headli)
            df = df.drop(['#'], axis=1)
            print(df)
            output = table2ascii(
                header=list(df.columns),
                body=list(df.values),
                #                    footer=[""],
            )
            await channel.send(f"```\n{output}\n```")
        else:
            print(response.status_code)

        time.sleep(1)
@app.event
async def on_message(message):
    print(message)
    channel =app.get_channel(937884630474956872)
    if message.author.bot:
        return None
    elif message.channel.name=="bot-dev-chatting-channel":
        if message.content == "!안녕":
            await channel.send("안녕하세요! "+message.author.name+"님 반갑습니다. ")

        elif message.content.startswith("!내정보"):
            embed=discord.Embed(title="EXAMPLE EMBED", description="This is Embed.", color=0x00ff56)
            embed.set_thumbnail(url = message.author.avatar_url)
            embed.add_field(name = "이름", value = message.author.name , inline = True)
            embed.add_field(name = "서버 닉네임", value = message.author.display_name , inline = True)
            embed.add_field(name = "아이디", value = message.author.id , inline = False)
            embed.set_footer(text = "This is footer")
            await channel.send(embed = embed)
        elif message.content.startswith("!오늘보고"):
            url = "https://debtolee.pe.kr/cityserver/task/report/list_today.php"
            response = requests.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find('table')
                tr = table.find_all('tr')

                head = table.find_all('th')
                headli = list()
                tdli = list()
                for h in head:
                    headli.append(h.text)
                for r in tr:
                    li = list()
                    r = r.find_all('td')
                    for d in r:
                        li.append(d.text)
                    tdli.append(li)
                tdli = tdli[1:]
                headli.pop()
                headli.pop()
                df = pd.DataFrame(tdli, columns=headli)
                df = df.drop(['#'],axis=1)
                print(df)
                output = table2ascii(
                    header=list(df.columns),
                    body=list(df.values),
#                    footer=[""],
                )
                await channel.send(f"```\n{output}\n```")
            else:
                print(response.status_code)

        elif message.content.startswith("!보고"):
            li = list()

            name = ""
            part = ""
            content = message.content.splitlines()

            await channel.send("https://debtolee.pe.kr/cityserver")

            # for c in content:
            #     dic = {'user':'','part':'','content':'','count':0,'unit':'','etc':''}
            #     if c.find("[")>=0:
            #         name = c.replace("[","").replace("]","")
            #     elif c.find("-")>=0:
            #         part = c.replace("-","").replace(" ","")
            #     elif c.find(":")>=0:
            #         dic['user'] = name
            #         dic['part'] = part
            #         dic['content'] = c[:c.find(':')]
            #         if c.find("(")>=0:
            #             etc = c[c.find("(")+1:c.find(")")]
            #             dic['etc'] =  etc
            #             c = c.replace("("+etc+")","")
            #
            #         cnt = c[c.find(':'):].replace(":","").replace(" ","")
            #         #+가 들어있으면 처리
            #         if cnt.find("+")>=0:
            #             for s in cnt.split("+"):
            #                 print(s)
            #                 s = s.replace(" ","")
            #
            #                 num = re.findall("\d+",s)[0]
            #                 dic['count'] = num
            #                 dic['unit'] = s.replace(str(num),"")
            #
            #                 li.append(dic)
            #         else:
            #             num = re.findall("\d+", c)[0]
            #             dic['count'] = num
            #             dic['unit'] = cnt.replace(str(num), "")  # 숫자를 빈칸으로
            #             li.append(dic)
            # for l in li:
            #     await channel.send(l)

        elif message.content.startswith("!"):
            await channel.send("모르니까 물어보지 마세요 ㅡ.ㅡ")


app.run(token)

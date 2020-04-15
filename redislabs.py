from __future__ import unicode_literals

import redis


# fill in the following.
HOST = "redis-16080.c13.us-east-1-3.ec2.cloud.redislabs.com"
PWD = "zxe4uRRBxbmQdukb2zR8QSdVItKyQ2uZ"
PORT = "16080" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)

# while True:
#     msg = input("Please enter your query (type 'quit' or 'exit' to end):").strip()
#     if msg == 'quit' or msg == 'exit':
#         break
#     if msg == '':
#         continue
#     print("You have entered " + msg, end='') 

#   Add your code here
    # if redis1.get(msg):
    #     redis1.set(msg, int(redis1.get(msg).decode()) + 1)
    # else:
    #     redis1.set(msg, 1)

# Store data as key-value pairs
# redis1.set('help', 'Function List: 1:New Confirmed Cases, 2:Total Cases, 3:Mask, 4:Supplies, 5:News, 6:Rumors, 7:Change Language🇨🇳/🇺🇸. Just type keywords to get the answer!')
# redis1.set('Change Language', 'Please input "use" and language code to select your language:🇨🇳: CH, 🇺🇸:EN.(EX:use CH) You can find other language code in https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes!')
# redis1.set('new confirmed cases', 'Added today: 7')
# redis1.set('total cases', 'Hong Kong Epidemic Statistics-confirmed: 155, death: 4, discharged: 84, hospitalized: 159, excluded: 2330, total reported: 2645.')
# redis1.set('mask', 'At present, you can buy masks through: Watsons: https://www.watsons.com.hk; Mannings: https://www.mannings.com.hk')
# redis1.set('supplies', 'Nucleic acid detection kit:http://www.liferiver.com.cn/newsinfor/p13_205.html?&pageid=13&_id=205&r=0')
# redis1.set('news', 'In the afternoon of March 14th, the last confirmed case in Changsha was discharged from the hospital. So far, all the confirmed cases in Changsha have been cleared. This also means that patients diagnosed with Hunan New Crown Pneumonia are cleared!')
# redis1.set('rumors', 'Extensive exercise during the outbreak can increase resistance? fake!')
print(redis1.get('Change Language').decode())
# print(redis1.get('xxx') == None)

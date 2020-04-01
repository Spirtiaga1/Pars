import requests
main_link='https://api.vk.com/method/friends.getOnline?v=5.52&access_token='
token='282060595038a81503dd904e5b11e1df4ff6c3ac10f155e3d06a9541ae009ef676cfe4f2e1ae60fa03739'
report=requests.get(main_link+token)
print(report)

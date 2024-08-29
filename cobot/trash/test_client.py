import requests
import json

# API 엔드포인트 URL
url = '192.168.58.14:8000/kiosk/order/0/'  # 원하는 엔드포인트의 URL로 변경하세요

# GET 요청을 사용하여 데이터 읽기
response = requests.get(url)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()  # JSON 응답을 딕셔너리로 파싱
    print("읽어온 데이터:", data)
else:
    print("데이터 읽기 실패")

# POST 요청을 사용하여 데이터 작성
new_article = {
    "recipe_name": "recipe 3",
    "coffee_beans": "1",
    "drip_method": "2",
    "ground_amount": "15",
    "brewing_ratio": "2",
    "total_amount": "300"
}

headers = {
    'Content-Type': 'application/json',
}

# response = requests.post(url, data=json.dumps(new_article), headers=headers)

# # 응답 데이터 확인
# if response.status_code == 201:
#     created_data = response.json()
#     print("생성된 데이터:", created_data)
# else:
#     print("데이터 작성 실패")

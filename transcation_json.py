# 翻译json文件
import argparse
import requests
import json
import os
from urllib import  parse
def trancation(item:dict)->dict:
    try:
        print(f"翻译:{item['Dialogue']}")
        if item.get("trans"):
            print("已经翻译跳过")
            return item
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&hl=zh-CN&dt=t&dt=bd&dj=1&source=input&tk=785991.785991&q={parse.quote(item['Dialogue'])}"

        payload={}
        headers = {
            'authority': 'translate.googleapis.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'none',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'x-client-data': 'CIi2yQEIpLbJAQjBtskBCKmdygEIlPLKAQiUocsBCOSXzQEIhaDNAQi+os0B'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        trans=response.json()['sentences'][0]['trans']
        item['trans']=trans
        print(f"翻译:{item['Dialogue']},结果:{trans}")
    except:
        print(f"翻译异常:{item['Dialogue']}")
    return item
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/preprocess")
    args = parser.parse_args()
   
    if os.path.exists(args.data_path):
        json_files = [f for f in os.listdir(args.data_path) if os.path.isfile(os.path.join(args.data_path, f)) and f.endswith('.json')]
        for json_file in json_files:
            print(f"开始处理文件：{json_file}")
            json_path = os.path.join(args.data_path, json_file)
            with open(json_path, 'r',encoding='utf-8') as f:
                json_data = json.load(f)
            # 翻译所有数据
            json_data =[ trancation(item) for item in json_data[0:]]
            # 保存json文件
            with open(json_path, 'w') as f:
                json.dump(json_data, f)
            print("处理成功")

        pass
    else:
        print(f"{args.data_path}文件夹不存在")

if __name__ == "__main__":
    main()
# 数据处理，将csv数据转换为json格式
import argparse
import json
import os
import requests
from urllib import  parse
def format_example(example: dict) -> dict:
    context = f"Instruction: {example['instruction']}\n"
    if example.get("input"):
        context += f"Input: {example['input']}\n"
    context += "Answer: "
    target = example["output"]
    return {"context": context, "target": target}

def trancation(item:dict)->dict:
    try:
        print(f"翻译:{item['Dialogue']}")
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&hl=zh-CN&dt=t&dt=bd&dj=1&source=input&tk=785991.785991&q={parse.quote(input)}"

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
        item['trans']=response.json()['sentences'][0]['trans']
    except:
        print(f"翻译异常:{item['Dialogue']}")
    return item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/original")
    parser.add_argument("--save_path", type=str, default="data/preprocess")
    args = parser.parse_args()
    if os.path.exists(args.data_path):
        csv_files = [f for f in os.listdir(args.data_path) if os.path.isfile(os.path.join(args.data_path, f)) and f.endswith('.csv')]
        for csv_file in csv_files:
            print(f"开始处理文件：{csv_file}")
            csv_path = os.path.join(args.data_path, csv_file)
            with open(csv_path, 'r',encoding='utf-8') as f:
                csv_data = f.readlines() # 读取csv文件内容
            # 转换为json格式
            json_data = [dict(zip(csv_data[0].strip().split(','), row.strip().split(','))) for row in csv_data[1:]]
            # 翻译所有数据
            json_data =[ trancation(item) for item in json_data[0:]]
           
            # 保存为json文件
            if not os.path.exists(args.save_path):
                os.makedirs(args.save_path)
            json_path = os.path.join(args.save_path, csv_file.replace('.csv', '.json'))
            with open(json_path, 'w') as f:
                json.dump(json_data, f)

            print("处理成功")

        pass
    else:
        print(f"{args.data_path}文件夹不存在")
    pass
if __name__ == "__main__":
    main()
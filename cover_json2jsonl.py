import argparse
import json
from tqdm import tqdm
import os


def format_item(item: dict) -> dict:
    if item.get('prev'):
        context = f"Instruction: {item['prev']['trans']}\n"
    else:
        context = f"Instruction: \n"
    context += "Answer: "
    target = item["trans"]
    return {"context": context, "target": target}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/trans")
    parser.add_argument("--save_path", type=str, default="data/output")

    args = parser.parse_args()
    """ 数据预处理 """
    if os.path.exists(args.data_path):
        json_files = [f for f in os.listdir(args.data_path) if os.path.isfile(os.path.join(args.data_path, f)) and f.endswith('.json')]
        # 预处理相关相关数据
        result_map={}
        for json_file in json_files:
            print(f"开始处理文件：{json_file}")
            json_path = os.path.join(args.data_path, json_file)
            with open(json_path, 'r',encoding='utf-8') as f:
                json_data = json.load(f)
            for i in range(1,len(json_data)):
                # 获取当前对象和前一个对象
                current_obj = dict(json_data[i])
                prev_obj = json_data[i-1] if i > 1 else None
                # 如果不是第一个对象，则将前一个对象作为当前对象的属性
                if prev_obj:
                    current_obj["prev"] = prev_obj
                if not result_map.get(current_obj['Character']):
                    result_map[current_obj['Character']]=[]
                result_map[current_obj['Character']].append(current_obj)
        if not os.path.exists(args.save_path):
                os.makedirs(args.save_path)
        for key,value in result_map.items():
            print(f"开始处理:{key}")
            file_path= os.path.join(args.save_path, f"{key.replace(' ','')}_alpaca_data.jsonl")
            # 翻译所有数据
            # 处理json文件
            with open(file_path, 'w') as f:
                for item in tqdm(value, desc="formatting.."):
                    f.write(json.dumps(format_item(item),ensure_ascii=False) + '\n')

        pass
    else:
        print(f"{args.data_path}文件夹不存在")


if __name__ == "__main__":
    main()
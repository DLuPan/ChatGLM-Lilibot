# 数据处理，将csv数据转换为json格式
import argparse
import json
import os

def format_example(example: dict) -> dict:
    context = f"Instruction: {example['instruction']}\n"
    if example.get("input"):
        context += f"Input: {example['input']}\n"
    context += "Answer: "
    target = example["output"]
    return {"context": context, "target": target}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/original")
    parser.add_argument("--save_path", type=str, default="data/preprocess")
    args = parser.parse_args()
    if os.path.exists(args.data_path):
        csv_files = [f for f in os.listdir(args.data_path) if os.path.isfile(os.path.join(args.data_path, f)) and f.endswith('.csv')]
        for csv_file in csv_files:
            csv_path = os.path.join(args.data_path, csv_file)
            with open(csv_path, 'r',encoding='utf-8') as f:
                csv_data = f.readlines() # 读取csv文件内容
            # 转换为json格式
            json_data = [dict(zip(csv_data[0].strip().split(','), row.strip().split(','))) for row in csv_data[1:]]
            
            # 遍历JSON列表
            result=[]
            for i in range(len(json_data)):
                # 获取当前对象和前一个对象
                current_obj = dict(json_data[i])
                prev_obj = json_data[i-1] if i > 0 else None

                # 如果不是第一个对象，则将前一个对象作为当前对象的属性
                if prev_obj:
                    current_obj["prev"] = prev_obj
                result.append(current_obj)
            # 保存为json文件
            if not os.path.exists(args.save_path):
                os.makedirs(args.save_path)
            json_path = os.path.join(args.save_path, csv_file.replace('.csv', '.json'))
            with open(json_path, 'w') as f:
                json.dump(result, f)

        pass
    else:
        print(f"{args.data_path}文件夹不存在")
    pass
if __name__ == "__main__":
    main()
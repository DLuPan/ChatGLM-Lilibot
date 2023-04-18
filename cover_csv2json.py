# 数据处理，将csv数据转换为json格式
import argparse
import json
import os



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
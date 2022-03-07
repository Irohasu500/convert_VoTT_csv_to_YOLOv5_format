import glob
from mimetypes import init
import os
import subprocess
import anotation_info

### 自己責任でお願い致します ###

########################## メタ情報　###############################
# ラベルの一覧が保存されたファイルのファイル名
label_list_file_name = "labels.txt" 

# VoTTで出力したcsvファイル
csv_file_path = "./vott-csv-export/anotations.csv"

# アノテーション対象の画像を格納したフォルダ
image_folder_path = "./vott-csv-export"

# (出力先) 画像
train_image_path = "./data/train/images"

# (出力先) ラベル
train_label_data_path = "./data/train/labels"

# 検証用画像
valid_image_path = "./data/valid"

########################## メタ情報　###############################

class_num:int = 0
index_to_labelname:dict = {}
label_name_list = []
annotations_list = []

def get_label_info():
    global label_list_file_name,index_to_labelname,label_name_list,class_num
    # ラベルの一覧が保存されたファイルからラベルの一覧を取り出す。
    with open(label_list_file_name, "r") as f:
        text = f.read()
        aline_info = text.split("\n")
        for aline in aline_info:
            if aline:
                label_index,label_name = aline.split(",")
                index_to_labelname[label_index] = label_name
                label_name_list.append(label_name)
                class_num += 1

    print("#"* 100)
    print(f"検出対象のラベルは、{index_to_labelname}です。")
    print(f"総ラベル数：{class_num}")
    print("#"* 100)

def import_anotationInfo_from_csv(csv_file_path:str):
    # CSVファイルから情報を読み取って画像に対応するtxtファイルを作成していく。
    with open(csv_file_path, "r") as f:
        text = f.read()
        aline_info = text.split("\n")
        annotations_list = aline_info[1:]
    return annotations_list

def images_copy(images_folder_path:str,image_out_path:str):
    default_path = os.getcwd()
    # 出力先の絶対パスを取ってくる。
    os.chdir(image_out_path)
    image_out_full_path = os.getcwd()
    os.chdir(default_path)
    os.chdir(images_folder_path)
    object = './*.jpg'
    flist = glob.glob(object)
    print("対象の画像")
    print(flist)
    for image in flist:
        command = f"copy {image} {image_out_full_path} "
        print(f"実行するコマンド：{command}")
        subprocess.run(command,shell=True)
    os.chdir(default_path)

def gen_data_yaml(train_image_path:str,valid_image_path:str,label_name_list:list):
    label_num = len(label_name_list)
    default_path = os.getcwd()
    out_str =   f"train: {train_image_path} \n" + \
                f"val: {valid_image_path}\n" + \
                f"\n" + \
                f"nc: {label_num}\n" + \
                f"names: {label_name_list}"
    with open("./data.yaml" , "w") as wf:
        wf.write(out_str)
    os.chdir(default_path)

########################## func ################################

if __name__ == "__main__":
    get_label_info()
    print(label_name_list)
    annotations_list = import_anotationInfo_from_csv(csv_file_path)
    print(annotations_list[0])
    Manager:anotation_info.annotation_Info_Manager = anotation_info.annotation_Info_Manager(label_name_list)
    for annotation_info in annotations_list:
        image_file_name, xmin, ymin, xmax, ymax, label = annotation_info.split(",")
        Manager.set_annotation_Info(image_file_name.replace('"',''), float(xmin), float(ymin), float(xmax), float(ymax), label.replace('"',''))
    
    # CSVファイルの情報から、出力ファイルの情報を生成 ※出力はしていないので注意。
    Manager.make_for_YOLO_txt_per_image()

    # フォルダの生成。
    Manager.preset_folders(train_label_data_path,train_image_path)

    # 実際に出力
    Manager.gen_folders_snapshot(train_label_data_path)

    # 画像を全てコピー
    images_copy(image_folder_path,train_image_path)

    # 最後にdata.yamlを生成。
    gen_data_yaml(train_image_path,valid_image_path,label_name_list)
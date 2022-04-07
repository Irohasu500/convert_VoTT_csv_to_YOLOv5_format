import glob
from mimetypes import init
import os
import subprocess
import re

## label.txtを生成するプログラム
## こちらのプログラムは単体で動作します。

## EN : program which generate "label.txt".
## EN : This program works independently.

########################## set this value　###############################
############################# メタ情報　###############################

# ラベルの一覧が保存されたファイルのファイル名
# EN : You can set output file name for other than "labels.txt"
label_list_file_name = "labels.txt" 

# VoTTで出力したcsvファイル
# EN : CSV file which VoTT output 
csv_file_path = "./anotation_movie-export.csv"

########################## set this value　###############################
############################# メタ情報　###############################

label_name_list = []

def add_label(label_name:str):
    global label_name_list
    if not (label_name in label_name_list):
        label_name_list.append(label_name)

def ref_VoTT_csv_file(csv_file_path:str):
    with open(csv_file_path, "r") as rf:
        csv_contents = rf.read()
        contents_per_lines = csv_contents.split("\n")
        for a_line_contents in contents_per_lines:
            if a_line_contents:
                image,xmin,ymin,xmax,ymax,label = a_line_contents.split(",")
                add_label(label)

def generate_labels_txt_contents(label_list:list):
    i:int = 0
    generated_str:str = ""
    for label in label_list:
        label = trim_str_quotations(label)
        generated_str = generated_str + "{0},{1}\n".format(i,label)
        i += 1
    generated_str = generated_str[0:len(generated_str) - 1]
    return generated_str

def write_labels_txt(label_list:list,label_list_file_name:str):
    output_contents = generate_labels_txt_contents(label_list)
    with open(label_list_file_name, "w") as wf:
        wf.write(output_contents)
    print("出力完了")

def trim_str_quotations(_str:str):
    pattern = "\"([^\"])*\""
    if re.match(pattern, pattern):
    # if (_str[0] == '"') and (_str[len(_str) -1 ] == '"'):
        a= _str[1:len(_str)-1]
        print(a)
        return a

if __name__ == "__main__":

    # CSV ファイルを参照
    ref_VoTT_csv_file(csv_file_path)

    # labels.txtを生成
    write_labels_txt(label_name_list,label_list_file_name)
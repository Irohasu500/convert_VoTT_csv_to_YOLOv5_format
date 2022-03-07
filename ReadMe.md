# VoTT(csv) to folders for YOLO

## テスト済み動作環境
windows10で動作  
Python 3.8.5  

macOSやUbuntu、その他の方はsubprocess.runメソッドの実行部分の  
copyコマンドなどを各OSに合わせて実行してみてください。  

## このプログラムの機能
VoTTから出力されるアノテーション付き画像データを
YOLOで学習できるフォルダ形式に変換します。  
**data.yaml**も出力します。

## 使用方法
set_label_txt.pyの上部にある下記のメタ変数を埋めて実行してください。
(相対パスでお願い致します。)

*label_list_file_name = "labels.txt"  
*csv_file_path = "./vott-csv-export/anotations.csv"  
*image_folder_path = "./vott-csv-export"  
*train_image_path = "./data/train/images"  
*train_label_data_path = "./data/train/labels"  

**label_list_file_name**はラベルの一覧を記載したtxtファイル(後述)、  
**csv_file_path**はVoTTが出力したCSVファイル、  
**image_folder_path**はVoTTでアノテーションを付けた画像ファイル、  
**train_image_path**は画像の出力先、  
**train_label_data_path**はラベルの出力先です。  


***

## 出力ファイル形式
画像は**train_image_path**で指定したパスに、  
ラベルは**train_label_data_path**で指定したパスに出力されます。

***

## ラベルの一覧
下記のように記載してください。  
0,person  
1,girl  
2,boy  
3,office_worker  
4,man  
5,student  
6,dog  

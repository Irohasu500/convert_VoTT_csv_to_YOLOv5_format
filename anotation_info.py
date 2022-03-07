import glob
from mimetypes import init
import os

# main中でアクセスする必要はない。
class annotation_Info:

    def __init__(self, image_file_name, xmin, ymin, xmax, ymax, label):
        self.image_file_name:str = image_file_name
        self.xmin:float = xmin
        self.ymin:float = ymin
        self.xmax:float = xmax
        self.ymax:float = ymax
        self.label:str = label

    def get_x_y_center(self):
        return (self.xmin + self.xmax)/2, (self.ymin + self.ymax)/2

    def get_height(self):
        return (self.ymax - self.ymin)

    def get_width(self):
        return (self.xmax - self.xmin)
    
    def get_label_name(self):
        return self.label

    def get_image_name(self):
        return self.image_file_name

# こちらからメインでアクセスする
class annotation_Info_Manager:
    def __init__(self,label_list:list):
        self.label_list:list = label_list
        self.annotation_Info_list_in:list[annotation_Info] = []
        self.annotation_Info_list_out:list = []
        self.text_per_image:dict[str:str] = {}
    
    def set_annotation_Info(self, image_file_name:str, xmin:float, ymin:float, xmax:float, ymax:float, label:str):
        new_annotation_Info = annotation_Info(image_file_name, xmin, ymin, xmax, ymax, label)
        self.annotation_Info_list_in.append(new_annotation_Info)
        
    def make_for_YOLO_txt_per_image(self):
        self.text_per_image = {}
        for an_annotation_Info in self.annotation_Info_list_in:
            index = self.label_list.index(an_annotation_Info.get_label_name())
            x_center,y_center = an_annotation_Info.get_x_y_center()
            width = an_annotation_Info.get_width()
            height = an_annotation_Info.get_height()
            aline = f"{index} {x_center} {y_center} {width} {height}\n"
            image_name = an_annotation_Info.get_image_name()
            if image_name in self.text_per_image.keys():
                self.text_per_image[image_name] = self.text_per_image[image_name] +  aline
            else:
                self.text_per_image[image_name] = aline
        print(self.text_per_image)

    def gen_folders_snapshot(self,out_label_folder_path:str):
        for key in self.text_per_image.keys():
            out_label_file_path = out_label_folder_path + "/" + key.replace(".jpg", ".txt")
            out_contants = self.text_per_image[key]
            print(f"次のファイルを記載しています。：{out_label_file_path}")
            with open(out_label_file_path, "w") as wf:
                wf.write(out_contants)

    # ./data/train/images
    def preset_folders(self,out_label_folder_path:str,out_image_folder_path:str ):
        out_label_folder_path_l = out_label_folder_path.replace(".","")
        out_image_folder_path_l = out_image_folder_path.replace(".","")
        label_folders = out_label_folder_path_l.split("/")
        image_folders = out_image_folder_path_l.split("/")
        default_path = os.getcwd()
        # ラベル用
        for folder in label_folders:
            now = f"./{folder}"
            if not os.path.exists(now):
                print(f"次のフォルダを生成します...。：{folder}")
                os.mkdir(now)
            else:
                print(f"既に存在しています。フォルダ名：{folder}")
            os.chdir(now)
        os.chdir(default_path)
        # ラベル用
        for folder in image_folders:
            now = f"./{folder}"
            if not os.path.exists(now):
                print(f"次のフォルダを生成します...。：{folder}")
                os.mkdir(now)
            else:
                print(f"既に存在しています。フォルダ名：{folder}")
            os.chdir(now)
        os.chdir(default_path)
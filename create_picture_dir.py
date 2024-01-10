import os
def create_dir(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder {folder_name} created successfully!")
    # else:
        # print(f"Folder {folder_name} already exists!")

def create_picture_dir():
    create_dir('图片')
    create_dir('图片/chart1图片')
    create_dir('图片/table1图片')
    create_dir('图片/table2图片')
    create_dir('图片/table3图片')

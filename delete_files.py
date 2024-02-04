import os
import glob


def delete_pdf():
    # 获取当前目录下所有的PDF文件
    pdf_files = glob.glob('*.pdf')

    # 遍历文件列表，逐个删除
    for pdf_file in pdf_files:
        if not pdf_file.startswith("template"):
            try:
                os.remove(pdf_file)
                print(f"Deleted: {pdf_file}")
            except Exception as e:
                print(f"Error deleting {pdf_file}: {e}")
        else:
            # 如果文件以"template"开头，不删除
            print(f"Skipped: {pdf_file}")

    print("All required PDF files in the current folder have been deleted.")

def delete_jpg(folder_path):
    # 构造搜索路径来匹配所有的.jpg文件
    jpg_files_path = os.path.join(folder_path, '*.jpg')

    # 获取文件夹下所有的.jpg文件
    jpg_files = glob.glob(jpg_files_path)

    # 遍历文件列表，逐个删除
    for jpg_file in jpg_files:
        try:
            os.remove(jpg_file)
            print(f"Deleted: {jpg_file}")
        except Exception as e:
            print(f"Error deleting {jpg_file}: {e}")

    print(f"All JPG files in the {folder_path} folder have been deleted.")

# delete_pdf()
# delete_jpg('图片/chart1图片')
# delete_jpg('图片/chart2图片')
# delete_jpg('图片/table1图片')
# delete_jpg('图片/table2图片')
# delete_jpg('图片/table3图片')


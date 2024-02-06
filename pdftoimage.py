from pdf2image import convert_from_path
import os
import glob

def convert_pdf_to_images(target_folder='研报图片'):
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # 获取当前目录下所有的PDF文件
    pdf_files = glob.glob('*.pdf')
    
    for pdf_file in pdf_files:
        if not pdf_file.startswith("template"):
            # 获取不带扩展名的PDF文件名
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            
            # 将PDF文件的每一页转换为图片
            pages = convert_from_path(pdf_file, 400)  # 300 DPI是一个比较好的折中选择
            
            # 保存图片到指定的目录，图片名格式为原名.jpg
            for i, page in enumerate(pages):
                image_filename = os.path.join(target_folder, f'{base_name}_{i+1}.jpg')
                page.save(image_filename, 'JPEG')
                print(f'Saved {image_filename}')
    
    print("Conversion completed for all required PDF files.")

# # 调用函数
# convert_pdf_to_images()

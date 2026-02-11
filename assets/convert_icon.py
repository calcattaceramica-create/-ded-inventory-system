from PIL import Image
import sys

try:
    # فتح الصورة
    img = Image.open(r'C:\Users\DELL\DED\assets\app_icon.png')
    
    # تحويل إلى RGB إذا كانت RGBA
    if img.mode == 'RGBA':
        # إنشاء خلفية بيضاء
        background = Image.new('RGB', img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # حفظ كأيقونة بأحجام متعددة
    icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(r'C:\Users\DELL\DED\assets\app_icon.ico', format='ICO', sizes=icon_sizes)
    print('تم إنشاء الأيقونة بنجاح')
except Exception as e:
    print(f'خطأ: {e}')
    sys.exit(1)

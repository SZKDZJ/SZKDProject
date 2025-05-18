import matplotlib.font_manager
import matplotlib.pyplot as plt

# 列出所有可用字体
fonts = matplotlib.font_manager.findSystemFonts()
for font in fonts:
    if 'SimHei' in font:
        print(f"SimHei 字体可用: {font}")
    elif '微软雅黑' in font:
        print(f"黑体字体可用: {font}")
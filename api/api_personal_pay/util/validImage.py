import string
from random import randint, sample
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from config.config import Config
import base64
from io import BytesIO
from config.config import Config


class ValidImage:
    # word_type=0生成4个数字,wordtype=1生成4个字母
    @classmethod
    def create(cls, word_type=0):
        # 定义变量
        img_size = (110, 50)  # 定义画布大小
        img_rgb = (248, 248, 248)  # 定义画布颜色，白色
        img = Image.new("RGB", img_size, img_rgb)

        img_text = ''
        if word_type == 0:
            img_text = " ".join(sample(string.digits, 4))
        else:
            img_text = " ".join(sample(string.ascii_letters, 4))
        # print(img_text.replace(' ',''))
        code = img_text.replace(' ','')

        # 画图
        drow = ImageDraw.Draw(img)
        for i in range(10):
            # 随机画线
            drow.line([tuple(sample(range(img_size[0]), 2)), tuple(sample(range(img_size[0]), 2))], fill=(0, 0, 0))
        for i in range(99):
            # 随机画点
            drow.point(tuple(sample(range(img_size[0]), 2)), fill=(0, 0, 0))

        # 文字
        font = ImageFont.truetype(Config.ROOT_PATH + "/src/font/Verdana Italic.ttf", 24)  # 定义文字字体和大小
        drow.text((6, 6), img_text, font=font, fill="green")

        # 扭曲图片和滤镜
        params = [
            1 - float(randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(randint(1, 10)) / 100,
            float(randint(1, 2)) / 500,
            0.001,
            float(randint(1, 2)) / 500
        ]
        img = img.transform(img_size, Image.PERSPECTIVE, params)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # 模糊:
        # image.filter(ImageFilter.BLUR)

        # code_name = '{}.jpg'.format('valid')
        # save_dir = '/{}'.format(code_name)
        # img.save(Config.ROOT_PATH + save_dir, 'jpeg')
        # print("已保存图片: {}".format(save_dir))

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        return {
            "img": 'data:image/jpeg;base64,' + bytes.decode(img_str),
            "code": code
        }

from PIL import Image, ImageDraw, ImageFont
import json
import pymorphy2

class Drawer():
    def __init__(self):
        self.data = self.get_data()
        self.image = self.get_pattern()
        self.morph = pymorphy2.MorphAnalyzer()
        self.starting_pos = (276, 580)
        self.font = ImageFont.truetype('arial.ttf', 35)
        self.draw = ImageDraw.Draw(self.image)
        self.schedule_maker()
        self.image_save()

    def get_data(self):
        with open('test_alarm.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    def schedule_maker(self):
        schedule = {}
        for key, value in self.data.items():
            pos = self.starting_pos
            if key == "id":
                continue
            else:
                if key == "Пн":
                    day_num = 1
                    pos = self.Xposition_move(pos, day_num)
                elif key == "Вт":
                    day_num = 2
                    pos = self.Xposition_move(pos, day_num)
                elif key == "Ср":
                    day_num = 3
                    pos = self.Xposition_move(pos, day_num)
                elif key == "Чт":
                    day_num = 4
                    pos = self.Xposition_move(pos, day_num)
                elif key == "Пт":
                    day_num = 5
                    pos = self.Xposition_move(pos, day_num)
                elif key == "Сб":
                    day_num = 6
                    pos = self.Xposition_move(pos, day_num)
                elif key == "Вс":
                    day_num = 7
                    pos = self.Xposition_move(pos, day_num)
                else:
                    continue
                for lesson in value:
                    if not lesson["class_num"].isdigit():
                        continue
                    pos = self.Yposition_move(pos, lesson["class_num"])
                    name = lesson["lesson"].split()
                    if len(name) > 3:
                        name = name[-3:]
                    else:
                        for word in name:
                            if len(word) <= 2:
                                name.remove(word)
                        name = name[:3]
                    for word in name:
                        if len(word) <= 2:
                            name.remove(word)
                    print(name)
                    short_name = []
                    vowels = [ 'у', 'е', 'ы', 'а', 'о', 'э', 'я', 'и', 'ю']
                    for word in name:
                        short_word = word
                        if len(word) > 10:
                            short_word = self.morph.parse(word)[0].inflect({'sing', 'nomn'}).word[:11]
                            while short_word[-1] in vowels:
                                short_word = short_word[:-1]
                        short_name.append(short_word)
                    # 20
                    short_name[0] = short_name[0].capitalize()
                    for word in short_name:
                        if lesson["type_lesson"] == "Лек":
                            self.draw.text(pos, word, font=self.font, fill=(135, 206, 235))
                            pos = (pos[0], pos[1] + 32)
                        else:
                            self.draw.text(pos, word, font=self.font, fill=(217, 33, 33))
                            pos = (pos[0], pos[1] + 32)

    def get_pattern(self):
        image = Image.open('pattern.png')
        return image

    def image_save(self):
        self.image.save('test3.png')

    def Yposition_move(self, pos, num):
        next_pos = (pos[0], self.starting_pos[1] + 117*(int(num) - 1))
        return next_pos

    def Xposition_move(self, pos, day):
        # 245
        next_pos = None
        for i in range(0, day):
            next_pos = (pos[0] + 245 * i, pos[1])
        return next_pos

p = Drawer()

# 135, 206, 235 light blue
# 217, 33, 33 red

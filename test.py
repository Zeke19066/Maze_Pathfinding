import PIL
import os
import cv2


class Capture():
    def __init__(self):
        self.parent_dir = r"GIFMAKER"
        self.subdir = ""
        self.game_count = 0
        self.img_count = 0


    def snap_maker(self, img, new_game_bool):
        if new_game_bool:
            self.game_count += 1
            self.img_count = 0
            self.subdir = os.path.join(self.parent_dir, self.game_count)
            os.mkdir(self.subdir)
            os.chdir(self.subdir)
        self.img_count += 1
        cv2.imwrite(self.game_count+"-"+self.img_count+".png", img)

    def gif_maker(self):
        pass

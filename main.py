from modules.Character2Tags import Character2Tags
from modules.data2html import render

i = Character2Tags()
i.fromfile('./catch/dataanalyze_arknights#1629052559.json')
render(i.t_tags_d_character('barefoot'),'裸足','明日方舟xp分析','占该角色所有色图的百分比')
from modules.Character2Tags import Character2Tags
from modules.data2html import render

def main():
    i = Character2Tags()
    # i.fromkeyword('arknights','./catch/getlinks_1629098074.json')
    i.fromfile('./catch/dataanalyze_genshin_impact+-rating_safe#1629107542.json')
    # render(i.t_tags_d_character('uniform'),'制服','明日方舟xp分析','bar','%inall')

    # i.fromkeyword('genshin_impact+-rating:safe')
    render(i.t_tags_d_character('bdsm','genshin impact'),'bdsm','原神xp分析','bar','%inall')
if __name__ == '__main__':
    main()
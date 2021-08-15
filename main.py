from modules.Character2Tags import Character2Tags

i = Character2Tags()
i.fromfile('./catch/dataanalyze_arknights#1629052559.json')
print(i.t_tags_d_character('barefoot'))
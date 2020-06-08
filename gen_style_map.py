import os


def gen_style_map_file(style_name='', map_name=''):
    with open(style_name+'.txt', 'w') as f:
        # terrain related
        terrain_array = ['cliff', 'grass', 'moss', 'noise', 'soil', 'stone']
        for item in terrain_array:
            f.write(f'data\\source\\maps_source\\texture\\terraintexture\\{item} data\\style_transfer\\data\\source\\ma'
                    f'ps_source\\texture\\terraintexture\\{item}\\expanded\\dds_output\\{style_name}\\\n')

        # foliage related
        f.write(f'data\\source\\maps_source\\texture\\foliage\\texture\\ data\\style_transfer\\data\\source\\maps_sour'
                f'ce\\foliage\\texture\\dds_output\\{style_name}\\\n')

        # base texture related
        f.write(f'data\\source\\maps_source\\texture\\ data\\style_transfer\\data\\source\\maps_source\\texture\\dds_'
                f'output\\{style_name}\\\n')
        f.write(f'data\\source\\texture\\ data\\style_transfer\\data\\source\\texture\\dds_output\\{style_name}\\\n')

        # map related
        f.write(f'data\\source\\maps\\{map_name}\\baked\\ data\\style_transfer\\data\\source\\maps\\{map_name}\\bak'
                f'ed\\dds_output\\{style_name}\\\n')


if __name__ == "__main__":
    gen_style_map_file('5', '稻香村')
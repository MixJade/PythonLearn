from utils.convertCase import snake_to_camel

with open('ibatis的插入列.txt', 'r') as file:
    for line in file:
        if line.endswith(",\n"):
            print(f'{line[:-2]}=#{snake_to_camel(line[:-2])}#,\n', end='')
        else:
            print(f'{line}=#{snake_to_camel(line)}#', end='')

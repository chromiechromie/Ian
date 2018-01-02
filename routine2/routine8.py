print('  *', ' * *', '* * *', '  | ', sep='\n')


def text_create(name, msg):
    file_path = 'D:/routine/python/routine3IO.txt'
    with open(file_path, 'r') as f:  # 相当于try catch
        for line in f.readlines():
            print(line.strip())  # 把末尾的/n 去掉 --- 啥意思!!!∑(ﾟДﾟノ)ノ


text_create(1, 2)

print('\n'.join([''.join([('AndyLove'[(x - y) % 8] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (
                                                                                                                y * 0.1) ** 3 <= 0 else' ')
                    for x in range(-30, 30)]) for y in range(15, -15, -1)]))


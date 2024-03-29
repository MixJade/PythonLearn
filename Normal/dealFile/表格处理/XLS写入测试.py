import xlwt

workbook = xlwt.Workbook(encoding='utf-8')  # 设置一个workbook，其编码是utf-8
worksheet = workbook.add_sheet("test_sheet")  # 新增一个sheet
a = [1, 2, 3, 4, 5]  # 列1
b = ['a', 'b', 'c', 'd', 'e']  # 列2
worksheet.write(0, 0, label='列1')  # 将‘列1’作为标题
worksheet.write(0, 1, label='列2')  # 将‘列2’作为标题
for i in range(len(a)):  # 循环将a和b列表的数据插入至excel
    worksheet.write(i + 1, 0, label=a[i])
    worksheet.write(i + 1, 1, label=b[i])
workbook.save(r"xlwt_test.xls")  # 这里save需要特别注意，文件格式只能是xls

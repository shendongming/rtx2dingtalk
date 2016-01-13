# coding:utf-8
"""
rtx xml 转csv 文件
"""
import re
import sys

from lxml import etree

if len(sys.argv) < 3:
    print('''
param error

python xml2csv.py rtx.xml out.csv

'''
          )
    sys.exit(0)
f, out = sys.argv[1:3]

# xml 格式有问题
xml = open(f).read().decode('gb18030')

# 用户
users = {}
# 部门
deps = {}
for row in re.findall(u'<Item.+?/>', xml):
    e = etree.fromstring(row)
    # 用户节点
    if len(e.xpath('//@UserName')):
        user = {
            'UserName': e.xpath('//@UserName')[0],
            'Gender': e.xpath('//@Gender')[0],
            'Mobile': e.xpath('//@Mobile')[0],
            'Email': e.xpath('//@Email')[0],
            'id': e.xpath('//@ID')[0],
            'dep': []

        }
        users[user['id']] = user

    # 部门
    if len(e.xpath('//@DeptName')):
        dep = {
            'id': e.xpath('//@DeptID')[0],
            'pid': e.xpath('//@PDeptID')[0],
            'name': e.xpath('//@DeptName')[0],
        }
        deps[dep['id']] = dep

for row in re.findall(u'<Item.+?/>', xml):
    e = etree.fromstring(row)
    if len(e.xpath('//@DeptID')) and len(e.xpath('//@UserID')):
        # 员工部门关系
        users[e.xpath('//@UserID')[0]]['dep'].append(e.xpath('//@DeptID')[0])


# 获取全称
def get_full_name(d):
    p = [d['name']]
    while 1:
        if d['pid'] not in deps:
            break
        d2 = deps[d['pid']]
        p.insert(0, d2['name'])
        d = d2
    return '-'.join(p)


fp = open(out, 'w')
fp.write('员工UserID\t部门\t姓名\t性别\t手机号\t邮件\n')

for u in users.values():
    print(' ' + u['UserName'].encode('utf-8'))
    dep = ','.join([get_full_name(deps[p]) for p in u['dep']])
    fp.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (
        u['id'].encode('utf-8'), dep.encode('utf-8'), u['UserName'].encode('utf-8'), u['Gender'].encode('utf-8'),
        u['Mobile'].encode('utf-8'), u['Email'].encode('utf-8')))

fp.close()
print('done: %s' % out)

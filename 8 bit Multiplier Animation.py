import c4d
from c4d import documents


def setunit(inlist):
    x = inlist[0]
    y = inlist[1]
    a = inlist[2]
    c = inlist[3]
    return x + 2 * y + 4 * a + 8 * c


def xinput(n):   #返回某一单元的传输x
    x = 1
    for k in range(0, 8):
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[2 * k]:
            x = 0
            break
    return x


def yinput(n):   #返回某一单元的传输y
    y = 1
    for k in range(0, 4):
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[4 * k] \
        or instances[n][c4d.INSTANCEOBJECT_LINK] == units[4 * k + 1]:
            y = 0
            break
    return y


def qoutput(n):   #返回某一单元的输出q
    q = 1
    for k in [0, 1, 2, 7, 11, 12, 13, 14]:
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[k]:
            q = 0
            break
    return q


def doutput(n):   #返回某一单元的输出q
    d = 0
    for k in [7, 11, 12, 13, 14, 15]:
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[k]:
            d = 1
            break
    return d


def unitinput(i,j,step,xlist,ylist):
    #c
    if i <> 0:   #不是最低位
        c = doutput(n - 1)
    else:   #是最低位
        c = 0
    
    #a
    if j == 0:   #是第一行
        a = 0
    else:
        if i <> 7:   #不是第一行且不是最高位
            a = qoutput(n - 7)
        if i == 7:   #不是第一行但是最高位
            a = doutput(n - 8)
    
    #x
    if j <> 0:   #不是第一行
        x = xinput(n - 8)   #获得上面单元的传输x
    else:   #是第一行
        if i == step:   #步数等于当前x位数
            x = int(xlist[step])
        else:
            x = xinput(n)
    
    #y
    if step >= 7 - i + j:   #限制y传输一次到底
        if i <> 7:   #不是最高位
            y = yinput(n + 1)   #获得左边单元的传输y
        else:   #是最高位
            if j == step:   #步数等于当前y位数
                y = int(ylist[step])
            else:
                y = yinput(n)
    else:   #远处的y保持原状
        y = yinput(n)
    
    return [x,y,a,c]


def main():
    control = doc.GetActiveObject()
    if control[c4d.ID_USERDATA,3]:   #脚本为启用状态
        controlchild = control.GetChildren()   #获取此对象子集列表
        global n, units, instances, xin, yin, lout, hout
        units = controlchild[0].GetChildren()   #获取元件列表
        instances = controlchild[1].GetChildren()   #获取实例列表
        xin = controlchild[2].GetChildren()   #获取x输入列表
        yin = controlchild[3].GetChildren()   #获取y输入列表
        lout = controlchild[4].GetChildren()   #获取低输出列表
        hout = controlchild[5].GetChildren()   #获取高输出列表
        xlist = control[c4d.ID_USERDATA,21][::-1]   #逆序X输入
        ylist = control[c4d.ID_USERDATA,22][::-1]   #逆序Y输入
        step = control[c4d.ID_USERDATA,1]   #步数
        for j in range(7, -1, -1):   #每行
            if ylist[j] == '0':   #输入y方块更新
                yin[j][c4d.INSTANCEOBJECT_LINK] = units[16]
            else:
                yin[j][c4d.INSTANCEOBJECT_LINK] = units[17]
            for i in range(7, -1, -1):   #每列
                if xlist[i] == '0':   #输入x方块更新
                    xin[i][c4d.INSTANCEOBJECT_LINK] = units[16]
                else:
                    xin[i][c4d.INSTANCEOBJECT_LINK] = units[17]
                n = j * 8 + i   #二维坐标转一维
                instances[n][c4d.INSTANCEOBJECT_LINK] = \
                units[setunit(unitinput(i,j,step,xlist,ylist))]
                if i == 0:
                    if qoutput(n) == 0:
                        lout[j][c4d.INSTANCEOBJECT_LINK] = units[16]
                    else:
                        lout[j][c4d.INSTANCEOBJECT_LINK] = units[17]
                if j == 7 and i > 0:
                    if qoutput(n) == 0:
                        hout[i-1][c4d.INSTANCEOBJECT_LINK] = units[16]
                    else:
                        hout[i-1][c4d.INSTANCEOBJECT_LINK] = units[17]
                if j == 7 and i == 7:
                    if doutput(n) == 0:
                        hout[i][c4d.INSTANCEOBJECT_LINK] = units[16]
                    else:
                        hout[i][c4d.INSTANCEOBJECT_LINK] = units[17]
        control[c4d.ID_USERDATA,1] += 1
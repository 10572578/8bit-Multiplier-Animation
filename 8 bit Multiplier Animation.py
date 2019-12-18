import c4d
from c4d import documents


def setunit(inlist):
    x = inlist[0]
    y = inlist[1]
    a = inlist[2]
    c = inlist[3]
    return x + 2 * y + 4 * a + 8 * c


def xinput(n):   #����ĳһ��Ԫ�Ĵ���x
    x = 1
    for k in range(0, 8):
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[2 * k]:
            x = 0
            break
    return x


def yinput(n):   #����ĳһ��Ԫ�Ĵ���y
    y = 1
    for k in range(0, 4):
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[4 * k] \
        or instances[n][c4d.INSTANCEOBJECT_LINK] == units[4 * k + 1]:
            y = 0
            break
    return y


def qoutput(n):   #����ĳһ��Ԫ�����q
    q = 1
    for k in [0, 1, 2, 7, 11, 12, 13, 14]:
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[k]:
            q = 0
            break
    return q


def doutput(n):   #����ĳһ��Ԫ�����q
    d = 0
    for k in [7, 11, 12, 13, 14, 15]:
        if instances[n][c4d.INSTANCEOBJECT_LINK] == units[k]:
            d = 1
            break
    return d


def unitinput(i,j,step,xlist,ylist):
    #c
    if i <> 0:   #�������λ
        c = doutput(n - 1)
    else:   #�����λ
        c = 0
    
    #a
    if j == 0:   #�ǵ�һ��
        a = 0
    else:
        if i <> 7:   #���ǵ�һ���Ҳ������λ
            a = qoutput(n - 7)
        if i == 7:   #���ǵ�һ�е������λ
            a = doutput(n - 8)
    
    #x
    if j <> 0:   #���ǵ�һ��
        x = xinput(n - 8)   #������浥Ԫ�Ĵ���x
    else:   #�ǵ�һ��
        if i == step:   #�������ڵ�ǰxλ��
            x = int(xlist[step])
        else:
            x = xinput(n)
    
    #y
    if step >= 7 - i + j:   #����y����һ�ε���
        if i <> 7:   #�������λ
            y = yinput(n + 1)   #�����ߵ�Ԫ�Ĵ���y
        else:   #�����λ
            if j == step:   #�������ڵ�ǰyλ��
                y = int(ylist[step])
            else:
                y = yinput(n)
    else:   #Զ����y����ԭ״
        y = yinput(n)
    
    return [x,y,a,c]


def main():
    control = doc.GetActiveObject()
    if control[c4d.ID_USERDATA,3]:   #�ű�Ϊ����״̬
        controlchild = control.GetChildren()   #��ȡ�˶����Ӽ��б�
        global n, units, instances, xin, yin, lout, hout
        units = controlchild[0].GetChildren()   #��ȡԪ���б�
        instances = controlchild[1].GetChildren()   #��ȡʵ���б�
        xin = controlchild[2].GetChildren()   #��ȡx�����б�
        yin = controlchild[3].GetChildren()   #��ȡy�����б�
        lout = controlchild[4].GetChildren()   #��ȡ������б�
        hout = controlchild[5].GetChildren()   #��ȡ������б�
        xlist = control[c4d.ID_USERDATA,21][::-1]   #����X����
        ylist = control[c4d.ID_USERDATA,22][::-1]   #����Y����
        step = control[c4d.ID_USERDATA,1]   #����
        for j in range(7, -1, -1):   #ÿ��
            if ylist[j] == '0':   #����y�������
                yin[j][c4d.INSTANCEOBJECT_LINK] = units[16]
            else:
                yin[j][c4d.INSTANCEOBJECT_LINK] = units[17]
            for i in range(7, -1, -1):   #ÿ��
                if xlist[i] == '0':   #����x�������
                    xin[i][c4d.INSTANCEOBJECT_LINK] = units[16]
                else:
                    xin[i][c4d.INSTANCEOBJECT_LINK] = units[17]
                n = j * 8 + i   #��ά����תһά
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
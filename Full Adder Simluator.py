import c4d
#Welcome to the world of Python


def process(thisobj):
    nextobj = thisobj[c4d.ID_USERDATA,1]   #输出的物体
    nextotherobj = thisobj[c4d.ID_USERDATA,2]   #输出的另一个物体
    nextmats = doc.GetMaterials()   #获取材质列表
    if nextobj[c4d.ID_USERDATA,5] == 1:   #输出物体类型是导线
        nextobj[c4d.ID_USERDATA,3] = thisobj[c4d.ID_USERDATA,3]   #设置激活状态
        nextobj[c4d.ID_USERDATA,4] = nextmats[thisobj[c4d.ID_USERDATA,3]]   #设置材质激活状态
    if nextotherobj <> None:   #如果另一个输出不是空
        nextotherobj[c4d.ID_USERDATA,3] = thisobj[c4d.ID_USERDATA,3]   #设置激活状态
        nextotherobj[c4d.ID_USERDATA,4] = nextmats[thisobj[c4d.ID_USERDATA,3]]   #设置材质激活状态
    if nextobj[c4d.ID_USERDATA,5] == 3:   #输出物体类型是或门
        nextin1 = nextobj[c4d.ID_USERDATA,6]   #获取或门的输入1
        nextin2 = nextobj[c4d.ID_USERDATA,7]   #获取或门的输入2
        if nextin1[c4d.ID_USERDATA,3] == 1  or nextin2[c4d.ID_USERDATA,3] == 1:
            nextobj[c4d.ID_USERDATA,3] = 1   #设为已激活
            nextobj[c4d.ID_USERDATA,4] = nextmats[1]  #设置材质为已激活导线
        else:
            nextobj[c4d.ID_USERDATA,3] = 0   #设为未激活
            nextobj[c4d.ID_USERDATA,4] = nextmats[0]   #设置材质为未激活导线
    if nextobj[c4d.ID_USERDATA,5] == 2:   #输出物体类型是非门
        if thisobj[c4d.ID_USERDATA,3] == 0:
            nextobj[c4d.ID_USERDATA,3] = 1   #设为已激活
            nextobj[c4d.ID_USERDATA,4] = nextmats[1]  #设置材质为已激活导线
        else:
            nextobj[c4d.ID_USERDATA,3] = 0   #设为未激活
            nextobj[c4d.ID_USERDATA,4] = nextmats[0]   #设置材质为未激活导线
    output = [nextobj, nextotherobj]
    return output


def main():
    control = doc.GetActiveObject()
    branchnodes = []   #分叉节点预留列表
    numpowers = control[c4d.ID_USERDATA,1].GetObjectCount()   #得到全部电源数量
    numactpowers = control[c4d.ID_USERDATA,3].GetObjectCount()   #得到将要激活的电源数量
    for i in range(0, numpowers):   #按照电源数量循环
        thisobj = control[c4d.ID_USERDATA,1].ObjectFromIndex(doc,i)   #选定全部电源中的一个
        thisobj[c4d.ID_USERDATA,3] = 0   #默认为0
        thisobj[c4d.ID_USERDATA,4] = doc.GetMaterials()[0]
        for j in range(0,numactpowers):   #在将要激活的电源列表里寻找
            if control[c4d.ID_USERDATA,3].ObjectFromIndex(doc,j) == thisobj and control[c4d.ID_USERDATA,2] == 1:
                thisobj[c4d.ID_USERDATA,3] = 1   #如果激活已启用，就把将要激活的电源激活
                thisobj[c4d.ID_USERDATA,4] = doc.GetMaterials()[1]
                break
        j = 0
        while True:   #遍历分叉节点
            j = j + 1
            k = 0
            while True:   #遍历单独的线
                k = k + 1
                if thisobj[c4d.ID_USERDATA,1] == None and thisobj[c4d.ID_USERDATA,2] == None or k > 1000:
                    break   #如果是线的末端，就结束单线遍历
                processout = process(thisobj)   #得到两个输出
                thisobj = processout[0]   #主输出
                if processout[1] <> None and branchnodes == [] or processout[1] <> None and processout[1] <> branchnodes[len(branchnodes)-1]:   #如果有另一个输出，就记录在预留列表中
                    branchnodes.append(processout[1])
            print len(branchnodes)
            if branchnodes == [] or j > 1000:   #如果预留列表为空，就退出分叉节点遍历
                break
            else:
                thisobj = branchnodes[len(branchnodes)-1]   #如果有内容，就将物体设为最后一个节点
                print thisobj
                del branchnodes[len(branchnodes)-1]   #删除列表最后一项
    c4d.EventAdd()
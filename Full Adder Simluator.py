import c4d
#Welcome to the world of Python


def process(thisobj):
    nextobj = thisobj[c4d.ID_USERDATA,1]   #���������
    nextotherobj = thisobj[c4d.ID_USERDATA,2]   #�������һ������
    nextmats = doc.GetMaterials()   #��ȡ�����б�
    if nextobj[c4d.ID_USERDATA,5] == 1:   #������������ǵ���
        nextobj[c4d.ID_USERDATA,3] = thisobj[c4d.ID_USERDATA,3]   #���ü���״̬
        nextobj[c4d.ID_USERDATA,4] = nextmats[thisobj[c4d.ID_USERDATA,3]]   #���ò��ʼ���״̬
    if nextotherobj <> None:   #�����һ��������ǿ�
        nextotherobj[c4d.ID_USERDATA,3] = thisobj[c4d.ID_USERDATA,3]   #���ü���״̬
        nextotherobj[c4d.ID_USERDATA,4] = nextmats[thisobj[c4d.ID_USERDATA,3]]   #���ò��ʼ���״̬
    if nextobj[c4d.ID_USERDATA,5] == 3:   #������������ǻ���
        nextin1 = nextobj[c4d.ID_USERDATA,6]   #��ȡ���ŵ�����1
        nextin2 = nextobj[c4d.ID_USERDATA,7]   #��ȡ���ŵ�����2
        if nextin1[c4d.ID_USERDATA,3] == 1  or nextin2[c4d.ID_USERDATA,3] == 1:
            nextobj[c4d.ID_USERDATA,3] = 1   #��Ϊ�Ѽ���
            nextobj[c4d.ID_USERDATA,4] = nextmats[1]  #���ò���Ϊ�Ѽ����
        else:
            nextobj[c4d.ID_USERDATA,3] = 0   #��Ϊδ����
            nextobj[c4d.ID_USERDATA,4] = nextmats[0]   #���ò���Ϊδ�����
    if nextobj[c4d.ID_USERDATA,5] == 2:   #������������Ƿ���
        if thisobj[c4d.ID_USERDATA,3] == 0:
            nextobj[c4d.ID_USERDATA,3] = 1   #��Ϊ�Ѽ���
            nextobj[c4d.ID_USERDATA,4] = nextmats[1]  #���ò���Ϊ�Ѽ����
        else:
            nextobj[c4d.ID_USERDATA,3] = 0   #��Ϊδ����
            nextobj[c4d.ID_USERDATA,4] = nextmats[0]   #���ò���Ϊδ�����
    output = [nextobj, nextotherobj]
    return output


def main():
    control = doc.GetActiveObject()
    branchnodes = []   #�ֲ�ڵ�Ԥ���б�
    numpowers = control[c4d.ID_USERDATA,1].GetObjectCount()   #�õ�ȫ����Դ����
    numactpowers = control[c4d.ID_USERDATA,3].GetObjectCount()   #�õ���Ҫ����ĵ�Դ����
    for i in range(0, numpowers):   #���յ�Դ����ѭ��
        thisobj = control[c4d.ID_USERDATA,1].ObjectFromIndex(doc,i)   #ѡ��ȫ����Դ�е�һ��
        thisobj[c4d.ID_USERDATA,3] = 0   #Ĭ��Ϊ0
        thisobj[c4d.ID_USERDATA,4] = doc.GetMaterials()[0]
        for j in range(0,numactpowers):   #�ڽ�Ҫ����ĵ�Դ�б���Ѱ��
            if control[c4d.ID_USERDATA,3].ObjectFromIndex(doc,j) == thisobj and control[c4d.ID_USERDATA,2] == 1:
                thisobj[c4d.ID_USERDATA,3] = 1   #������������ã��Ͱѽ�Ҫ����ĵ�Դ����
                thisobj[c4d.ID_USERDATA,4] = doc.GetMaterials()[1]
                break
        j = 0
        while True:   #�����ֲ�ڵ�
            j = j + 1
            k = 0
            while True:   #������������
                k = k + 1
                if thisobj[c4d.ID_USERDATA,1] == None and thisobj[c4d.ID_USERDATA,2] == None or k > 1000:
                    break   #������ߵ�ĩ�ˣ��ͽ������߱���
                processout = process(thisobj)   #�õ��������
                thisobj = processout[0]   #�����
                if processout[1] <> None and branchnodes == [] or processout[1] <> None and processout[1] <> branchnodes[len(branchnodes)-1]:   #�������һ��������ͼ�¼��Ԥ���б���
                    branchnodes.append(processout[1])
            print len(branchnodes)
            if branchnodes == [] or j > 1000:   #���Ԥ���б�Ϊ�գ����˳��ֲ�ڵ����
                break
            else:
                thisobj = branchnodes[len(branchnodes)-1]   #��������ݣ��ͽ�������Ϊ���һ���ڵ�
                print thisobj
                del branchnodes[len(branchnodes)-1]   #ɾ���б����һ��
    c4d.EventAdd()
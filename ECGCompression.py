import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import math
from queue import Queue


def encode(q):
    noOfSmpl = 1
    intDiff = []
    endOfEcg = False
    rrOn = True
    rrCount = 0
    ecgSmpl1 = 200 * q.get()
    rrComp1 = 0
    encSB = []
    rrSB = []
    gsm = list(
        r'@£$¥èéùìòÇØøÅå_^{}[~]|€ӔӕßÉ!#¤%&()*+,-./:;<?¡§¿äöñüàÀÁÂÃÄÈÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝÞþáâãçêëíîïðóôõúûýabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    gsm.append("\\")
    intHrv = 0
    while endOfEcg != True and not q.empty():
        intDiff = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 8):
            ecgSmpl2 = 200 * q.get()
            noOfSmpl = noOfSmpl + 1
            diff = ecgSmpl2 - ecgSmpl1
            try:
                if (math.ceil(diff) - diff) > 0.5:
                    intDiff[i] = int(math.floor(diff))  # there was an (int) here
                else:
                    intDiff[i] = int(math.ceil(diff))
            except:
                print(intDiff[i], math.floor(diff))

            ecgSmpl1 = ecgSmpl2

        if q.empty():
            endOfEcg = True

        # intDiff is a list of 8 elements
        signVal = 0

        for i in range(0, 8):
            if intDiff[i] <= -1:
                if i == 0:
                    signVal = signVal + 1
                elif i == 1:
                    signVal = signVal + 2
                elif i == 2:
                    signVal = signVal + 4
                elif i == 3:
                    signVal = signVal + 8
                elif i == 4:
                    signVal = signVal + 16
                elif i == 5:
                    signVal = signVal + 32
                elif i == 6:
                    signVal = signVal + 64
                elif i == 7:
                    encSB.append('')

                intDiff[i] = abs(intDiff[i])

        encSB.append(gsm[signVal])

        # for q = 7
        for i in range(0, 7, 2):
            # compresses two single digits as one
            if (intDiff[i] < 10) and (intDiff[i + 1] < 10):
                join = intDiff[i] * 10 + intDiff[i + 1]
                encSB.append(gsm[join])
            # compresses all values less than 147
            elif (intDiff[i] < 47) and (intDiff[i + 1] < 47):
                encSB.append(gsm[intDiff[i] + 100])
                encSB.append(gsm[intDiff[i + 1] + 100])
            else:
                encSB.append(str(intDiff[i]))
                encSB.append('"')
                encSB.append(str(intDiff[i + 1]))
                encSB.append('"')
                # rr detection proceeding
                if rrOn == True:
                    if (rrComp1 < intDiff[i]) and (intDiff[i] < intDiff[i + 1]):
                        rrComp1 = intDiff[i + 1]
                    else:
                        if rrComp1 < intDiff[i]:
                            rrCount = rrCount - 1
                        rrVal = float(rrCount)
                        rrVal = rrVal / 360
                        rrSB.append(rrVal)
                        rrCount = 0
                        rrOn = False
                        intHrv = intHrv + 1

        # print(q.qsize())
    str_encSB = ''.join(encSB)
    # print(str_encSB)
    # print(len(str_encSB))
    # print()

    return str_encSB


def main():

    f1 = open(r'signal_file', 'r')
    for l1 in f1:
        signals = list(l1.split(","))
        
    f1.close()

    signals = list(map(float, signals))
    np_sig = np.array(signals)
    
    np_sig[:] *= 200
    Diff_normalized_ECG = -np.diff(np_sig[:])
    DN_ECG_without_sign = np.absolute(Diff_normalized_ECG)

    result_list = []
    i = 0
    while(i < len(DN_ECG_without_sign)-100):
        mean_check = np.mean(DN_ECG_without_sign[i:(i+100)])
        mean = np.mean(DN_ECG_without_sign[i:(i+100)])
        num = 0

        for j in range(i, i+100):
            if DN_ECG_without_sign[j] > mean:
                mean = DN_ECG_without_sign[j]
                num = j
                
        if DN_ECG_without_sign[num] > mean_check+80:            
            i = num+50            
        else:        
            i = i + 100           
            
        result_list.append(num)

    class_list = []
    for i in result_list:
        max = 0
        for j in range(i-50, i+50):
            if DN_ECG_without_sign[j] > max:
                max = DN_ECG_without_sign[j]
        if max > 80:
            class_list.append(1)
        else:
            class_list.append(0)


    str_segments = []
    q = Queue()

    for i in result_list:
        for iter in range(i-48, i+49):
            q.put(signals[iter])

        str_segments.append(encode(q))
        q.queue.clear()


    #counting each value in a segment

    range_list = [0,50,100,150,200, 250,300,350,400,450]
    segment_count = []
    alpha_count = {}

    key_set = set()

    for segment in str_segments:
        i = 0
        while i < len(segment):            

            if segment[i].isdigit() :
                
                s = ''
                while(segment[i] != '"'):
                    s = s + segment[i]
                    i = i + 1


                for g in range(len(range_list)):
                    if int(s) <= range_list[g]:
                        t = "Num"+str(g)
                        break

                key_set.add(t)   

                if t not in alpha_count.keys():
                    alpha_count[t] = 1
                else:
                    alpha_count[t] = alpha_count[t] + 1                       


            else:
                s = segment[i]            

                key_set.add(s)                

                if s not in alpha_count.keys():
                    alpha_count[s] = 1
                else:
                    alpha_count[s] = alpha_count[s] + 1

            i = i+1

        segment_count.append(alpha_count)

        alpha_count = {}

    key_list = list(key_set)
    key_list.sort()

    f1 = open(r'output.txt', 'w')
    f2 = open(r'output_class.txt', 'w')

    h = 0
    for item in segment_count:
        output = str(class_list[h]) + ","
        for val in key_list:
            if val in item.keys():
                output = output + str(item[val])+","
            else:
                output = output + "0,"
        

        output = output[0:len(output)-1]+'\n'
        f1.write(output)
        f2.write(str(class_list[h]) + ",")

        if(h == (len(segment_count))//3):
            f1.close();
            f1 = open(r'output_testing.txt', 'w')   
            f2.close()
            f2 = open(r'output_class_testing.txt', 'w')


        if(h == (len(segment_count)*2)//3):
            f1.close();
            f1 = open(r'output.txt', 'a')   
            f2.close()
            f2 = open(r'output_class.txt', 'a')


        h = h + 1

    f1.close()
    f2.close()

main()

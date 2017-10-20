
import numpy as np

def reset_isdispersing(indiv_isdispersing, indiv_whichpatchid, indiv_habarea, indiv_islive, indiv_isdispersingRESET, spatialresolution, homerangesize):
    '''
    This function... preciso descrever essa funcao.
    COMPLETE!
    '''
    
    isdispersing_aux=[]
    isdispersingRESET_aux=[]
    
    
    for i in range(len(indiv_isdispersing)):
        isdispersing_aux.append(indiv_isdispersing[i])
        isdispersingRESET_aux.append(indiv_isdispersingRESET[i])
    
    #patchidLIST=[]
    #for indiv in range(len(indiv_whichpatchid)):
        #if indiv_whichpatchid[indiv] in patchidLIST:
            #pass
        #else:
            #if indiv_islive[indiv]==1:
                #patchidLIST.append(indiv_whichpatchid[indiv])
    patchidLIST = np.unique(indiv_whichpatchid)

    patchid_numHR=[]
    for seq_patchid in range(len(patchidLIST)):
        if patchidLIST[seq_patchid]==0L:
            numHR=999999
        else:
            for indiv in range(len(indiv_whichpatchid)):
                if patchidLIST[seq_patchid]==indiv_whichpatchid[indiv]:
                    areaha = indiv_habarea[indiv]
                    numHR = int(areaha/homerangesize)+1
        patchid_numHR.append(numHR)

    stopToDisperseList=[]    
    for seq_patchid in range(len(patchidLIST)):
        if patchidLIST[seq_patchid]==0L:
            numHR=999999
            stopToDisperseOnThisPatch=0
        else:
            stopToDisperseOnThisPatch=0
            NumbIndivsIsliveNotDispersingOnThisPatch=0
            for indiv in range(len(indiv_whichpatchid)):
                if patchidLIST[seq_patchid]==indiv_whichpatchid[indiv]:
                    if indiv_islive[indiv]==1:
                        if isdispersing_aux[indiv]==0:
                            NumbIndivsIsliveNotDispersingOnThisPatch+=1
            if NumbIndivsIsliveNotDispersingOnThisPatch < patchid_numHR[seq_patchid]:
                stopToDisperseOnThisPatch=patchid_numHR[seq_patchid] - NumbIndivsIsliveNotDispersingOnThisPatch
        stopToDisperseList.append(stopToDisperseOnThisPatch)

    for seq_patchid in range(len(patchidLIST)):
        if patchidLIST[seq_patchid]==0L:
            numHR=999999
        else:
            NumIsDispersingResetedOnthispatch=0
            for indiv in range(len(indiv_whichpatchid)):
                if patchidLIST[seq_patchid]==indiv_whichpatchid[indiv]:
                    if indiv_islive[indiv]==1:
                        if isdispersing_aux[indiv]==1:
                            if stopToDisperseList[seq_patchid]>NumIsDispersingResetedOnthispatch:
                                NumIsDispersingResetedOnthispatch+=1
                                isdispersing_aux[indiv]=0
                                isdispersingRESET_aux[indiv]=1

    return isdispersing_aux, isdispersingRESET_aux

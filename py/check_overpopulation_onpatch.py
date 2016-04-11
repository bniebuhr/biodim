
def check_overpopulation_onpatch(indiv_isdispersing, indiv_whichpatchid, indiv_habarea, indiv_age, homerangesize):
    """
    This function checks, in each patch, how many individuals there are; this number is compared with
    the maximum number of individuals the patch supports, based on their minimum homerange; if there the number
    of individuals is greater than the carrying capacity, some of them are chosen to disperse.
    Input: 
    - indiv_isdispersing: list indentifying which animal is dispersing (1) or not dispersing (0)
    - indiv_whichpatchid: list indentifying the patch id of the patch each animal is in (=0 when dispersing)
    - indiv_habarea: list identifying the area of the patch the animal is in (=0 when dispersing)
    - indiv_age: not used, but may be useful!!!
    - homerangesize: minimum size of an agent homerange, in hectares
    Output:
    - isdispersing_aux: new list indentifying which animal is dispersing (1) or not dispersing (0)
    """    
    
    #### what happens with id = 0 (when animals are dispersing, outside patches??)
    
    isdispersing_aux=[]    
    for i in range(len(indiv_isdispersing)):
        isdispersing_aux.append(indiv_isdispersing[i])
        
    patchidSET={}
    for i in indiv_whichpatchid:
        try: patchidSET[i] += 1
        except KeyError: patchidSET[i] = 1
    
    keys = patchidSET.keys()
    keys.sort()
    
    patchid_overpopLIST=[]
    for k in keys:
        patchid=k
        numind=patchidSET[k]
        for LL in range(len(indiv_habarea)):
            if indiv_whichpatchid[LL]==patchid and patchid>0L:
                areaha = indiv_habarea[LL]
                numHR = int(areaha/homerangesize)+1
                if numHR < numind:
                    overpop = numind-numHR
                    patchid_overpopLIST.append([patchid, overpop])
                else:
                    overpop = 0
                    
    needdisperseLIST=[]
    for m in range(len(patchid_overpopLIST)):
        patchid=patchid_overpopLIST[m][0]
        overpop=patchid_overpopLIST[m][1]

        #check how many isdispersing on the patch
        dispersing=0
        for n in range(len(indiv_whichpatchid)):
            ###if indiv_whichpatchid[n]==patchid and indiv_isdispersing[n]==1:
            if indiv_whichpatchid[n]==patchid and isdispersing_aux[n]==1:
                dispersing+=1
        needdisperse=overpop-dispersing
        if needdisperse>0:
            needdisperseLIST.append([patchid, overpop, dispersing, needdisperse])
    
    # here we may include age - cubs are more prone to disperse!
    ###############
    # this code bias individuals with low index to disperse!!!!!!!!!!!!!!!!!!!
    for o in range(len(needdisperseLIST)):
        patchid=needdisperseLIST[o][0]
        overpop=needdisperseLIST[o][1]
        dispersing=needdisperseLIST[o][2]
        needdisperse=needdisperseLIST[o][3]
        
        newdisperser=0        
        for p in range(len(indiv_whichpatchid)):
            if indiv_whichpatchid[p]==patchid:
                #if indiv_isdispersing[p]==0:
                if isdispersing_aux[p]==0:
                    if needdisperse > newdisperser:
                        isdispersing_aux[p]=1
                        newdisperser+=1

    #return indiv_isdispersing
    return isdispersing_aux
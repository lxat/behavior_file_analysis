"""
Code to read through Dropbox/Share/DMS training, find files of listed subjects, fix files as necessary,
and plot training data
~Alexei

How to use:
Only have to change lines in code parameters

Decide subjects you want to look at, what directories to use, what day to start looking from, and whether you want
to make plots, and save plots or data

Change plot parameters in function 'overallPlot'
"""

import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# CODE PARAMETERS:

subjects = ['D347','D348','D346','H181','H183','H185','H187','H188','H189','H190']
makePlot = True
savePlot = False
saveData = False

saveDir = r'C:\Users\Julia\Dropbox\Share\Alexei\Projects\training'
dataDir = r'C:\Users\Julia\Dropbox\Share\DMS training'
os.chdir(dataDir)
folders = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)] # get only folders

# start_day = '2019.06.17'
# start_day = '2019.01.28' # beginning of year start date
start_day = '2019.07.22'
start_day_ind = [i for i, s in enumerate(folders) if start_day in s][0]
folders = folders[start_day_ind:]
num_folders = len(folders)

col_to_use = list(range(0,25)) # for python txt files

def get_session_type(ttype,session_type):

    # trial types are:
    # 0->9 = AA->FA respectively
    ttype = pd.to_numeric(ttype)
    types = np.unique(ttype)
    types = pd.to_numeric(types)
    AA = []
    AB = []
    BB = []
    BA = []
    if 0 in types:
        AA = np.argwhere(ttype==types[0]) #if this makes an error, do pd.tonumeric on ttype
    if 1 in types:
        AB = np.argwhere(ttype == types[1])
    if 2 in types:
        BB = np.argwhere(ttype == types[2])
    if 3 in types:
        BA = np.argwhere(ttype == types[3])
    # Not sure how to track ITS, if making figures for current week, it doesn't know when the start day is. It could
    # be coded to look at previous day to see if there's data, then if there is ignore ITS, but that's a lotta work...

    # if session_type == 'start' or session_type == 'ITS':
    #     if 2 and 3 in types:
    #         session_type = 'ITS'
    #     else:
    #         session_type = '2types'
    #     if 4 and 5 in types:
    #         session_type = '2types'
    #
    # if session_type == '2types':
    #     if 2 and 3 in types:
    #         session_type = 'ABAB'
    #     elif 6 and 7 in types:
    #         session_type = 'CDAB'

    # if session_type == 'start':
    if 0 in types and 1 in types and 2 not in types:
        session_type = '2T'
    elif 4 in types and 5 in types and 6 not in types:
        session_type = '2T'
    elif 8 in types and 9 in types and 10 not in types:
        session_type = '2T'
    elif 3 in types and 4 not in types and 8 not in types:
        session_type = 'ABAB'
    elif 3 not in types and 4 in types and 8 not in types:
        session_type = 'CDAB'
    elif 3 not in types and 4 not in types and 8 in types:
        session_type = 'EFAB'
    elif 3 in types and 4 in types and 8 not in types:
        session_type = '8T'
    elif 3 in types and 4 not in types and 8 in types:
        session_type = '8T'
    elif 3 not in types and 4 in types and 8 in types:
        session_type = '8T'
    elif 3 in types and 4 in types and 8 in types:
        session_type = '12T'

    # Possible problems with method:
    # When running EFAB, sometimes user forgets to change trial structure until after hitting run, which means
    # a few ABCD trial types are ran when they aren't supposed to
    if session_type == 'ABAB' or session_type == 'CDAB' or session_type == '8T':
        if len(AA)+len(AB)+len(BB)+len(BA) < 8:
            session_type = 'EFAB'



    # if session_type == 'ABAB' or session_type == 'CDAB' or session_type == 'EFAB':
    #     if 3 in types and 4 in types and 8 not in types:
    #         session_type = '8T'
    #     elif 3 in types and 4 not in types and 8 in types:
    #         session_type = '8T'
    #     elif 3 not in types and 4 in types and 8 in types:
    #         session_type = '8T'
    #     elif 3 in types and 4 in types and 8 in types:
    #         session_type = '12T'
    #
    # if session_type == '8T' or session_type == '12T':
    #     if 3 in types and 4 not in types and 8 not in types:
    #         session_type = 'ABAB'
    #     elif 3 not in types and 4 in types and 8 not in types:
    #         session_type = 'CDAB'
    #     elif 3 not in types and 4 not in types and 8 in types:
    #         session_type = 'EFAB'
    #     elif 3 in types and 4 in types and 8 not in types:
    #         session_type = '8T'
    #     elif 3 in types and 4 not in types and 8 in types:
    #         session_type = '8T'
    #     elif 3 not in types and 4 in types and 8 in types:
    #         session_type = '8T'
    #     elif 3 in types and 4 in types and 8 in types:
    #         session_type = '12T'

    # For random designation - mostly works, but not perfect. This is a stupid way to do it..
    # if session_type == 'FA' or session_type == '2types_to_FA' or session_type == 'FR':
    #     testInd = [round(len(AA)/3),round(len(AA)/3)*2] # take two AA's far enough apart
    #     rand = 0
    #     for t in range(len(testInd)):
    #         testList = ttype[AA[testInd[t]][0]:]
    #         abExist = 0
    #         for i in range(len(testList)):
    #             order = False
    #             if i == 0:
    #                 continue
    #             else:
    #                 if testList[i]==0 or testList[i]==1:
    #                     abExist = testList[i]
    #                     order = True
    #                 if not order and abExist==0: # if there's no order and AB trial happened after AA
    #                     order = False
    #                     rand+= 1
    #             break
    #         if not order and rand == 2:
    #             session_type = 'FR'
    #         elif not order and rand == 1:
    #             session_type = 'FA-FR'

    return session_type

def is_txt_good(curData,useEvent):
    "restarting training program adds a new date and time into txt file. Check if anything isn't roundable."
    txt_good = True
    trialno = curData['trial_no.']
    if useEvent:
        if len(np.argwhere(trialno==0)) > 1:
            txt_good = False
    else:
        try:
            round(trialno)
        except:
            txt_good = False
    return txt_good

def fix_bad_txt(curData,useEvent):
    # When session is restarted, new data is continued in the same text file. In labview files, it puts the ID and date
    # in the first columns which changes everything to a str instead of int.
    # This code is written like shit I think - scrap it all if necessary

    trialno = curData['trial_no.']
    nums=[]
    if useEvent:
        trial_ind = 0
        start_ind = np.argwhere(trialno==0)
        start_ind = np.append(start_ind,len(curData))
        for i in range(len(start_ind)):
            try:
                t = start_ind[i+1] - start_ind[i]
                if t > trial_ind:
                    trial_ind = t
                    if start_ind[i] == 0: # -1 to remove first trial of bad section, -4 to remove that and three header rows
                        good_ind = np.array([start_ind[i], start_ind[i+1]-4])
                    else:
                        good_ind = np.array([start_ind[i],start_ind[i+1]-1])
            except:
                t = start_ind[i] - start_ind[i-1]
                if t > trial_ind:
                    if start_ind[i-1] == 0:
                        good_ind = np.array([start_ind[i - 1], start_ind[i] - 1])
                    else:
                        good_ind = np.array([start_ind[i-1],start_ind[i]-1])
        return good_ind
    else:
        for i in trialno:
            try:
                x = float(i)
                nums.append(x)
            except:
                nums.append(np.nan)
                continue
        nums = np.asarray(nums)
        start_ind = np.argwhere(nums==1)
        trial_ind = 0
        for i in range(len(start_ind)):
            try:
                t = int(start_ind[i+1]) - int(start_ind[i])
                if t > trial_ind:
                    trial_ind = t
                    if int(start_ind[i]) == 0: # -1 to remove first trial of bad section, -4 to remove that and three header rows
                        good_ind = np.array([int(start_ind[i]), int(start_ind[i + 1]) - 4])
                    else:
                        good_ind = np.array([int(start_ind[i]),int(start_ind[i+1]) - 1])
            except:
                last_ind = len(nums)-1
                t = last_ind - int(start_ind[i])
                if t > trial_ind:
                    trial_ind = t
                    good_ind = np.array([int(start_ind[i]), last_ind])
    return good_ind

def is_txt_size_good(curData):
    txt_size_good = True
    if len(curData) <= 50:
        txt_size_good = False
    return txt_size_good

def overallPlot(subjects, df, savePlot, saveDir):
    # Plot overall performance for selected dates

    # Plotting defaults
    # Colors: //https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    colors = ['black', 'slategrey', 'lightblue', 'dodgerblue', 'lightseagreen', 'slateblue', 'violet', 'orange']

    # Make dynamic subplot:
    numRows = math.ceil(len(subjects) / 5)
    if len(subjects) < 6:
        numCols = len(subjects)
    else:
        numCols = math.ceil(len(subjects) / 2)

    fig = plt.figure(figsize=(19,10))

    for i in range(len(subjects)):
        curSubj = subjects[i]
        curDates = df['Dates'][df.ID == curSubj].reset_index(drop=True)
        curSType = df['SessionType'][df.ID == curSubj].reset_index(drop=True)
        curPerfs = df['Performances'][df.ID == curSubj].reset_index(drop=True)
        curEl = df['EarlyLicks'][df.ID == curSubj].reset_index(drop=True)
        curMax = df['Max'][df.ID == curSubj].reset_index(drop=True)
        curMin = df['Min'][df.ID == curSubj].reset_index(drop=True)

        # make sure all values are floats in case some str trickery happened...
        curPerfsu = []
        curELu = []
        curMaxu = []
        curMinu = []
        for c in range(len(curPerfs)):
            t = float(curPerfs[c])
            curPerfsu.append(t)
            t = float(curEl[c])
            curELu.append(t)
            t = float(curMax[c])
            curMaxu.append(t)
            t = float(curMin[c])
            curMinu.append(t)

        x = np.array(range(1, len(curPerfs) + 1))

        plt.subplot(numRows, numCols, i + 1)

        for p in range(len(x)):
            sType = curSType[p]
            if sType == 'ITS':
                fillColor = colors[0]
                markertype = 'o'
            elif sType == '2T':
                fillColor = colors[1]
                markertype = 'o'
            elif sType == 'ABAB':
                fillColor = colors[2]
                markertype = 'o'
            elif sType == 'CDAB':
                fillColor = colors[3]
                markertype = 'o'
            elif sType == 'EFAB':
                fillColor = colors[4]
                markertype = 'o'
            elif sType == '8T':
                fillColor = colors[5]
                markertype = 'v'
            elif sType == '12T':
                fillColor = colors[6]
                markertype = 'D'
            plt.plot(x[p], curPerfsu[p], color='dimgray', marker=markertype, markerfacecolor=fillColor,
                     markeredgecolor=fillColor, markersize=8)
            plt.vlines(x[p], curMinu[p], curMaxu[p], color=fillColor)

        plt.hlines(0.8, 1, max(x), color='lightgrey', linestyles='dashed', alpha=0.5)

        plt.plot(x, curELu, color=colors[7], marker='o', markerfacecolor=colors[7],
                 markeredgecolor=colors[7], markersize=4, linestyle='dashed')  # early lick line

        if len(subjects) < 6:
            if i == 0:
                plt.ylabel('Performance')
                plt.xlabel('Day')
        elif len(subjects) > 5 and len(subjects) < 11:
            if i == 5:
                plt.ylabel('Performance')
                plt.xlabel('Day')
        else:
            if i == 10:
                plt.ylabel('Performance')
                plt.xlabel('Day')
        plt.title(curSubj)
        plt.ylim(.05, 1.05)

    # Plot items outside of loop:

    # Legend:
    leg_ITI = mpatches.Patch(color=colors[0], label='ITI')
    leg_2T = mpatches.Patch(color=colors[1], label='2T')
    leg_ABAB = mpatches.Patch(color=colors[2], label='ABAB')
    leg_CDAB = mpatches.Patch(color=colors[3], label='CDAB')
    leg_EFAB = mpatches.Patch(color=colors[4], label='EFAB')
    leg_8T = mpatches.Patch(color=colors[5], label='8T')
    leg_12T = mpatches.Patch(color=colors[6], label='12T')
    leg_EL = mpatches.Patch(color=colors[7], label='Early Lick')
    fig.legend(handles=[leg_ITI, leg_2T, leg_ABAB, leg_CDAB, leg_EFAB, leg_8T, leg_12T, leg_EL], loc='center right')

    # Title
    figureTitle = 'Performances for ' + str(curDates[0]) + ' through ' + str(curDates.iloc[-1])
    plt.suptitle(figureTitle, fontsize=16)

    if savePlot:
        plt.savefig(saveDir + '\\' + figureTitle + '.png', bbox_inches='tight')
        print('plot saved as '+figureTitle)
    else:
        print('plot not saved')
    plt.show()

# MAIN LOOP - ITERATE THROUGH ANIMALS
for id_index in range(len(subjects)):
    cur_ids = []
    cur_dates = []
    cur_type = []
    cur_performances = []
    max_perf = []
    min_perf = []
    cur_el = []
    curID = subjects[id_index]
    session_type = 'ITS'
    eventFid = curID + '_events'
    trainFid = curID + '_training'

    # ITERATE THROUGH FOLDERS
    for date_index in range(num_folders):

        curDate = folders[date_index]

        # obtain list of files in folder iteration
        curDir = dataDir + '\\' + curDate
        os.chdir(curDir)
        files = os.listdir()
        print(curDir)

        # SPECIAL CASES FOR LOOP TO SKIP:
        # No header appears in some python files...very strange. No idea how that happened
        if curID=='D338' and curDate=='2019.04.03':
            print('No header. Skipped '+curID+', '+curDate)
            continue
        elif curID=='D338' and curDate=='2019.05.17':
            print('No header. Skipped ' + curID + ', ' + curDate)
            continue
        elif curID=='D348' and curDate=='2019.05.17':
            print('No header. Skipped ' + curID + ', ' + curDate)
            continue

        # determine if using _events(py) or _training(lv) file
        # issue here is py files were initially named _event, but now are named _training, so needs try statements
        if eventFid not in files and trainFid not in files:
            continue
        else:
            if eventFid in files and trainFid in files:
                # if both files exist, take one with largest
                try:
                    temp_events = pd.read_csv(eventFid, usecols=col_to_use)
                except:
                    temp_events = pd.read_csv(eventFid, sep='\t', header=1, skipfooter=1)
                numTrials_events = len(temp_events)
                temp_training = pd.read_csv(trainFid)
                numTrials_training = len(temp_training)
                if numTrials_events > numTrials_training:
                    curFid = eventFid
                    useEvent = True
                else:
                    curFid = trainFid
                    useEvent = False
            elif eventFid in files:
                curFid = eventFid
                useEvent = True
            elif trainFid in files:
                curFid = trainFid
                useEvent = False

        # DO THINGS IF TXT FILE EXISTS IN FOLDER
        if curFid in files:
            if useEvent:
                try:
                    curData = pd.read_csv(curFid, index_col=False, usecols=col_to_use)
                except ValueError as error: # some labview days were named _event instead of _training.............
                    curData = pd.read_csv(curFid, sep='\t', header=1, skipfooter=1)
                    useEvent = False
            else:
                try:
                    curData = pd.read_csv(curFid, sep='\t', header=1, skipfooter=1)
                except pd.errors.ParserError as error:
                    print(error)
                    print('switched from python to lv, screwing up delimiters. Skipped '+curID+', '+curDate)
                    continue
                try: # files named _training have python delimiters
                    curData.trial_type
                except AttributeError as error:
                    curData = pd.read_csv(curFid, index_col=False, usecols=col_to_use)
            print(curFid)

            # Check if labview program started before python which creates an error
            try:
                pd.to_numeric(curData['trial_no.'])
            except ValueError as error:
                print(error)
                print('switched from lv to python, screwing up delimiters. Skipped '+curID+', '+curDate)
                continue

            # CHECK IF FILE WAS RESTARTED WITHIN SESSION (screws up index)
            txt_good = is_txt_good(curData,useEvent)
            if not txt_good:
                # good_ind are good indices in current data. Remove all other indices
                good_ind = fix_bad_txt(curData,useEvent)
                curData = curData.iloc[good_ind[0]:good_ind[1]+1,:]

            # CHECK IF FILE IS LARGE ENOUGH
            txt_size_good = is_txt_size_good(curData)
            if not txt_size_good:
                print('txt file is less than 50 trials. Skipped '+curID+', '+curDate)
                continue

            # if curData was sliced at all, indices get messed up. Reset indices to 0
            curData.reset_index(drop=True, inplace=True)
            ttype = np.array(curData.trial_type)

            # get session type
            session_type = get_session_type(ttype, session_type)




            # iterate: if last 2 trials are no choice -> remove
            if session_type != 'ITS':
                miss = pd.to_numeric(curData.miss)
                done = False
                while not done:
                    t = len(curData) - 1
                    if miss[t] == 1 and miss[t - 1] == 1:
                        curData = curData.iloc[0:t - 1, :]
                    else:
                        done = True

            # no more alterations of curData after this point

            numTrials = len(curData)
            # use pd.to_numeric because if txt is bad, dates in middle changes all values to strings
            ttype = pd.to_numeric(curData.trial_type)
            correct = pd.to_numeric(curData.correct)
            error = pd.to_numeric(curData.error)
            switch = pd.to_numeric(curData.switch)
            miss = pd.to_numeric(curData.miss)
            early_lick = pd.to_numeric(curData.early_lick)

            # get correct performance for each trial type for max/min perf
            ttype_perf=[]
            fx = np.array(correct)
            num_ttypes = max(ttype)+1
            for n in range(int(num_ttypes)):
                t = np.argwhere(ttype==n)
                if sum(fx[t]) == 0 or len(fx[t]) == 0:
                    # ttype_perf.append(np.array([0]))
                    continue
                else:
                    ttype_perf.append(sum(fx[t])/len(fx[t]))

            # append data for found file
            cur_ids.append(curID)
            cur_dates.append(curDate)
            cur_type.append(session_type)
            try:
                cur_performances.append((sum(correct))/numTrials)
            except:
                correct = pd.to_numeric(correct)
                cur_performances.append((sum(correct)) / numTrials)
            max_perf.append(max(ttype_perf))
            min_perf.append(min(ttype_perf))
            cur_el.append((sum(early_lick)) / numTrials)


    # min and max are in a list of narray, instead of list of list - convert
    max_perf = np.concatenate(max_perf)
    max_perf = max_perf.tolist()
    min_perf = np.concatenate(min_perf)
    min_perf = min_perf.tolist()

    temp_d = np.vstack((cur_ids,cur_dates,cur_type,cur_performances,max_perf,min_perf,cur_el))

    if id_index == 0:
        cur_d = temp_d
    else:
        cur_d = np.hstack((cur_d,temp_d))

d = {'ID': cur_d[0], 'Dates': cur_d[1], 'SessionType': cur_d[2], 'Performances': cur_d[3], 'Max': cur_d[4],
     'Min': cur_d[5], 'EarlyLicks': cur_d[6]}

df = pd.DataFrame(d)

if saveData:
    os.chdir(saveDir)
    fid = 'training_data_'+start_day+'_-_'+curDate
    df.to_csv(fid, index=False)
    print('dataframe saved as '+fid)
else:
    print('dataframe not saved')

if makePlot:
    fig = overallPlot(subjects,df,savePlot,saveDir)

print('All done')


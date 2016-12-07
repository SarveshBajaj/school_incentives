"""
Filename: matchfuncs.py
Author: Yoshiasa Ogawa
LastModified: 29/10/2015
Functions for matching algorithms.
"""
from __future__ import division
import numpy as np
import itertools
# import gambit
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from matching import *
def BOS(prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None, interview=None):
    """
    Boston School Algorithm
    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants
    Returns
    ---
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_indptr : ndarray(int, ndim=1)
        Index Pointer for proposers
    resp_indptr : ndarray(int, ndim=1)
        Index Pointer for respondants
    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_matched = np.zeros(sum(prop_caps), dtype=int) + prop_unmatched
    resp_matched = np.zeros(sum(resp_caps), dtype=int) + resp_unmatched
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    propcaps_rest = [i for i in prop_caps]
    respcaps_rest = [i for i in resp_caps]
    prop_single = range(prop_num)
    prop_prefsptr = [0 for i in range(prop_num)]
    prop_counter = [0 for i in range(prop_num)]
    if list_length is None:
        l_length = prop_prefs.shape[1]
    else:
        l_length = list_length
    interview_num = 0

    while len(prop_single) >= 1:
        prop_single_copy = [i for i in prop_single]
        approach = np.zeros(resp_num)
        for prop_id in prop_single_copy:
            if prop_counter[prop_id] == l_length:
                prop_single.remove(prop_id)
                continue
            if prop_prefsptr[prop_id] == prop_prefs.shape[1]:
                prop_single.remove(prop_id)
                continue
            resp_id = prop_prefs[prop_id][prop_prefsptr[prop_id]]
            if resp_id == prop_unmatched:
                prop_single.remove(prop_id)
                continue
            while respcaps_rest[resp_id] == 0:
                prop_prefsptr[prop_id] += 1
                if prop_prefsptr[prop_id] == prop_prefs.shape[1]:
                    resp_id = prop_unmatched
                    prop_single.remove(prop_id)
                    break
                resp_id = prop_prefs[prop_id][prop_prefsptr[prop_id]]
                if resp_id == prop_unmatched:
                    prop_single.remove(prop_id)
                    break
            if resp_id != prop_unmatched:
                prop_counter[prop_id] += 1
                prop_prefsptr[prop_id] += 1
                approach[resp_id] += 1
                interview_num += 1
        prop_single_copy = [i for i in prop_single]
        for resp_id in range(resp_num):
            if respcaps_rest[resp_id] >= approach[resp_id]:
                for prop_id in prop_single_copy:
                    if prop_prefs[prop_id][prop_prefsptr[prop_id]-1] == resp_id:
                        propcaps_rest[prop_id] -= 1
                        respcaps_rest[resp_id] -= 1
                        prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                        resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                        if propcaps_rest[prop_id] == 0:
                            prop_single.remove(prop_id)
            elif respcaps_rest[resp_id] != 0:
                applicants = []
                for prop_id in prop_single_copy:
                    if prop_prefs[prop_id][prop_prefsptr[prop_id]-1] == resp_id:
                        applicants.append(prop_id)
                for k in range(resp_prefs.shape[1]):
                    prop_id = resp_prefs[resp_id][k]
                    if prop_id in applicants:
                        propcaps_rest[prop_id] -= 1
                        respcaps_rest[resp_id] -= 1
                        prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                        resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                        if propcaps_rest[prop_id] == 0:
                            prop_single.remove(prop_id)
                    if respcaps_rest[resp_id] == 0:
                        break
    if interview is not None:
        return interview_num
    if switch == 0:
        return prop_matched, resp_matched
    elif switch == 1:
        return prop_matched, resp_matched, resp_indptr
    else:
        return prop_matched, resp_matched, prop_indptr, resp_indptr

def DA(prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None):
    """
    Deffered Acceptance Algorithm
    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
      Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
      Preference of respondants
    prop_caps : list
      Capacity of proposers
    resp_caps : list
      Capacity of respondants
    Returns
    ---
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_indptr : ndarray(int, ndim=1)
        Index Pointer for proposers
    resp_indptr : ndarray(int, ndim=1)
        Index Pointer for respondants
    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_matched = np.zeros(sum(prop_caps), dtype=int) + prop_unmatched
    resp_matched = np.zeros(sum(resp_caps), dtype=int) + resp_unmatched
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    propcaps_rest = [i for i in prop_caps]
    respcaps_rest = [i for i in resp_caps]
    prop_single = range(prop_num)
    prop_counter = [0 for i in range(prop_num)]
    if list_length is None:
        l_length = prop_prefs.shape[1]
    else:
        l_length = list_length

    while len(prop_single) >= 1:
        prop_single_roop = [i for i in prop_single]
        for prop_id in prop_single_roop:
            if prop_counter[prop_id] == l_length:
                prop_single.remove(prop_id)
                break
            resp_id = prop_prefs[prop_id][prop_counter[prop_id]]
            prop_counter[prop_id] += 1
            if resp_id == prop_unmatched:
                prop_single.remove(prop_id)
            elif respcaps_rest[resp_id] >= 1:
                propcaps_rest[prop_id] -= 1
                respcaps_rest[resp_id] -= 1
                prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                if propcaps_rest[prop_id] == 0:
                    prop_single.remove(prop_id)
            else:
                deffered = resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]]
                max_rank = max([resp_ranks[resp_id][i] for i in deffered])
                max_id = resp_prefs[resp_id][max_rank]
                if resp_ranks[resp_id][prop_id] < max_rank:
                    if max_id not in prop_single:
                        prop_single.append(max_id)
                    propcaps_rest[max_id] += 1
                    propcaps_rest[prop_id] -= 1
                    prop_matched[np.where(prop_matched[prop_indptr[max_id]:prop_indptr[max_id+1]] == resp_id)[0][0] + prop_indptr[max_id]] = prop_unmatched
                    prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                    resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == max_id)[0][0] + resp_indptr[resp_id]] = prop_id
                    if propcaps_rest[prop_id] == 0:
                        prop_single.remove(prop_id)

    if switch == 0:
        return prop_matched, resp_matched
    elif switch == 1:
        return prop_matched, resp_matched, resp_indptr
    else:
        return prop_matched, resp_matched, prop_indptr, resp_indptr

def AddBOS(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps=None, prop_caps=None, interview=None):
    """
    Additional BOS Stage after the matching given by any mechanism.
    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants
    Returns
    ---
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_indptr : ndarray(int, ndim=1)
        Index Pointer for proposers
    resp_indptr : ndarray(int, ndim=1)
        Index Pointer for respondants
    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    prop_ranks = np.argsort(prop_prefs)
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    propcaps_rest = [i for i in prop_caps]
    respcaps_rest = [i for i in resp_caps]
    add_prop = []
    add_resp = []
    for prop_id in range(prop_num):
        pairs = prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]
        for pair in pairs:
            if pair != resp_num:
                propcaps_rest[prop_id] -= 1
        if propcaps_rest[prop_id] != 0:
            add_prop.append(prop_id)
    for resp_id in range(resp_num):
        pairs = resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]]
        for pair in pairs:
            if pair != prop_num:
                respcaps_rest[resp_id] -= 1
        if respcaps_rest[resp_id] != 0:
            add_resp.append(resp_id)
    add_prop_prefs = np.argsort(prop_ranks[:, add_resp])
    add_resp_prefs = np.argsort(resp_ranks[:, add_prop])

    if len(add_resp) != 0 and len(add_prop) != 0:
        approach = defaultdict()
        for prop_id in add_prop:
            counter = 0
            resp_id = add_resp[add_prop_prefs[prop_id][counter]]
            while resp_id in prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]:
                counter += 1
                if counter == add_prop_prefs.shape[1]:
                    resp_id = resp_num
                    break
                resp_id = add_resp[add_prop_prefs[prop_id][counter]]
            approach[prop_id] = resp_id

        for resp_id in add_resp:
            applicants = [i for i in add_prop if approach[i] == resp_id]
            if respcaps_rest[resp_id] >= len(applicants):
                for prop_id in applicants:
                    propcaps_rest[prop_id] -= 1
                    respcaps_rest[resp_id] -= 1
                    prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                    resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
            else:
                for k in add_resp_prefs[resp_id]:
                    prop_id = add_prop[k]
                    if prop_id in applicants:
                        propcaps_rest[prop_id] -= 1
                        respcaps_rest[resp_id] -= 1
                        prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                        resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                    if respcaps_rest[resp_id] == 0:
                        break
    if interview is not None:
        return len(add_prop)
    if switch == 0:
        return prop_matched, resp_matched
    elif switch == 1:
        return prop_matched, resp_matched, resp_indptr
    else:
        return prop_matched, resp_matched, prop_indptr, resp_indptr

prop_prefs = [[0,1],[1,0]]
resp_prefs = [[1,0],[0,1]]
resp_caps =[1,1]
prop_caps = [1,1]

res = BOS(prop_prefs,resp_prefs,prop_caps,resp_caps)
print AddBOS(prop_prefs,resp_prefs,res[0],res[1],prop_caps,resp_caps)

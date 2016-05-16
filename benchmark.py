"""Testing the speed of various ways of sampling elements of Python data structures.
"""
import crandom,random,timeit
from matplotlib import pyplot as plt

#Test the speed of sampling a single item from a dictionary.
dict_sizes=[10**x for x in range(1,5)] #test the dictionaries with different numbers of elements to get an idea for the scaling
rounds_for_sizes=[10**6,10**5,10**4,10**3,10**2]
rounds=1000000 #avarege over this many rounds

command_dicts={"default":"random.choice(list(myDict))",
               "ctypes" :"crandom.choice_dict_ctypes(myDict)",
               "cext"   :"crandom.choice_dict_cext(myDict)" }
results_dicts=dict([(method,[]) for method in command_dicts.keys()]) #save results here


#Get the times to sample with the methods
for i,dict_size in enumerate(dict_sizes):
    for method,cmd in command_dicts.items():
        if method=="default":
            nrounds=rounds_for_sizes[i]
        else:
            nrounds=rounds

        timer=timeit.Timer(setup="import random,crandom;myDict=dict(((random.random(),None) for i in xrange(%u)))"%dict_size,stmt=cmd)
        results_dicts[method].append(timer.timeit(number=nrounds)/nrounds)

#Plot the results for dicts
fig,ax=plt.subplots()
for method,results in results_dicts.items():
    ax.loglog(dict_sizes,map(lambda x:x*10**6,results),label=command_dicts[method])
ax.set_xlabel("Number of elements in the dict")
ax.set_ylabel("Time (micro seconds)")
l=ax.legend(loc="upper left")

#Remove some chart junk
l.draw_frame(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

fig.savefig("benchmark.png")


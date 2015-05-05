'''
EL6383 Final Project
Shiyi Li
N11459158
'''
#Import the Data
f = open('C:/Users/Administrator/Desktop/6383/dec-pkt-1.tcp', 'r')
timestamp = []
srchost = []
dsthost = []
srcport = []
dstprot = []
payload = []

for line in f:
    lines = line.split()
    timestamp.append(float(lines[0]))
    srchost.append(int(lines[1]))
    dsthost.append(int(lines[2]))
    srcport.append(int(lines[3]))
    dstprot.append(int(lines[4]))
    payload.append(int(lines[5]))
f.close()

#Task 1: Traffic Characteristics
#(A)What is the average bit rate for the entire duration?
#Please note that both the Ethernet header, IP packet header and payload have to be counted.)
Total_bytes = sum(payload) + 58*len(payload)
#18 bytes Ethernet header, 20 bytes IP header and 20 bytes TCP header
Duration = timestamp[-1] - timestamp[0];
Bitrate_ave = Total_bytes / Duration / 1024; #bit rate in kilobytes/second
print ('The average bit rate is :',Bitrate_ave)


#(B)Find the average bit rate for each 5-minute window, please add more
#rows to complete the following table.
win,win_bytes,win_size,win_time = [],[],[],[]
win = ([1]*14)         # stores the begin point of each 300sec time window.
win_bytes = ([0]*13)  # stores the number of bits in each 300sec window.
win_size = ([0]*13)    # stores the number of packets in each 300sec window.
win_time = ([0]*13)    # stores the time duration of each window.

for i in range(0,12):
    for j in range(0,len(timestamp)+1):
        if(timestamp[j+win[i]] >= 300*i):
            win[i+1] = win[i] + j
            break

win[-1] = len(timestamp)+1
for i in range(0,13):
    win_size[i] = win[i+1] - win[i]
    win_bytes[i] =  win_size[i]*58 + sum(  payload[ win[i]:win[i+1] ]  )
    win_time[i] =  timestamp[ win[i+1] -2 ] - timestamp[ win[i] -1 ]
Bitrate_win = []

for i in range(0,13):
    Bitrate_win.append( win_bytes[i] / win_time[i] / 1024 )     #unit: kilobytes/second
print ('The average bit rate for each 5-minute window is :',Bitrate_win)


#(C) Find the distribution of packets based on the payload sizes
count = ([0]*6)              #packet size count
Total_pakt = len(payload)
for i in range( 0 , Total_pakt ):
    if payload[i]<1:
        count[0] += 1
    elif payload[i]>=1 and payload[i]<128: 
        count[1] += 1
    elif payload[i]>=128 and payload[i]<256: 
        count[2] += 1
    elif payload[i]>=256 and payload[i]<384: 
        count[3] += 1
    elif payload[i]>=384 and payload[i]<512: 
        count[4] += 1
    elif payload[i] == 512:
        count[5] += 1
percentage = []
for num in count:
    percentage.append( num / Total_pakt *100 ) #Percentage based on the number of packets
print ('Percentage are:',percentage)

#(D)Sort the source IP addresses according to their traffic volume, list the top 3 source IP addresses and                       
#the corresponding traffic volume and the percentage in the total traffic volume


src_traffic = ([0] * max(srchost))

for i in range( 0, max(srchost) ):
    for j in range( 0, len(srchost) ):
        if srchost[j] == i+1 :
            src_traffic[i] += payload[j] + 58           
                                                                                                                                                                                                                                                                                                                                                                                                                                                      
Top3_src = ([0]*3)
Top3_srctraffic = ([0]*3)
for j in range(0,3):
    for i in range( 0, len(src_traffic) ):
        if src_traffic[i] == max(src_traffic):
            Top3_src[j] = i+1
            Top3_srctraffic[j] = max(src_traffic)
            src_traffic[i] -= 10**10
            break
Top3_srcrate = []
for n in Top3_srctraffic:
    Top3_srcrate.append( n / Total_bytes * 100 )

print ('Top3_src:',Top3_src)
print ('Top3_srctraffic:',Top3_srctraffic)
print ('Top3_srcrate:',Top3_srcrate)

#(E)Sort the destination ports according to their traffic volume, list the top 3 destination ports
#and the corresponding traffic volume and the percentage in the total traffic volume
dst_traffic = ([0] * max(dsthost))

for i in range( 0, max(dsthost) ):
    for j in range( 0, len(dsthost) ):
        if dsthost[j] == i+1 :
            dst_traffic[i] = dst_traffic[i] + payload[j] + 58           
                                                                                                                                                                                                                                                                                                                                                                                                                                                      
Top3_dst = ([0]*3)
Top3_dsttraffic = ([0]*3)
for j in range(0,3):
    for i in range( 0, len(dst_traffic) ):
        if dst_traffic[i] == max(dst_traffic):
            Top3_dst[j] = i+1
            Top3_dsttraffic[j] = max(dst_traffic)
            dst_traffic[i] = dst_traffic[i] - 10**10
            break
Top3_dstrate = []
for n in Top3_dsttraffic:
    Top3_dstrate.append( n / Total_bytes * 100 )

print ('Top3_dst:',Top3_dst)
print ('Top3_dsttraffic:',Top3_dsttraffic)
print ('Top3_dstrate:',Top3_dstrate)


#3.Load Balancing
#(A)
port_traffic = [([0]*4) for i in range(13)]  # Number of bytes through each port.
port_wintime = [([0]*4) for i in range(13)] # Time duration for each window.
max_diff = []                   # The maximum difference among the ports.
path = [0]*len(dsthost)             # The output path for each packet.

for i in range(1,len(dsthost)+1):
    reminder = i%4
    if reminder == 0:
        path[i-1] = 4
    elif reminder == 1:
        path[i-1] = 1
    elif reminder == 2:
        path[i-1] = 2
    elif reminder == 3:
        path[i-1] = 3

for i in range(0,13):    
    for j in range(0,4):
        port_wintime[i][j] = win_time[i]
        for k in range(win[i], win[i+1]):
            if path[k-1] == j+1:
                port_traffic[i][j] += payload[k-1] + 58

Bitrate_port = [([0]*4) for i in range(13)]
for i in range(0,13):
    for j in range(0,4):
        Bitrate_port[i][j] = port_traffic[i][j] / port_wintime[i][j] / 1024  #kilobytes/second
print('Bitrate_port:',Bitrate_port)

maxq = [0]*13
minq = [0]*13
max_diff= [0]*13
for i in range (0,13):
    maxq[i] = Bitrate_port[i][0]
    minq[i] = Bitrate_port[i][0]
    for j in range (1,4):
        if Bitrate_port[i][j] > maxq[i]:
            maxq[i] = Bitrate_port[i][j]
        if Bitrate_port[i][j] < minq[i]:
            minq[i] = Bitrate_port[i][j]
    max_diff[i] =  maxq[i] - minq[i]
        
print ('max_diff:',max_diff)



# (B) Solving out-of-order problem
path_inorder = [0]*len(dsthost) # The output path for each packet.
inorder_traffic = [([0]*4) for i in range(13)]          # No. of bytes through each port.
max_diffinorder = [0]*13          # The maximum difference among the ports.

for i in range( 1,len(dsthost)+1 ):
    reminder = i%4
    if reminder == 0:
        path_inorder[i-1] = 4
    elif reminder == 1:
        path_inorder[i-1] = 1
    elif reminder == 2:
        path_inorder[i-1] = 2
    elif reminder == 3:
        path_inorder[i-1] = 3

for i in range( 1,len(dsthost)+1 ):    
        for j in range(i-1,0,-1):
            if (srchost[i-1] == srchost[j-1]) and (dsthost[i-1] == dsthost[j-1]):
                path_inorder[i-1] = path_inorder[j-1] 
                break

  
for i in range(0,13):
    for j in range(0,4):
        for k in range( win[i],win[i+1] ):
            if path_inorder[k-1] == j+1:
                inorder_traffic[i][j] = inorder_traffic[i][j] + payload[k-1] + 58


Bitrate_inorder = [([0]*4) for i in range(13)]
for i in range(0,13):
    for j in range(0,4):
        Bitrate_inorder[i][j] = inorder_traffic[i][j] / port_wintime[i][j] / 1024  #kilobytes/second
print('Bitrate_inorder:',Bitrate_inorder)



maxqq = [0]*13
minqq = [0]*13
max_diffinorder= [0]*13
for i in range (0,13):
    maxqq[i] = Bitrate_inorder[i][0]
    minqq[i] = Bitrate_inorder[i][0]
    for j in range (1,4):
        if Bitrate_inorder[i][j] > maxqq[i]:
            maxqq[i] = Bitrate_inorder[i][j]
        if Bitrate_inorder[i][j] < minqq[i]:
            minqq[i] = Bitrate_inorder[i][j]
    max_diffinorder[i] =  maxqq[i] - minqq[i]
        
print ('max_diffinorder:',max_diffinorder)


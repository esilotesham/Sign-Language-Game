
import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import pickle
import numpy as np
import random
import datetime
import matplotlib.gridspec as gridspec


database = pickle.load(open('userData/database.p','rb'))
#print database
userName = raw_input('Please enter your name: ')

if userName in database:
	(database[userName])['logins']+=1
	#reset all values to zero since we've already calculated the highscore!
	(database[userName])['0']=0
	(database[userName])['1']=0
	(database[userName])['2']=0
	(database[userName])['3']=0
	(database[userName])['4']=0
	(database[userName])['5']=0
	(database[userName])['6']=0
	(database[userName])['7']=0
	(database[userName])['8']=0
	(database[userName])['9']=0
	print("Welcome back "+userName+".")
	print database
else:
	database[userName] = {'logins':1, '0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'highscore':0}
	print 'welcome ' + userName + '.'

def levelTwo():
	j=0
	for values in range(0,10):
		j+=(database[userName])[str(values)]
	if j>=9:
		return True
	else:
		return False
def levelThree():
	j=0
	for values in range(0,10):
		j+=(database[userName])[str(values)]
	if j>=18:
		return True
	else:
		return False



def points():
	j=0
	k=0
	for values in range(0,10):
		j+=(database[userName])[str(values)] #j is the players current score.
	for elements in database: #get highscores of all users!	
		if elements!='ultimatescore':
			if ((database['ultimatescore'])['score'])<=((database[elements])['highscore']):
				k=((database[elements])['highscore'])
			else:
				k=(database['ultimatescore'])['score']
	return k,j
	
def getNum():
	num = random.randrange(0, 10, 1)
	print"randomly chosen letter"
	print(num)
	if (database[userName])[str(num)]!=0: #gives me a key error when 0 is input...
		#print "ttttoday"
		count=0
		for values in range(0,10,1):
			if(database[userName])[str(num)] == (database[userName])[str(values)]: 
				print("equalTo")
				count+=1
				print(count)
				if count == 10:
					return num
				else:
					print"not yet..."
			elif (database[userName])[str(num)] > (database[userName])[str(values)]:
				print("more of num than one of the numbers")
				return values
			else:
				print("less of num than one of the numbers")
				return num
	else: 
		return num
	
def dictSigns(asl_number):
	if asl_number in database[userName]:
		(database[userName])[asl_number]+=1
	else: 
		database[userName].update({asl_number:1})
		#print(database)
	print('You have signed: '+str((database[userName])[asl_number])+" "+str(asl_number)+'s')
	
	print database[userName]
	pickle.dump(database,open('userData/database.p','wb'))
	
	
pickle.dump(database,open('userData/database.p','wb'))


clf = pickle.load( open('userData/classifier.p','rb') )
testData = np.zeros((1,30),dtype='f')
controller = Leap.Controller()
lines = []
matplotlib.interactive(True)
fig= plt.figure( figsize=(10,8) )
ax = fig.add_subplot(2,1,2, projection='3d')#111, projection='3d' )


ax2 = fig.add_subplot(2, 1, 1, sharex=ax, sharey=ax)
ax2.autoscale(False)
plt.axis('off')

programState = 0
predictedClass = getNum()
num = predictedClass

#find better images:
image_file0 = ('imgs/image0.png')
image0 = plt.imread(image_file0)
image_file1 = ('imgs/centerimg.png')
image1 = plt.imread(image_file1)
image_file2 = ('imgs/centerimg.png')
image2 = plt.imread(image_file2)
image_file4 = ('imgs/img4.png')
image4 = plt.imread(image_file4)
image_file5 = ('imgs/img5.png')
image5 = plt.imread(image_file5)
welcome = ('imgs/WelcomeScreen.png')
welcome2 = plt.imread(welcome)
print "start..."




def isHandCentered(hand_center):
   if ( (50 > hand_center.x > -150) & (450 > hand_center.y > 120) & (120 > hand_center.z > -120) ):
      return True
   else:
      return False

def CenterData(testData):
   #get mean of X coords
   allXCoords = testData[0,::3] #[:,:,0,:]
   XmeanValue = allXCoords.mean()
   testData[0,::3] = allXCoords - XmeanValue
   #print testData[:,:,0,:].mean()
   #get mean of Y coords
   allYCoords = testData[0,1::3] #[:,:,1,:]
   YmeanValue = allYCoords.mean()
   testData[0,1::3] = allYCoords - YmeanValue
   #print testData[:,:,1,:].mean()
   #get mean of Z coords
   allZCoords = testData[0,2::3] #[:,:,2,:]
   ZmeanValue = allZCoords.mean()
   testData[0,2::3] = allZCoords - ZmeanValue
   #print testData[:,:,2,:].mean()
   return testData
   
#mirrors the hand to be a right hand, if it's a left hand
#doesnt always work...
def scale_transformation(hand):
   basis = hand.basis
   x_basis = (basis.x_basis * -1)
   y_basis = (basis.y_basis * -1)
   z_basis = (basis.z_basis * -1)
   return hand
go=False #============================================@@@@@@@@@@@@@@@@@@@@@@@@@@@@ make go = FALSE when you want to show welcome screen ==================...
count=0
while(go==False):
	frame = controller.frame()
	plt.clf()
	gs1 = gridspec.GridSpec(1, 1)
	ax1 = fig.add_subplot(gs1[0])
	ax1.imshow(plt.imread('imgs/WelcomeScreen.png'))
	ax1.axis('off')
	plt.show()
	plt.draw()
	#wait a second
	time.sleep(2)
	count +=1
	if count==3:
		print count
		go=True
   
while ( go==True ):
#    frame = controller.frame()
   while (programState == 0): #no hand
      #print programState
      #print('__')
      frame = controller.frame()
      plt.clf()
      gs1 = gridspec.GridSpec(2, 1)
      ax1 = fig.add_subplot(gs1[1])
      ax1.imshow(plt.imread('imgs/nohand.png'))
      #ax1.patch.set_facecolor('red')
      ax2 = fig.add_subplot(gs1[0])
      ax2.imshow(plt.imread('imgs/state0.png'))
      ax1.axis('off')
      ax2.axis('off')
      plt.show()
      plt.draw()
      if((frame.hands.is_empty) == False):
         programState = 1
         plt.clf()
      
         
   while (programState == 1):  #if hand is over Leap but not centered
      frame = controller.frame()
      #print programState
      hand = frame.hands[0]
      hand_center = hand.palm_position
      plt.clf()
      
      gs2 = gridspec.GridSpec(3, 1)
      ax = fig.add_subplot(gs2[2], projection='3d')
      ax.set_xlim(0,300)
      ax.set_ylim(0,300)
      ax.set_zlim(0,200)
      ax.view_init(azim=90)
      ax.axis('off') # clear x- and y-axes
      
      
      ax2 = fig.add_subplot(gs2[1])
      ax2.imshow(image2)
      ax2.autoscale(False)
      ax2.axis('off')
      
      center = ('imgs/center.png')
      center1 = plt.imread(center)
      ax3 = fig.add_subplot(gs2[0])
      ax3.imshow(center1)
      ax3.autoscale(False)
      ax3.axis('off')
      k=0
      for i in range(0,5): #for all fingers in hand
         finger = hand.fingers[i]
         for j in range(0,4): #for all bones in finger
            bone = finger.bone(j)
            boneBase = bone.prev_joint
            boneTip = bone.next_joint
            xBase = boneBase[0]
            yBase = boneBase[1]
            zBase = boneBase[2]
            xTip = boneTip[0]
            yTip = boneTip[1]
            zTip = boneTip[2]
            lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))
            if ( (j==0) | (j==3) ):
            	testData[0,k] = xTip
               	testData[0,k+1] = yTip
               	testData[0,k+2] = zTip
               	k = k + 3      
      plt.axis('off')
      plt.show()
      plt.draw()
      if((frame.hands.is_empty) == True):
         programState = 0
         plt.clf()
         
      elif (isHandCentered(hand_center) == True):
      	 if levelThree()== True:
      	 	a = 5
      	 elif levelTwo()==True:
      	 	a=10
         programState = 2
         time.sleep(2)
         plt.clf()

   jump=0  
   while (programState == 2):  #if hand is over Leap and centered
      frame = controller.frame()
      hand = frame.hands[0]
      hand_center = hand.palm_position
      plt.clf()
      
      gs3 = gridspec.GridSpec(3, 1)
      
      #ax = fig.add_subplot(2,1,2, projection='3d')#111, projection='3d' )
      #ax.set_xlim(0,300)
      #ax.set_ylim(0,300)
      #ax.set_zlim(0,200)
      #ax.view_init(azim=90)
      #ax.axis('off') # clear x- and y-axes
      
      ax2 = fig.add_subplot(gs3[1])
      ax4 = fig.add_subplot(gs3[2])
      ax4.axis('off')
      
      ax3 = fig.add_subplot(gs2[0])
      #ax3.autoscale(False)
      
      level1 = ('imgs/levelOne.png')  ########### STILL NEED TO CREATE ##############
      level1 = plt.imread(level1)
      level2 = ('imgs/levelTwo.png')  ########### STILL NEED TO CREATE ##############
      level2 = plt.imread(level2)
      level3 = ('imgs/levelThree.png')  ########### STILL NEED TO CREATE ##############
      level3 = plt.imread(level3)
      
      #ax3.imshow(image244)
      ax3.axis('off')
      if((frame.hands.is_empty) == True):
         programState = 0
         plt.clf()
         
      elif(isHandCentered(hand_center) == False):
         programState = 1
         plt.clf()

      print '***', num
      image_file3 = ('imgs/asl'+ str(num) +'.png')
      image3 = plt.imread(image_file3)
      ax2.imshow(image3)
      
      ax2.autoscale(False)
      ax2.axis('off')
      plt.axis('off')
      k = 0
      for i in range(0,5): #for all fingers in hand
         finger = hand.fingers[i]
         for j in range(0,4): #for all bones in finger
            bone = finger.bone(j)
            boneBase = bone.prev_joint
            boneTip = bone.next_joint
            xBase = boneBase[0]
            yBase = boneBase[1]
            zBase = boneBase[2]
            xTip = boneTip[0]
            yTip = boneTip[1]
            zTip = boneTip[2]
            lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))
            if ( (j==0) | (j==3) ):
            	testData[0,k] = xTip
               	testData[0,k+1] = yTip
               	testData[0,k+2] = zTip
               	k = k + 3
               	
      
      ax4.plot([1,2,3])
      if levelThree()== True:
      	a-=1
      	ax3.imshow(level3)
      	time.sleep(.3)
      elif levelTwo()== True:
      	a-=1
      	ax3.imshow(level2)
      	time.sleep(.3)
      else:
      	ax3.imshow(level1)
      
      if (hand.is_left):
         hand = scale_transformation(hand)
      if levelThree()== True:
      	 if a ==0:
      		programState =4;
      elif levelTwo()== True:
      	 if a ==0:
      		programState =4;
      testData = CenterData(testData)
      predictedClass = clf.predict(testData)
      ax4.axis('off')
      
      
      warmer = ('imgs/warm.png')
      warm = plt.imread(warmer)
      
      colder = ('imgs/cold.png')
      cold = plt.imread(colder)
      
      if (num!=0) and (num+1==predictedClass or num-1==predictedClass):
      	ax4.imshow(warm)
      	ax4.autoscale(False)
      elif predictedClass!=num or predictedClass==[]:
      	ax4.imshow(cold)
      	ax4.autoscale(False)
      plt.show()
      plt.draw()
      plt.clf()
      
      if (predictedClass == num):
         print 'success!'
         dictSigns(str(num))
         programState = 3
         
   while (programState == 3):  #correctly signed number
      frame = controller.frame()
      #print programState
      hand = frame.hands[0]
      hand_center = hand.palm_position
      plt.clf()
      j=0
      for values in range(0,10):
      	#print(str((database[userName])[str(values)])+"bongos")
      	j+=(database[userName])[str(values)] #j is the players current score.
      
      ultimatescore, yourscore = points()
      if yourscore>ultimatescore:
	  	(database['ultimatescore'])['score']=yourscore
      if yourscore>(database[userName])['highscore']:
	  	(database[userName])['highscore']=yourscore
	  	
	  
	  	
      ax = fig.add_subplot(2,2,4,  sharex=ax, sharey=ax)
      ax.text(3, 8, 'Personal High Score: '+str((database[userName])['highscore'])+'\nOverall High Score: '+str((database['ultimatescore'])['score'])+'\n Current Score: '+str(j), style='italic',bbox={'facecolor':'green', 'alpha':.3, 'pad':4000})
      ax.axis('off')
      
      
      ax3 = fig.add_subplot(2,2,3, sharex=ax, sharey=ax)
      ax3.autoscale(False)
      ax3.axis('off')
      ax2 = fig.add_subplot(2, 2, 2, sharex=ax, sharey=ax)
      ax2.imshow(image4)
      ax2.autoscale(False)
      ax2.axis('off')
      ax3.text(3, 8, 'Number   Times Signed\n0:              '+str((database[userName])['0'])+"\n1:              "+str((database[userName])['1'])+"\n2:              "+str((database[userName])['2'])+"\n3:              "+str((database[userName])['3'])+"\n4:              "+str((database[userName])['4'])+"\n5:              "+str((database[userName])['5'])+"\n6:              "+str((database[userName])['6'])+"\n7:              "+str((database[userName])['7'])+"\n8:              "+str((database[userName])['8'])+"\n9:              "+str((database[userName])['9']), style='italic',bbox={'facecolor':'green', 'alpha':1.0, 'pad':50})
      
      plt.axis('off')
      plt.show()
      plt.draw()
      time.sleep(3)
      programState = 2
      predictedClass = getNum()
      num = predictedClass
      if((frame.hands.is_empty) == True):
      	programState = 0
      	plt.clf()
      if(isHandCentered(hand_center) == True):
   	  	if levelThree()== True:
   	  		a = 5
   	  	elif levelTwo()== True:
   	  		a = 10
   	  	programState = 2
   	  	plt.clf()
      if(isHandCentered(hand_center) == False):
   	  	programState = 1
   	  	plt.clf()
   	  

   while (programState == 4):
   	  frame = controller.frame()
   	  hand = frame.hands[0]
   	  hand_center = hand.palm_position
   	  plt.clf()
   	  gs13 = gridspec.GridSpec(1, 1)
   	  ax12 = fig.add_subplot(gs13[0])
   	  ax12.imshow(image5)
   	  ax12.autoscale(False)
   	  plt.axis('off')
   	  plt.show()
   	  plt.draw()
   	  time.sleep(3)
   	  programState = 2
   	  predictedClass = getNum()
   	  num = predictedClass
   	  print "I've Won"
   	  if((frame.hands.is_empty) == True):
   	     programState = 0
   	     plt.clf()
   	  if(isHandCentered(hand_center) == False):
   	    programState = 1
   	    plt.clf()
   	  if (isHandCentered(hand_center) == True):
   	  	if levelThree()== True:
   	  		a = 0
   	  	elif levelTwo()== True:
   	  		a = 0
   	  	programState = 2
   	  	plt.clf()
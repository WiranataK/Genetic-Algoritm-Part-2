from numpy.random import seed
from numpy.random import randint
from random import random

def rulenya(c):
  array = c.split(" ")
  rule = [0]*15

  #SUHU
  if(array[0] == "Rendah"):
    rule[0] = 1
  elif(array[0] == "Normal"):
    rule[1] = 1
  elif(array[0] == "Tinggi"):
    rule[2] = 1 
				
	#WAKTU
  if(array[1] == "Pagi"):
    rule[3] = 1
  elif(array[1] == "Siang"):
    rule[4] = 1
  elif(array[1] == "Sore"):
    rule[5] = 1
  elif(array[1] == "Malam"):
    rule[6] = 1
		
	#KONDISI LANGIT
  if(array[2] == "Berawan"):
    rule[7] = 1
  elif(array[2] == "Rintik"):
    rule[8] = 1
  elif(array[2] == "Hujan"):
    rule[9] = 1
  elif(array[2] == "Cerah"):
    rule[10] = 1
		
	#KELEMBAPAN
  if(array[3] == "Rendah"):
    rule[11] = 1
  elif(array[3] == "Normal"):
    rule[12] = 1
  elif(array[3] == "Tinggi"):
    rule[13] = 1
		
	#TERBANG GAK?
  if(array[4] == "Ya"): #YOI
    rule[14] = 1
  else:
    rule[14] = 0 #SKIP
  
  return rule

#BUAT BACA FILE
def bacafile(file):
  f = open(file, "r")
  i = 0
  testData = []
  line = f.readline()
  while( line != ""):
    i = i + 1
    line = line.replace("\n", "")
    testData.append(rulenya(line))
    line = f.readline()

  f.close()
  return testData

#POPOULASI
def ukuranpopulasi():
  for i in range(0 , len(pop)):
    pop[i] = Chromosome()
    pop[i].gen = randint(0, 2, 15 * randint(1,4))

#PERBANDINGAN
def comparison(chromosome , data):
  Counter = len(chromosome)/15
  differentAnswer = int(chromosome[len(chromosome)-1] == 0)
  valid = False
  rule = 0
  while(valid==False):
    if(rule >= Counter):
      break
    createLoc = rule*15
  
    #SUHU
    session = data[0] and chromosome[createLoc + 0]
    session = session or (data[1] and chromosome[createLoc + 1])
    session = session or (data[2] and chromosome[createLoc + 2])  
    if(session==0):
      rule = rule + 1
      continue
  
    #WAKTU
    session = data[3] and chromosome[createLoc + 3]
    session = session or (data[4] and chromosome[createLoc + 4])
    session = session or (data[5] and chromosome[createLoc + 5])
    session = session or (data[6] and chromosome[createLoc + 6])
    if(session==0):
      rule = rule + 1
      continue
  
    #KONDISI LANGIT
    session = data[7] and chromosome[createLoc + 7]
    session = session or (data[8] and chromosome[createLoc + 8])
    session = session or (data[9] and chromosome[createLoc + 9])
    session = session or (data[10] and chromosome[createLoc + 10])
    if(session==0):
      rule = rule + 1
      continue
  
    #KELEMBAPAN
    session = data[11] and chromosome[createLoc + 11]
    session = session or (data[12] and chromosome[createLoc + 12])
    session = session or (data[13] and chromosome[createLoc + 13])
    if(session==0):
      rule = rule + 1
      continue
  
    #VALID GA?
    valid = True
    if(valid):
      return chromosome[(rule*15) + 14]
    else:
      return differentAnswer

#FUNGSI FITNESS
def fitness(chromosome):
  value = 0
  for i in range( 0 , len(testData)):
    Result = comparison(chromosome , testData[i])
    if(Result == testData[i][14]):
      value = value + 1
  
  return value/(len(testData)*1.0)

#NYARI ORTU
def nyariortu(fitnessSummary):
  probability = random()*fitnessSummary
  for i in range(0 , popCounter):
    probability -= pop[i].fit
    if(probability < 0):
      return i

  return 0

#ORTU PALING KECIL
def nyariortuterkecil(par):
  if(len(pop[par[0]].gen)>=len(pop[par[1]].gen)):
    return 1
  else:
    return 0

#RANDOM POINTER
def pointerRange(chromosome):
  x=0
  y=0
  while(x==y):
    x = randint(0,len(chromosome.gen))
    y = randint(0,len(chromosome.gen))
  if(y>x):
    return [x,y]
  else:
    return [y,x]

#NGUBAH POINTER
def converter(pntr,minRg):
  Pointer = pntr//15
  Loc = pntr%15
  if(Loc < 3 and minRg>=3):
    return [Pointer*15+0 , Pointer*15+2]
  elif(Loc <7 and minRg>=4):
    return [Pointer*15+3 , Pointer*15+6]
  elif(Loc < 11 and minRg>=4):
    return [Pointer*15+7 , Pointer*15+10]
  elif(Loc < 14 and minRg>=3):
    return [Pointer*15+11 , Pointer*15+13]
  elif(Loc == 14 and minRg>=1):
    return [Pointer*15+14 , Pointer*15+14]
  else:
    return None

#POINTER LAIN
def otherPntr(pts):
  othr = []
  othr.append(pts)
  minRg = pts[1]-pts[0]+1
  x = converter(pts[0],minRg)
  if(x!= None):
    othr.append(x)
  x = converter(pts[1],minRg)
  if(x!= None):
    othr.append(x)
  
  return othr

#CROSSOVER A
def CrossA(parA , parB , ptrA , ptrB):
  child = []
  maks = (ptrB[0]) + (ptrA[1]-ptrA[0]+1)+(len(parB) - 1 - ptrB[1])
  maks = maks - (maks%15)
  for i in range(0,ptrB[0]):
    child.append(parB[i])
    maks -= 1
    if(maks==0):
      return child
  for i in range(ptrA[0],ptrA[1]+1):
    child.append(parA[i])
    maks -= 1
    if(maks==0):
      return child
  for i in range(ptrB[1]+1,len(parB)):
    child.append(parB[i])
    maks -= 1
    if(maks==0):
      return child

  return child

#CROSSOVER B
def CrossB(parA , parB , ptrB):
  i=0
  child = []
  while(i < len(parB)):
    if(CrossTengah(ptrB , i)):
      child.append(parB[i])
    else:
      child.append(parA[i])
    i = i+ 1
  
  return child

#CROSSOVER TENGAH-TENGAH
def CrossTengah(pts , pntr):
  return pntr >= pts[0] and pntr <= pts[1]

#CROSSOVER
def Cross(parA , parB , ptrA , otpt):
  ptrB = otpt[randint(0,len(otpt))]
  if(len(parA) < len(parB)):
    temp = parB
    parB = parA
    parA = temp
  childA = CrossA(parB  ,parA , ptrA , ptrB)
  childB = CrossB(parA , parB , ptrB)
  return [childA , childB]

#MUTASI
def mutasi(child):
  for i in range(0,len(child)):
    if(random() < mutasiProb):
      child[i] = int(child[i]==0)

  return child

#FITNESS INDEX TERKECIL
def fitidxkecil():
  mn = 1
  idx = 0
  for i in range(0,len(pop)):
    if(pop[i].fit < mn):
      mn = pop[i].fit
      idx=i
    elif(pop[i].fit == mn and random() < 0.2):
      idx=i

  return idx

#FITNESS INDEX TERBESAR
def fitidxbesar():
  mn = 0
  idx = 0
  for i in range(0,len(pop)):
    if(pop[i].fit > mn):
      mn = pop[i].fit
      idx=i
    elif(pop[i].fit == mn and random() < 0.2):
      idx=i

  return idx

#SELEKSI INDIVIDU
def seleksiindividu(child):
  fitptr = fitness(child)
  idxkcl = fitidxkecil()
  if(pop[idxkcl].fit > fitptr):
    return
  
  pop[idxkcl].fit = fitptr
  pop[idxkcl].gen = child

#KROMOSOM
class Chromosome:
  gen = []
  fit = 0


####################
### MAIN PROGRAM ###
####################


testData = None
popCounter = 10
pop = [None] * popCounter
fitnessSummary = 0
mutasiProb = 0.01
limit = 1000
testData = bacafile("datatest.txt")

#FITNESS
ukuranpopulasi()
for i in range(0 , popCounter):
  pop[i].fit = fitness(pop[i].gen)
loop = 0
while(loop < limit):
  fitnessSummary = 0
  for i in range(0 , popCounter):
    fitnessSummary = fitnessSummary + pop[i].fit

  #ORTU NYA
  par = [0,0]
  while(par[0] == par[1]):
    par[0]=nyariortu(fitnessSummary)
    par[1]=nyariortu(fitnessSummary)
  shortestpar = nyariortuterkecil(par)

  #POINTER
  pntr = pointerRange(pop[par[shortestpar]])
  otherpntr = otherPntr(pntr)
  child = Cross(pop[par[0]].gen,pop[par[1]].gen,pntr , otherpntr)
  len(child[0])
  len(child[1])

  #MUTASI
  child[0] = mutasi(child[0])
  child[1] = mutasi(child[1])

  #SELEKSI INDIVIDU
  seleksiindividu(child[0])
  seleksiindividu(child[1])
  loop += 1

idx = fitidxbesar()
print("")
print("Gen : ", pop[idx].gen)
print("")
print("HASIL TERBAIK : ", idx)
print("Fitness : ", pop[idx].fit)

dataUji = bacafile("datauji.txt")
f = open("hasil.txt", "w")
print("")
print("Hasil :")
for i in range( 0 , len(dataUji)):
  resultAnswer = comparison(pop[idx].gen , dataUji[i])
  print(i,resultAnswer)
  f.write(str(resultAnswer)+"\n")
f.close()
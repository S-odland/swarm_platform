
letters = ['A', 'B', 'C', 'D']
numbers = ['1','2','3','4','5','6','7']

def decimalToBinary(n,num):
    temp = str(bin(n).replace("0b", ""))
    if len(temp) < num:
      temp = '0'*(num-len(temp)) + temp
    return temp

def decimalToBinary2(n,num):
    temp = str(bin(int(n)).replace("0b", ""))
    if len(temp) < num:
      temp = '0'*(num-len(temp)) + temp
    return temp    

bins = []
for i in range(0,32):
    bins.append(decimalToBinary(i,5))

regionbins = []
for i in range(0,10):
    regionbins.append(decimalToBinary(i,4))

regiondict = {

}

for i in range(0,len(regionbins)):
    regiondict[str(i)]=regionbins[i]

# print(regiondict)

bbdict = {
  "112": "0",
  "01": "1",
  "02": "2",
  "05": "3",
  "06": "4",
  "11": "5",
  "12": "6",
  "14": "7",
  "19": "8",
  "110": "9" 
}

policydict = {
  "D1": bins[0],
  "B1": bins[1],
  "C1": bins[2],
  "A1": bins[3],
  "D5": bins[4],
  "B5": bins[5],
  "C5": bins[6],
  "A5": bins[7],
  "D3": bins[8],
  "B3": bins[9],
  "C3": bins[10],
  "A3": bins[11],
  "D7": bins[12],
  "B7": bins[13],
  "C7": bins[14],
  "A7": bins[15],
  "D2": bins[16],
  "B2": bins[17],
  "C2": bins[18],
  "A2": bins[19],
  "D6": bins[20],
  "B6": bins[21],
  "C6": bins[22],
  "A6": bins[23],
  "D4": bins[24],
  "B4": bins[25],
  "C4": bins[26],
  "A4": bins[27]
  # "D7": bins[28],
  # "B7": bins[29],
  # "C7": bins[30],
  # "A7": bins[31]
}

# ivd = {v: k for k, v in policydict.items()}
ivd = dict((v, k) for k, v in policydict.items())
# print(bins)
# print(bins[12])
# print(policydict)
# print(ivd)
# print(bins[12])
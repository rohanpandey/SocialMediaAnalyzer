import os
import Msft_Vision_onlocalImage
entries = os.listdir('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\ponnurangam.kumaraguru\\Uploaded Photos')
count=0
for entry in entries:
   print(entry)
   print(Msft_Vision_onlocalImage.get_caption())
   count+=1
   if(count==5):
       break
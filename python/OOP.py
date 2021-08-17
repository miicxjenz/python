#Contact on Phone
from dataclasses import dataclass, field    #เป็นการบอกว่าตัวนี้จะเป็น class ที่เราใช้นะ
from typing import Dict,List,Optional    #เป็นการบอกว่าเราใช้ data type ประเภทไหน
from uuid import uuid1, uuid4
from collections import defaultdict
import numpy as np

#Write Contact(Create contact contain to Object.)
@dataclass
class Contact:
    name: str   #name = str   #ความหมายคือมี type เป็น string
    phone: str  #phone = str  #ความหมายคือมี type เป็น string
    country: str

ContactID = str

@dataclass
class PhoneBook:
    name:str #ความหมายคือมี type เป็น string
    contact: Dict[str,Contact] = field(default_factory=dict)
    #Dict[str,Contact] คือเก็บตั้งแต่ string ไปหา Contact
    #@dataclass ช่วยในการเวลาสร้าง object มาแล้วให้มันสามารถ print ได้เพราะปกติเวลาสร้าง object ก็จะเป็นค่าไรไม่รู้อ่านไม่ออก

                                                     #self ทำให้เราสามารถ refer ได้ว่าเราสามารถเชื่อมโยงไปหา contact กับ name ได้
    def add_contact(self, ct:Contact) -> ContactID:  # ct has type is Contact and its return is ContactID
        contact_id = str(uuid4())
        #uuid4() คือวิธีการได้ random number มาแบบเร็วๆ เป็น ramdom string ยาวๆ
        self.contact[contact_id] = ct # self.contact ที่ contact id
        return ContactID 
    
    def add_contacts(self, cts:List[Contact]) -> List[ContactID]:
        return [self.add_contact(ct) for ct in cts]

    def filter_country(self, country:str) -> List[Contact]:
        return list(filter(lambda word: word.country ==country,self.contact.value()))

pb = PhoneBook(name = 'PhoneBook1')
#ct1 = Contact(name ="Micjen", phone="0928830594")
#pb.add_contact(ct1)
#print(pb)

cts =[Contact(name=f"Contact{i}", phone=f"{i}",country=".") for i in range(10)]
pb.add_contacts(cts)
print(pb)


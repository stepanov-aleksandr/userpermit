from Crypto.Cipher import Blowfish
from ui import Ui_ROOT
import random
from PyQt5 import QtWidgets
from struct import pack
import sys
import binascii

def Random():
    return str(random.randrange(11111, 99999, 1))

def Crypt(text_,key_):
    bs = Blowfish.block_size
    key = bytes(key_, 'utf-8')
    cipher = Blowfish.new(key,Blowfish.MODE_ECB)
    plaintext = bytes(text_, 'utf-8')
    plen = bs - divmod(len(plaintext), bs)[1]
    padding = [plen] * plen
    padding = pack('b' * plen, *padding)
    encrypted_data = cipher.encrypt(plaintext + padding)
    return encrypted_data

def Decrypt(encrypted_data,key):
    cipher = Blowfish.new(key)
    return cipher.decrypt(encrypted_data)


class mywindow(QtWidgets.QMainWindow):
    def slot_create_hw_id(self):
        m_key = self.ui.m_key.text()
        hw_id = self.ui.hw_id.text()
        userpermit = Crypt(hw_id,m_key)
        self.ui.userpermit.clear()
        for i in userpermit:
            self.ui.userpermit.insert(str(hex(i))[2:])
        self.ui.userpermit.setText(self.ui.userpermit.text().upper())
        crc = binascii.crc32(self.ui.userpermit.text().encode().upper())
        crc_hex = hex(crc)
        crc_str = str(crc_hex)
        self.ui.userpermit.insert(crc_str[2:].upper())
        self.ui.userpermit.insert("3130")
        self.ui.size_user_permit.display(len(userpermit) * 2)

    def CreateHW_ID(self):
        hw_id = Random()
        self.ui.hw_id.setText(hw_id)

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_ROOT()
        self.ui.setupUi(self)
        self.ui.create.clicked.connect(self.slot_create_hw_id)
        self.ui.pushButton.clicked.connect(self.CreateHW_ID)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()


sys.exit(app.exec())





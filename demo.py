import xlrd
import tkinter as tk
from tkinter import ttk
import threading

class AddressInfo(object):

    def get_workbook(self):
        self.workbook = xlrd.open_workbook("address.xls")
        self.sheet = self.workbook.sheet_by_name("Sheet1")
        return self.sheet
    def get_address_datas(self):
        rows = self.get_workbook().nrows
        datas = []
        for i in range(2, rows):
            datas.append(self.get_workbook().row_values(i))
        # print(datas)
        return datas
    def get_chain_datas(self):
        chain_datas = []
        rows = self.get_workbook().nrows
        for i in range(2, rows):
            chain_datas.append(self.get_workbook().row_values(i)[0])
        chain_datas = list(set(chain_datas))
        chain_datas.sort()
        # print(chain_datas)
        return chain_datas

    def show_address(self, chain):
        self.chain = chain
        self.chain = combobox_address.get()
        private_text.delete(1.0, tk.END)
        rows = AddressInfo().get_workbook().nrows
        for i in range(2, rows):
            if self.chain == AddressInfo().get_address_datas()[i][0]:
                chain_address = AddressInfo().get_address_datas()[i][1]
                chain_key = AddressInfo().get_address_datas()[i][2]
                chain_info = "链：" + self.chain + "\n" + \
                             "链地址: " + chain_address + "\n" + "私钥/助记词： " + chain_key + "\n" + "\n"
                private_text.insert(1.0, chain_info)



window = tk.Tk()
window.title("demo")
window.geometry("1000x600+20+20")

frame = ttk.Frame(window)
frame.pack()

# 链选择框
combobox_address = ttk.Combobox(frame)
combobox_address['value'] = AddressInfo().get_chain_datas()
combobox_address.current(0)
combobox_address.pack()
combobox_address.bind("<<ComboboxSelected>>", threading.Thread(target=AddressInfo().show_address))
#地址信息展示框
private_text = tk.Text(frame, height=15)


#滚动条
scroll_bar = tk.Scrollbar(frame)
scroll_bar.config(command=private_text)
private_text.config(yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
private_text.pack()

window.mainloop()

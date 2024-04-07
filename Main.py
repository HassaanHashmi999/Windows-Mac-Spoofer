import tkinter as tk
import tkinter.messagebox
import customtkinter
import subprocess
import regex as re
import string
import random
import psutil
import pandas as pd
import time
from scapy.all import ARP, Ether, srp

# the registry path of network interfaces
network_interface_reg_path = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
# the transport name regular expression, looks like {AF1B45DB-B5D4-46D0-B4EA-3E18FA49BF5F}
transport_name_regex = re.compile("{.+}")
# the MAC address regular expression
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
devices_list = []
randmac_list = []


check=[0,0,0,0]
class MenuWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.geometry("920x430")
        # configure grid layout (4x4)
        
        self.logo_label = customtkinter.CTkLabel(self, text="Developed by:Hassaan Hashmi", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, padx=20, pady=5)

        self.logo_label = customtkinter.CTkLabel(self, text="Roll:i191777", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, padx=20, pady=5)
        self.logo_label = customtkinter.CTkLabel(self, text="Section:CS(A)", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=2, padx=20, pady=5)
        self.logo_label = customtkinter.CTkLabel(self, text="Deegree:CYSEC", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=3, padx=20, pady=5)
        self.logo_label = customtkinter.CTkLabel(self, text="Campus:Islamabad", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=4, padx=20, pady=5)
        self.logo_label = customtkinter.CTkLabel(self, text="Course:Ethical Hacking", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=5, padx=20, pady=5)
        self.logo_label = customtkinter.CTkLabel(self, text="11:32pm 3/10/24", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=6, padx=20, pady=5)
        self.logo_label = customtkinter.CTkLabel(self, text="The Mac Address Changer app allows users to change the MAC address of their network adapters.\n It provides options to change the MAC address randomly, select from network devices, choose from manufacturer MAC prefixes,\n or input a custom MAC address. The app also displays connected adapters and their MAC addresses.", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.logo_label.grid(row=7, padx=20, pady=5)
        # create scrollable radiobutton frame
        self.continue_button = customtkinter.CTkButton(self,height=60,width=300, text="Continue", command=self.open_main_app)
        self.continue_button.grid(row=8,pady=7)

    def open_main_app(self):
        self.destroy()  # Close the menu window
        app = App()
        app.mainloop()


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        state="normal" if self.check_item(item) else "disabled"
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable,state=state)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10), sticky="w")
        self.radiobutton_list.append(radiobutton)
    def check_item(self, item):
        connected_adapters_mac=[]
        for potential_mac in subprocess.check_output("getmac").decode().splitlines():
            mac_address = mac_address_regex.search(potential_mac) 
            if mac_address:
                connected_adapters_mac.append(mac_address.group())
        extracted_mac =mac_address_regex.search(item)
        match=extracted_mac.group()
        if match in connected_adapters_mac:
            return 1
        else:
            return 0
    def get_checked_item(self):
        global originmac
        originmac=self.radiobutton_variable.get()
        return self.radiobutton_variable.get()
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Mac Address Changer.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=350, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="MacAddress Changer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # create scrollable radiobutton frame
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.sidebar_frame, width=500, command=self.radiobutton_frame_event,
                                                                       item_list=self.get_connected_adapters_mac_address(),
                                                                       label_text="Name | MAC (Select the Interface)")
        self.scrollable_radiobutton_frame.grid(row=1, column=0, padx=15, pady=15, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=350)

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.CustomMAC = customtkinter.StringVar()  # custom mac address
        self.CustomMAC.set("00:00:00:00:00:00(CUSTOM)")
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self.sidebar_frame,width=215,textvariable=self.CustomMAC)
        self.entry.grid(row=3, column=0, padx=20, pady=0,sticky='w')
        self.customB = customtkinter.CTkButton(master=self.sidebar_frame,text='GO!!',border_width=2,command=self.get_entry_value)
        self.customB.grid(row=3, column=0, padx=20, pady=0, sticky="e")
        self.resetB = customtkinter.CTkButton(self.sidebar_frame,border_width=2,hover_color='red',text='RESET',font=customtkinter.CTkFont(size=20, weight="bold"),command=self.origin)
        self.resetB.grid(row=4, column=0, padx=20, pady=30, sticky="nsew")
        # create tabview
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="nsew")
        self.tabview.add("Manufacturer MACs")
        self.tabview.add("Network MACs")
        self.tabview.add("Random MAC")
        self.tabview.tab("Manufacturer MACs").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Network MACs").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Random MAC").grid_columnconfigure(0, weight=1)
        self.Manufacture = customtkinter.StringVar()
        self.Manufacture_Mac = customtkinter.StringVar()
        self.Manufacture_Mac.set("<<<Select Manufacturer Mac Prefix>>>")
        self.Manufacture.set("<<<Select Manufacturer>>>")
        self.Network_Mac = customtkinter.StringVar()                    # network mac address
        self.Network_Mac.set("<<<Select Network Mac>>>")     
        self.m_Mac = customtkinter.StringVar()                          # the manufacture mac
        self.m_Mac.set("<<<Select Mac>>>")                          
        self.randmac = customtkinter.StringVar()                        # random mac
        self.randmac.set("<<<Select Random Mac>>>")
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Manufacturer MACs"),dynamic_resizing=False,width=390,
                                                        values=self.get_manufacturer_name(),variable=self.Manufacture,anchor="center")
        self.Manufacture.trace_add("write", self.get_manufacturer)
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
       
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Manufacturer MACs"),width=260,justify='center',
                                                    values=self.get_manufacturer_mac(self.Manufacture.get()) ,variable=self.Manufacture_Mac)
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.Manufacture_Mac.trace_add("write", self.generate_manufacturer_mac_options)
        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.tabview.tab("Manufacturer MACs"), dynamic_resizing=False, width=390,
                                                values=[], variable=self.m_Mac, anchor="center",
                                                )
        self.optionmenu_3.grid(row=2, column=0, padx=20, pady=(20, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Manufacturer MACs"), text="Go!!!",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))
        
        
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Network MACs"), text="Scan",
                                                           command=self.get_scan)
        self.string_input_button.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Network MACs"),width=390,
                                                        values=self.get_mac_devices(),variable=self.Network_Mac,anchor="center")
        self.optionmenu_2.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.progressbar_1 = customtkinter.CTkProgressBar(self.tabview.tab("Network MACs"))
        self.progressbar_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
        
        
        self.progressbar_2 = customtkinter.CTkProgressBar(self.tabview.tab("Random MAC"))
        self.progressbar_2.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.randbutton = customtkinter.CTkButton(self.tabview.tab("Random MAC"), text="Generate",
                                                           command=self.generate_random_mac)
        self.randbutton.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.optionmenu_4 = customtkinter.CTkOptionMenu(self.tabview.tab("Random MAC"),width=390,
                                                        values=[],variable=self.randmac,anchor="center")
        self.optionmenu_4.grid(row=4, column=0, padx=20, pady=(20, 10))
        
        self.changeTHEMAC = customtkinter.CTkButton(self, text="Change MAC Address",command=self.changemac,
                                                           font=customtkinter.CTkFont(size=20, weight="bold"))
        self.changeTHEMAC.grid(row=1, column=1, padx=20, pady=(25, 10),sticky='nsew')
        self.progressbar_3 = customtkinter.CTkProgressBar(self)
        self.progressbar_3.grid(row=2, column=1, padx=(20, 10), pady=(5, 10), sticky="ew")
        
    def get_scan(self):
        global check
        check=[0,0,1,0]
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        ip_range = "192.168.100.1/24"
        devices_list.clear()
        arp_request = ARP(pdst=ip_range)
        ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = ether_frame / arp_request

        answered_list, unanswered_list = srp(arp_request_broadcast, timeout=1, verbose=False)

        for element in answered_list:
            device_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices_list.append(device_dict)
            
        # Update the options in the Network_Mac option menu
        self.optionmenu_2.configure(values=self.get_mac_devices())
        # Set the default value to the first option if available
        #self.progressbar_1.stop()
        if devices_list:
            self.Network_Mac.set(devices_list[0]["mac"])
        else:
            self.Network_Mac.set("<<<No devices found>>>")
    def get_mac_devices(self):
        mac = []
        #self.get_scan()
        for device in devices_list:
            mac.append(device["mac"])
        return mac
    def generate_manufacturer_mac(self, val):
        man_mac = []
        val="".join(c for c in val if c in string.hexdigits).upper() 
        uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
        random.seed(time.time())
        for i in range(10):
            man_mac.append(val + "".join(random.sample(uppercased_hexdigits, k=6)))
        # 2nd character must be 2, 4, A, or E
        print(man_mac)
        return man_mac
    
    def generate_manufacturer_mac_options(self, *args):
        selected_prefix = self.Manufacture_Mac.get()
        options = self.generate_manufacturer_mac(selected_prefix)
        self.optionmenu_3.configure(values=options)
        #self.m_Mac.set(options[0] if options else "<<<No options>>>")
    def generate_random_mac(self):
        global check

        check=[0,0,0,1]
        self.progressbar_2.configure(mode="indeterminnate")
        self.progressbar_2.start()
        uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
        # 2nd character must be 2, 4, A, or E
        random.seed(time.time())
        for i in range(10):
            randmac_list.append(random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(random.sample(uppercased_hexdigits, k=10)))
        self.optionmenu_4.configure(values=randmac_list)
        self.randmac.set(randmac_list[0])
        
    def origin(self):
        print(originmac)
        extracted_mac = mac_address_regex.search(originmac)
        originmac = extracted_mac.group
        connected_adapters_mac = self.get_connected_adaptersT()
        #print(connected_adapters_mac)
        target_transport_name=self.get_choice(connected_adapters_mac,thechange)
        adapter_index = self.change_mac_address(target_transport_name, self.m_Mac.get())
        self.disable_adapter(adapter_index)
        print("[+] Adapter is disabled")
        self.enable_adapter(adapter_index)
        print("[+] Adapter is enabled again")


    
    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}")
    def get_entry_value(self):
        global check
        check=[1,0,0,0]
        print(self.CustomMAC.get())
    def open_input_dialog_event(self):
        global check
        check=[0,1,0,0]
    def get_connected_adapters_mac_address(self):
        # make a list to collect connected adapter's MAC
        adapters_mac = []
        
        # iterate over all network interfaces
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    mac_address = addr.address
                    interface_name = interface
                    adapters_mac.append(interface_name +" " +mac_address)
        return adapters_mac
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def get_manufacturer_name(self):
        file_path = 'grouped_mac_addresses.csv'
        df = pd.read_csv(file_path)
        return df['Vendor Name'].tolist()
    def get_manufacturer(self,*args):
        #print(args)
        selected_manufacturer = self.Manufacture.get()
        new_mac_values = self.get_manufacturer_mac(selected_manufacturer)
        print(self.Manufacture.get())
        self.combobox_1.set("")
        if selected_manufacturer:
            self.combobox_1.configure(state="normal")
        else:
            self.combobox_1.configure(state="disabled")
        # Add the new values to the combobox
        if new_mac_values:
            self.combobox_1.configure(values=new_mac_values)
            self.combobox_1.set(new_mac_values[0])
    def get_manufacturer_mac(self,manufacturer): 
        file_path = 'grouped_mac_addresses.csv'
        df = pd.read_csv(file_path)
        row = df[df['Vendor Name'] == manufacturer]
        if not row.empty:
            mac_prefixes = row['Mac Prefix'].tolist()
            if mac_prefixes:
                return random.choice(mac_prefixes).split(', ')
        return []
    def change_mac_address(self,adapter_transport_name, new_mac_address):
        # use reg QUERY command to get available adapters from the registry
        output = subprocess.check_output(f"reg QUERY " +  network_interface_reg_path.replace("\\\\", "\\")).decode()
        for interface in re.findall(rf"{network_interface_reg_path}\\\d+", output):
            # get the adapter index
            adapter_index = int(interface.split("\\")[-1])
            interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
            if adapter_transport_name in interface_content:
                # if the transport name of the adapter is found on the output of the reg QUERY command
                # then this is the adapter we're looking for
                # change the MAC address using reg ADD command
                changing_mac_output = subprocess.check_output(f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
                # print the command output
                print(changing_mac_output)
                # break out of the loop as we're done
                break
        # return the index of the changed adapter's MAC address
        return adapter_index
    def disable_adapter(self,adapter_index):
    # use wmic command to disable our adapter so the MAC address change is reflected
        disable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call disable").decode()
        return disable_output
    def enable_adapter(self,adapter_index):
        # use wmic command to enable our adapter so the MAC address change is reflected
        enable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call enable").decode()
        return enable_output
    def get_connected_adaptersT(self):
    # make a list to collect connected adapter's MAC addresses along with the transport name
        connected_adapters_mac = []
        # use the getmac command to extract 
        for potential_mac in subprocess.check_output("getmac").decode().splitlines():
            # parse the MAC address from the line
            mac_address = mac_address_regex.search(potential_mac)
            # parse the transport name from the line
            transport_name = transport_name_regex.search(potential_mac)
            if mac_address and transport_name:
                # if a MAC and transport name are found, add them to our list
                connected_adapters_mac.append((mac_address.group(), transport_name.group()))
        return connected_adapters_mac
    def clean_mac(self,mac):
        """Simple function to clean non hexadecimal characters from a MAC address
        mostly used to remove '-' and ':' from MAC addresses and also uppercase it"""
        return "".join(c for c in mac if c in string.hexdigits).upper()  
    def get_choice(self,connected,old):
        for i, option in enumerate(connected):
            if option[0]==old:
                return [option[1]]
    def format_mac_address(self,mac_address):
    # Ensure that the input string is in the correct format
        mac_address = mac_address.upper()
        if len(mac_address) != 12:
            raise ValueError("Invalid MAC address length")

        # Split the string into groups of two characters each
        formatted_mac = '-'.join([mac_address[i:i+2] for i in range(0, 12, 2)])

        return formatted_mac
    def changemac(self):
        global thechange
        self.progressbar_3.configure(mode="indeterminnate")
        self.progressbar_3.start()
        extracted_mac = mac_address_regex.search(self.scrollable_radiobutton_frame.get_checked_item())
        print(extracted_mac.group())
        old=extracted_mac.group()
        connected_adapters_mac = self.get_connected_adaptersT()
        #print(connected_adapters_mac)
        target_transport_name=self.get_choice(connected_adapters_mac,old)
        if (check==[0,0,0,0]):
            print("Cannot changemac",)

        if(check==[0,0,0,1]):
            print("rand")
            print(self.randmac.get())
            adapter_index = self.change_mac_address(target_transport_name, self.randmac.get())
            self.disable_adapter(adapter_index)
            print("[+] Adapter is disabled")
            self.enable_adapter(adapter_index)
            print("[+] Adapter is enabled again")
            thechange=self.format_mac_address(self.randmac.get())
            self.progressbar_3.stop()

        if(check==[0,0,1,0]):
            print("networks")
            print(self.clean_mac(self.Network_Mac.get()))
            adapter_index = self.change_mac_address(target_transport_name, self.clean_mac(self.Network_Mac.get()))
            self.disable_adapter(adapter_index)
            print("[+] Adapter is disabled")
            self.enable_adapter(adapter_index)
            print("[+] Adapter is enabled again")
            thechange=self.format_mac_address(self.clean_mac(self.Network_Mac.get()))
            self.progressbar_3.stop()

        if(check==[0,1,0,0]):
            print("manufacturer")
            print(self.m_Mac.get())
            adapter_index = self.change_mac_address(target_transport_name, self.m_Mac.get())
            self.disable_adapter(adapter_index)
            print("[+] Adapter is disabled")
            self.enable_adapter(adapter_index)
            print("[+] Adapter is enabled again")
            thechange=self.format_mac_address(self.m_Mac.get())
            self.progressbar_3.stop()
        if(check==[1,0,0,0]):
            print("custom")
            print(self.CustomMAC.get())
            adapter_index = self.change_mac_address(target_transport_name, self.CustomMAC.get())
            self.disable_adapter(adapter_index)
            print("[+] Adapter is disabled")
            self.enable_adapter(adapter_index)
            print("[+] Adapter is enabled again")
            thechange=self.format_mac_address(self.CustomMAC.get())
            self.progressbar_3.stop()
        else:
            print("Cannot DO NO MORE")
        
        

    

if __name__ == "__main__":
    menu_window = MenuWindow()
    menu_window.mainloop()

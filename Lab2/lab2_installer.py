from cx_Freeze import setup, Executable
import win32api, wmi, hashlib,  winreg
from ctypes import windll

n_value = 6819884858976479606203008597129034015850948528782488170470960918634684472651971697182432028982772570623067963897772032692853013313838775641095336283963168762043005965330965552867036700220027750430000294194155769195851491913224223203785611000559228949893286584518386295552113051994373093508398979029513874939300416758488196859449690659528952382157476299923546588297496938443326401101565615521842486966231992376229836446403513493018140602628413705835309763816240062684413901987467182677304806169449244584950399725691412786296347731889361087616087579119532557767589156087549270848092906571657439764636396652763192000471
e = 65537
d_value = 5467500349046847048072268713883097734513705031520525977153588928788088513017184871777197022060574234907100018175272599748465602217410060133341319616334419487106544035040576485240199814856653158297490661111359053196198074928860245530770401263109120775384029943958077640944864303596996455529316123063150411266530942675090198580043692580707907497576932852999553296101644460118237876336462964990948228612234249321550497243335025109599208202731618224774763428631043989657567371428648483917228394911499404107672447544045254895040725974022592099608320548706850361803104726518857788221615221300318956769453868709316147305073

def create_installer():
    product_name = "My Gui lab"
    version_name = "2.0"
    default_directory = "default_directory_for_lab2"

    bdist_msi_options = {
    "upgrade_code": "{48B079F4-B598-438D-A62A-8A233A3F8901}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\%s" %(default_directory)
    }
    
    exe_file = Executable(script="lab1.py",base="Win32GUI")

    setup(name=product_name, 
        version=version_name, 
        description="This is my installer!", 
        executables=[exe_file],
        options={"bdist_msi": bdist_msi_options})
    
def hash_and_sign_message(m, d, n):
    m = hashlib.md5(m.encode()).hexdigest()
    s = pow(int(m, base=16), d, n)
    return s

def get_user_info():
    myTuple = (win32api.GetUserName(), 
        win32api.GetComputerName(), 
        win32api.GetWindowsDirectory(), 
        win32api.GetSystemDirectory(),
        str(windll.user32.GetKeyboardType(0)),
        str(windll.user32.GetKeyboardType(1)),
        str(win32api.GetSystemMetrics(1)),
        str(round(win32api.GlobalMemoryStatusEx()['TotalPhys']/1024/1024/1024)),
        wmi.WMI().Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()) 
    info_about_target_device = ";;".join(myTuple)
    signature = hash_and_sign_message(info_about_target_device,d_value,n_value)
    return signature

def write_to_registry_editor(str_to_write):
    key = winreg.HKEY_CURRENT_USER
    key_value = "Software\Snigur_Anton"
    handle_of_the_opened_key  = winreg.CreateKey(key, key_value)
    winreg.SetValueEx(handle_of_the_opened_key, "personal_reg_of_Snigur_Anton", 0, winreg.REG_SZ, str_to_write)
    winreg.CloseKey(handle_of_the_opened_key)
    
if __name__ == "__main__":
    create_installer()
    write_to_registry_editor(str(get_user_info()))
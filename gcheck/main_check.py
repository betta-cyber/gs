# -*- coding: utf-8 -*-
from windows.conn import WindowsMachine
from windows.windows import Windows_check

# a = Linux_check("10.1.78.190", "betta", "killer551", check_type="linux")
# # print(a.run())

# ip = '10.19.201.100'
# username = 'administrator'
# password = 'killer551.'
# server = WindowsMachine(ip, username, password)
# ret, return_value = server.run_remote('cscript //NOLOGO C:\\Windows_check_build20190920.vbs', async=False, output=True))
# if return_value == "success" and self.xml_file.exists():
#     check_res = self._task_controller.convertxml_to_report(
#         self.xml_file, "html\\result.html")

a = Windows_check("1111", "10.19.201.88", "administrator", "killer551.", check_type="windows")
print(a.run())
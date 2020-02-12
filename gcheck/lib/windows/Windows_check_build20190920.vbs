'Author: autocreated
Dim argu_count, args_dic, uuid, template_version
uuid = split(WScript.ScriptName, ".")(0)
' 配置模板创建时间
template_time = "2019-07-05 19:51:20"
set args_dic = CreateObject("Scripting.Dictionary")
uservars = Array()
' 处理自定义参数
For Each var In uservars
    inputvalue = Cstr(inputbox("" & var(0),var(0)))
    args_dic.Add var(1), inputvalue
Next
dim obj_shell
set obj_shell = createobject("wscript.shell")
dim init_cmd(125)

' 声明初始化命令
init_cmd(0) = obj_shell.run("cmd /c secedit /export /cfg %tmp%\sec.log", 0, True)
init_cmd(1) = obj_shell.run("cmd /c wmic qfe get hotfixid > %tmp%\patch.log", 0, True)
init_cmd(3) = obj_shell.run("cmd /c echo On Error Resume Next>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(4) = obj_shell.run("cmd /c echo set objFirewall = CreateObject(""HNetCfg.FwMgr"")>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(5) = obj_shell.run("cmd /c echo ErrNum = Err.Number>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(6) = obj_shell.run("cmd /c echo On Error Goto ^0>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(7) = obj_shell.run("cmd /c echo If 0 ^<^> ErrNum Then>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(8) = obj_shell.run("cmd /c echo 	set ws = CreateObject(""WScript.Shell"")>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(9) = obj_shell.run("cmd /c echo 	set FwSvcExec = ws.Exec(""wmic service where name=""""SharedAccess"""" get state"")>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(10) = obj_shell.run("cmd /c echo 	FwSvcExec.StdIn.Close>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(11) = obj_shell.run("cmd /c echo 	FwSvcOut = FwSvcExec.StdOut.ReadAll>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(12) = obj_shell.run("cmd /c echo 	If InStr(FwSvcOut, ""State"")  Then>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(13) = obj_shell.run("cmd /c echo 		If InStr(FwSvcOut, ""Running"") Then>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(14) = obj_shell.run("cmd /c echo 			Wscript.Echo ""Enabled"">>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(15) = obj_shell.run("cmd /c echo 		Else>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(16) = obj_shell.run("cmd /c echo 			Wscript.Echo ""Disabled"">>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(17) = obj_shell.run("cmd /c echo 		End If>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(18) = obj_shell.run("cmd /c echo 	Else>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(19) = obj_shell.run("cmd /c echo 		Wscript.Echo ""NoFirewallWindows"">>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(20) = obj_shell.run("cmd /c echo 	End If>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(21) = obj_shell.run("cmd /c echo Else>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(22) = obj_shell.run("cmd /c echo 	On Error Resume Next>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(23) = obj_shell.run("cmd /c echo 	set objPolicy = objFirewall.LocalPolicy.CurrentProfile>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(24) = obj_shell.run("cmd /c echo 	ErrNum = Err.Number>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(25) = obj_shell.run("cmd /c echo 	On Error Goto ^0>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(26) = obj_shell.run("cmd /c echo 	If 0 ^<^> ErrNum Then>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(27) = obj_shell.run("cmd /c echo 		Wscript.Echo ""Enabled"">>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(28) = obj_shell.run("cmd /c echo 	Else>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(29) = obj_shell.run("cmd /c echo 		If True = objPolicy.FirewallEnabled Then>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(30) = obj_shell.run("cmd /c echo 			Wscript.Echo ""Enabled"">>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(31) = obj_shell.run("cmd /c echo 		Else>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(32) = obj_shell.run("cmd /c echo 			Wscript.Echo ""Disabled"">>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(33) = obj_shell.run("cmd /c echo 		End If>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(34) = obj_shell.run("cmd /c echo 	End If>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(35) = obj_shell.run("cmd /c echo End If>>%tmp%\checkfirewall.vbs", 0, True)
init_cmd(36) = obj_shell.run("cmd /c echo Set objWMIService = GetObject(""winmgmts:\\.\root\CIMV2"") > %tmp%\sharecheck.vbs", 0, True)
init_cmd(37) = obj_shell.run("cmd /c echo Set colItems = objWMIService.ExecQuery(""SELECT * FROM Win32_LogicalShareAccess"",,48) >> %tmp%\sharecheck.vbs", 0, True)
init_cmd(38) = obj_shell.run("cmd /c echo For Each objItem in colItems >> %tmp%\sharecheck.vbs", 0, True)
init_cmd(39) = obj_shell.run("cmd /c echo     If InStr(objItem.Trustee, ""S-1-1-0"") Then >> %tmp%\sharecheck.vbs", 0, True)
init_cmd(40) = obj_shell.run("cmd /c echo 		Wscript.Echo ""Everyone"" >> %tmp%\sharecheck.vbs", 0, True)
init_cmd(41) = obj_shell.run("cmd /c echo 		Exit For >> %tmp%\sharecheck.vbs", 0, True)
init_cmd(42) = obj_shell.run("cmd /c echo 	End If >> %tmp%\sharecheck.vbs", 0, True)
init_cmd(43) = obj_shell.run("cmd /c echo Next >> %tmp%\sharecheck.vbs", 0, True)

' 声明检查项中的执行命令
Dim pre_cmd_dic
set pre_cmd_dic = CreateObject("Scripting.Dictionary")

pre_cmd_dic.Add "10021", "cmd /c type %tmp%\sec.log | find /i ""PasswordComplexity ="" || echo PasswordComplexity = not config"
pre_cmd_dic.Add "10022", "cmd /c type %tmp%\sec.log | find /i ""MinimumPasswordLength ="" || echo MinimumPasswordLength = not config"
pre_cmd_dic.Add "10037", "cmd /c ""for %i in (KB4499175 KB4499180 KB4500331 KB4499149) do @type %tmp%\patch.log|@find /i ""%i"" || echo Not installed"""
pre_cmd_dic.Add "10038", "cmd /c ""for %i in (KB4012598 KB4012212 KB4012215 KB4012213) do @type %tmp%\patch.log|@find /i ""%i"" || echo Not installed"""
pre_cmd_dic.Add "10039", "cmd /c ""for %i in (KB2621440 KB2667402) do @type %tmp%\patch.log|@find /i ""%i"" || echo Not installed"""
pre_cmd_dic.Add "10049", "cmd /c ""for %i in (KB4512497 KB4512517 KB4512507 KB4512516 KB4512501 KB4511553 KB4512508 KB4512506 KB4512486 KB4512506 KB4512488 KB4512489 KB4512553) do @type %tmp%\patch.log|@find /i ""%i"" || echo Not installed"""

pre_cmd_dic.Add "10016", "cmd /c reg query ""HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp"" /v PortNumber 2>nul | find /i ""PortNumber"""
pre_cmd_dic.Add "10017", "cmd /c type %tmp%\sec.log | find /i ""NewAdministratorName ="" || echo NewAdministratorName = not config"
pre_cmd_dic.Add "10018", "cmd /c type %tmp%\sec.log | find /i ""MaximumPasswordAge ="" || echo MaximumPasswordAge = not config"
pre_cmd_dic.Add "10019", "cmd /c type %tmp%\sec.log | find /i ""PasswordHistorySize ="" || echo PasswordHistorySize = not config"
pre_cmd_dic.Add "10020", "cmd /c type %tmp%\sec.log | find /i ""LockoutDuration ="" || echo LockoutDuration = not config"
pre_cmd_dic.Add "10023", "cmd /c type %tmp%\sec.log | find /i ""ResetLockoutCount ="" || echo ResetLockoutCount = not config"
pre_cmd_dic.Add "10024", "cmd /c type %tmp%\sec.log | find /i ""LockoutBadCount ="" || echo LockoutBadCount = not config"
pre_cmd_dic.Add "10025", "cmd /c type %tmp%\sec.log | find /i ""EnableGuestAccount ="" || echo EnableGuestAccount = not config"
pre_cmd_dic.Add "10026", "cmd /c reg query ""HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"" /v AutoAdminLogon || echo AutoAdminLogon notfound"
pre_cmd_dic.Add "10027", "cmd /c type %tmp%\sec.log | find /i ""AuditLogonEvents ="" || echo AuditLogonEvents = not config"
pre_cmd_dic.Add "10028", "cmd /c wmic service where name=""wuauserv"" get state | find /i ""running"" || echo not config"
pre_cmd_dic.Add "10029", "cmd /c cscript %tmp%\checkfirewall.vbs //Nologo"
pre_cmd_dic.Add "10030", "cmd /c wmic service where displayname=""DHCP Server"" get state | find /i ""running"" || echo not config"
pre_cmd_dic.Add "10032", "cmd /c wmic service where name=""rasman"" get state | find /i ""running"" || echo not config"
pre_cmd_dic.Add "10033", "cmd /c wmic service where name=""telnet"" get state | find /i ""running"" || echo not config"
pre_cmd_dic.Add "10034", "cmd /c wmic service where name=""snmptrap"" get state | find /i ""running"" || echo not config"
pre_cmd_dic.Add "10035", "cmd /c wmic service where name=""upnphost"" get  state | find /i ""running"" || echo not config"
pre_cmd_dic.Add "10036", "cmd /c reg query ""HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\LanmanServer\Parameters"" /v AutoShareServer 2>nul && reg query ""HKEY_LOCAL_MACHINE\System\CurrentControlSet\ Services\LanmanServer\Parameters"" /v  AutoShare 2>nu  || echo not config"
pre_cmd_dic.Add "10050", "cmd /c cscript %tmp%\sharecheck.vbs //Nologo find /i ""Everyone"" || echo not config"

pre_cmd_dic.Add "10001", "cmd /c type %tmp%\sec.log | find /i ""AuditAccountManage"" || echo AuditAccountManage = not config"
pre_cmd_dic.Add "10002", "cmd /c type %tmp%\sec.log | find /i ""AuditProcessTracking"" || echo AuditProcessTracking = not config"
pre_cmd_dic.Add "10003", "cmd /c type %tmp%\sec.log | find /i ""AuditPolicyChange"" || echo AuditPolicyChange = not config"
pre_cmd_dic.Add "10004", "cmd /c type %tmp%\sec.log | find /i ""AuditAccountLogon"" || echo AuditAccountLogon = not config"
pre_cmd_dic.Add "10005", "cmd /c type %tmp%\sec.log | find /i ""AuditObjectAccess"" || echo AuditObjectAccess = not config"
pre_cmd_dic.Add "10006", "cmd /c type %tmp%\sec.log | find /i ""AuditDSAccess"" || echo AuditDSAccess = not config"
pre_cmd_dic.Add "10007", "cmd /c type %tmp%\sec.log | find /i ""AuditPrivilegeUse"" || echo AuditPrivilegeUse = not config"
pre_cmd_dic.Add "10008", "cmd /c type %tmp%\sec.log | find /i ""AuditSystemEvents"" || echo AuditSystemEvents = not config"
pre_cmd_dic.Add "10009", "cmd /c type %tmp%\sec.log | find /i ""MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters\NullSessionPipes="" || echo not config"
pre_cmd_dic.Add "10010", "cmd /c wmic nteventlog where filename=""application"" get  maxfilesize 2>nul | find /i /v ""maxfilesize"""
pre_cmd_dic.Add "10011", "cmd /c wmic nteventlog where filename=""application"" get overwriteoutdated 2>nul | find /i /v ""overwriteoutdated"""
pre_cmd_dic.Add "10012", "cmd /c wmic nteventlog where filename=""system"" get overwriteoutdated 2>nul | find /i /v ""overwriteoutdated"""
pre_cmd_dic.Add "10013", "cmd /c wmic nteventlog where filename=""system"" get  maxfilesize 2>nul | find /i /v ""maxfilesize"""
pre_cmd_dic.Add "10014", "cmd /c wmic nteventlog where filename=""security"" get  maxfilesize 2>nul | find /i /v ""maxfilesize"""
pre_cmd_dic.Add "10015", "cmd /c wmic nteventlog where filename=""security"" get overwriteoutdated 2>nul | find /i /v ""overwriteoutdated"""

pre_cmd_dic.Add "10031", "cmd /c wmic service where displayname=""DHCP Client"" get state | find /i ""running"" || echo not config"

pre_cmd_dic.Add "10048", "cmd /c wmic os get caption,csdversion,version | find /i /v ""caption"""

pre_keys = pre_cmd_dic.Keys
pre_values = pre_cmd_dic.Items

'声明附录检查项的执行命令
Dim appendix_cmd_dic
set appendix_cmd_dic = CreateObject("Scripting.Dictionary")
appendix_cmd_dic.Add "0", "cmd /c del /f/s/q %tmp%\sec.log && del /f/s/q %tmp%\patch.log && del /f/s/q %tmp%\checkfirewall.vbs && del /f/s/q %tmp%\sharecheck.vbs"
appendix_keys = appendix_cmd_dic.Keys
appendix_values = appendix_cmd_dic.Items

' 逻辑关系处理
dim NIC1, Nic, StrIP, localIp
dim appendix_keys,appendix_values,pre_keys,pre_values,i

Set NIC1 = getObject("winmgmts:").InstancesOf("Win32_NetworkAdapterConfiguration")
For Each Nic in NIC1
    if Nic.IPEnabled then
        StrIP = Nic.IPAddress(i)
        if Nic.ServiceName <> "VMnetAdapter" and Nic.ServiceName <> "VNA" and Nic.ServiceName <> "vna_ap" then
            localIp = StrIP
        end if
    end if
next

Dim curtime
curtime=Year(Date)&"-"&Month(Date)&"-"&Day(Date)
dim os

' 创建xml文件
Dim ip_uuid_xml
Dim oADO
Dim str_result

ip_uuid_xml = "c:\output.xml"
Set oADO = CreateObject("ADODB.Stream")
oADO.Charset = "utf-8"
oADO.Open
oADO.WriteText "<?xml version=""1.0"" encoding=""UTF-8""?>" &VbCrLf
oADO.WriteText "<result ip="""&localIp&""" uuid="""&uuid&""" template_time = """&template_time&""">" &VbCrLf
oADO.WriteText "    <security type=""auto"">" &VbCrLf

' 执行检查项执行命令, 并将结果存入xml文件
for i=0 to pre_cmd_dic.count -1
    oADO.WriteText "    <item flag="""&pre_keys(i)&""">" &VbCrLf
    oADO.WriteText "        <cmd info="""&curtime&""">" &VbCrLf
    oADO.WriteText "            <command><![CDATA["
    oADO.WriteText """"&pre_values(i)&"""]]> "&VbCrLf
    oADO.WriteText "            </command>" &VbCrLf
    oADO.WriteText "            <value><![CDATA["
    set str_result = obj_shell.exec(pre_values(i))
    str_result.stdin.close
    if str_result.exitcode = 0 then
        oADO.WriteText replace(str_result.stdout.readall, ">", "&gt;") &VbCrLf
    else
        oADO.WriteText "                 failed" &VbCrLf
    end if
    oADO.WriteText "            ]]></value>" &VbCrLf
    oADO.WriteText "        </cmd>" &VbCrLf
    oADO.WriteText "    </item>" &VbCrLf
next
oADO.Writetext "    </security>" &VbCrLf
oADO.Writetext "    <security type=""display"">" &VbCrLf

Dim fso, Myfile, f2
Set fso = CreateObject("Scripting.FileSystemObject")

' 执行附录检查项执行命令, 并将结果存入xml文件
for i=0 to appendix_cmd_dic.count-1
    oADO.WriteText "    <item flag="""&appendix_keys(i)&""">" &VbCrLf
    oADO.WriteText "        <cmd info="""&curtime&""">" &VbCrLf
    oADO.WriteText "            <command><![CDATA["
    oADO.WriteText """"&appendix_cmd_dic(i)&"""""]]>"&VbCrLf
    oADO.WriteText "            </command>" &VbCrLf
    oADO.WriteText "            <value><![CDATA["
    if len(appendix_values(i)) > 1000 then
        Set Myfile = fso.CreateTextFile("c:\appendix.bat", True)
        MyArray = Split(appendix_values(i), "[RRPP]", -1, 1)
        Myfile.writeline("@echo off")

        for Each line in MyArray
            Myfile.writeline(line)
        next
        Myfile.close()
        set str_result = obj_shell.exec("c:\appendix.bat")
    else
        set str_result = obj_shell.exec(appendix_values(i))
    end if
    str_result.stdin.close
    if str_result.exitcode = 0 then
            oADO.WriteText replace(str_result.stdout.readall, ">", "&gt;") &VbCrLf
    else
            oADO.WriteText "                 failed" &VbCrLf
    end if
    oADO.WriteText "            ]]></value>" &VbCrLf
    oADO.WriteText "        </cmd>" &VbCrLf
    oADO.WriteText "        </item>" &VbCrLf
next

if fso.fileexists("c:\apendix.bat") then
    set f2 = fso.getfile("c:\appendix.bat")
    f2.delete
end if

if fso.fileexists("TempWmicBatchFile.bat") then
    set f2 = fso.getfile("TempWmicBatchFile.bat")
    f2.delete
end if

oADO.Writetext "    </security>" &VbCrLf
oADO.WriteText "</result>"
oADO.SaveToFile ip_uuid_xml, 2
oADO.close
wscript.echo "DONE ALL"

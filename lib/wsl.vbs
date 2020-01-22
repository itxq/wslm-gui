If WScript.Arguments.Count <= 0 Then
    WScript.Quit
End If

bat = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\")) & WScript.Arguments(0) & ".bat"
arg = ""

If WScript.Arguments.Count > 1 Then
    arg = WScript.Arguments(1)
End If

CreateObject("WScript.Shell").Run """" & bat & """ """ & arg & """", 0, False
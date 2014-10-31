skypeSnapshotKey()
{
	WinGet, active_id, ID, A
	SendInput, !adv ; Alt+A for Call menu, d for Video, v for Video Snapshot
	WinWait, ahk_class TVideoSnapshotsForm ; wait for skype to raise the Snapshot Gallery window
	tooltip TVideoSnapshotsForm is active
	sleep 200
	;#WinActivateForce
	WinActivate, ahk_id %active_id% ; reactivate the chat window
	WinWait, ahk_id %active_id%
	sleep 500
	ToolTip
}
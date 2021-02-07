# Alfred Zoom Passcode Grabber for Google Calendar
If you spend a lot of time on Zoom, you have probably had that annoyance where you click a zoom meeting
and then have to go and copy-paste the passcode from the calendar entry.

This workflow helps automate that flow.

On the first run (defaulted by typing `zp` into Alfred), an Google authentication flow will open in the browser.
Once this is complete, the workflow will be able to read your Google Calendar.

On subsequent runs of the `zp` command, the flow will fetch the next two meetings from your calendar and try
 to extract the passcode. If it can't find a structured field for the passcode, it looks for the word "Passcode" and 6 digits after it.
 
Selecting the passcode copies it to the clipboard.

Happy to try to take any issues or pull requests, but this was just a little thing I orginally made for myself,
so please be patient if you ask for any help or changes.

Requires Python3, Alfred 3+ and the powerpack to run.

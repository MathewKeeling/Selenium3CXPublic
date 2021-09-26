# 3CX BLF Automation Tool

## What does this tool do?
This tool allows you to quickly replace entries in the BLF panels of a YeaLink branded phone in an environment that uses 3CX.

This tool could be altered to work on any YeaLink phone using an alternate phone management software with very little effort.

<b> This version features no information in it and ought to be populated with the BLF fields relevant to your extensions, information, etc. You will want to adjust key variable values in accordance with your environment.


## Why was it created?
This tool was developed as a response to the horrific reliability of the existing 3CX BLF GUI configuration page. It is neither reliable nor predictable and is a nightmare to work with. This eliminates the need to work with that interface.

#### Version 7.0 Notes: <br />
1. Now features the ability to use speed dial entries.


#### Version 6.0 Notes: <br/>
1. Made a change so that you no longer have to store the values in five separate
 CSV files. You now can just write all of your BLF fields to the single
 receptionBLF.csv and you are good to go.
2. The logic works like this: <br />
The five panels are comprised of five spans: 00-39, 40-79, 80-119, 120-159, 160-199 <br />
Those five sections have a common factor of forty.
Therefore: to access the apropriate index value for a given panel. (panels are counted by extensionPanelCounter) simply perform the following operation: <br />
(extensionPanelCounter * 40 ) + extensionPanelKeyCounter <br /> Where
extensionPanelKeyCounter represents the index of 0-39 for the particular panel. <br />

For example: suppose you wanted to supply the value for the 32nd BLF field
of the fourth panel. You would supply: (3*40)+31, which would result in 151. <br />
151 being the 32nd key on the fourth panel. (120-159, 00-39 accordingly)


#### Version 5.0 Notes: <br/>
1. Handled alerts
2. Added debug flag (debug mode does not confirm changes)
3. FIRST WORKING VERSION
4. Worked 2021/05/23 @ 12:15 - 2021/05/23 @ 1:45

#### Version 4.0 <br/>
1. This version has CSV integration
2. This can iterate over one of the extension panels.
3. All of the data accurate as of 5/23/21 is saves in the receptionBLF.csv file

Still do do: <br/>
1. Make it cycle through all five pages (need to differentiate between 40 key blocks)
2. Make it save changes

#### Version 3.50 <br/>
1. This version of code can execute all of the code required to populate the
entirety of one BLF extension panel if enough data is supplied.
2. Need to set up a loop to account for the changing of BLF Extension panels
3. Need to set up integration for a CSV file. Right now it's iterating just
2 BLF Extension Panel Keys with all indexes. It needs to be supplied 5 index
values for 40 keys for 5 extension panels
4. Worked on this from 2021/05/22 @ 10:15 - 2021/05/22 @ 13:35 &&
5. Worked on this from 2021/06/22 @ 06:15 - 2021/05/22 @ 23:02


#### Version 3.00 <br/>
1. First version with a readme.md
2. Completed the script enough to access the BLF Dsskey panel in the reception
 phone.
3. Completed pseudocode to represent cycling through the BLF panel pages to fill in information from csv
4. Completed debug loops to fill in the information <br/>

#### To do:
1. Make a mock test array to test the process.
2. import the CSV library to the python script
3. Import the datas from the CSV into the script
4. Test it
5. Prepare an excel sheet for the end user
6. Make Documentation for Technicians to use it.
7. Make it so you can drag a CSV onto the python script? <br/> </t></t>
(a) or at least make it so that the naming scheme allows automatic usage <br/>
8. Make a GUI?
9. Make an executable GUI version w/ drag, drop, excecute ability?

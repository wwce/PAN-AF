#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sys
import requests
import xml.etree.ElementTree as ET
sys.path.insert(0, '/var/dug/')
import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>IP to User-ID Mappings</title>

<style>

.titleblock {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100px;
    background-color: #e8ebeb;
}

.titleblock > .image {
    position: absolute;
    left: 15px;
    top: 15px;
    height: 100px;
}

.titleblock > .text {
    position: absolute;
    top: 40px;
    left: 43%;
    font:normal 30px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

ul {
    position: absolute;
    top: 100px;
    left: 0px;
    list-style-type: none;
    margin: 0;
    padding: 0;
    width: 150px;
    height: 100%;
    background-color: #e8ebeb;
}

li a {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

li a:hover {
    background-color: #306a89;
    color: white;
}

.response {
    position: absolute;
    top: 125px;
    left: 175px;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

</style>
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.svg" height="75px">
  </div>
  <div class="text">
    IP to User-ID Mappings
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'
#Make call to firewall to get XML user-id information
values = {'type': 'op', 'cmd': '<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

#Convert the response from the firewall to an ElementTree to parse as XML
tree = ET.fromstring(r.text)

if (tree.get('status') == "success"):
  print "<table cellpadding=5 cellspacing=0 border=1>"
  print "<tr><td>IP</td><td>User</td></tr>"
  for entry in tree.findall('./result/entry'):
    print "<tr>"
    print "<td>%s</td>" % (entry.find('ip').text, )
    print "<td>%s</td>" % (entry.find('user').text, )
    print "</tr>"
  print "</table>"
print "</div>"


print """
  </body>
  </html>
"""
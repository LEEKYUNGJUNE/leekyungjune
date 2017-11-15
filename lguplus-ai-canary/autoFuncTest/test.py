import requests
import json
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

line = ""
line_split = ""
question = ""
ref = ""
body = ""
dic = ""
data = ""
response = ""
res = ""

pass_num = 0
fail_num = 0

# URL inform
URL = 'http://front.mindslab.ai:17877/nlpapi/v1/analyze'
headers = {
        "Content-Type": "application/json",
        "x-device-token": "avc"
    }

filename = "log" + datetime.now().strftime('%Y%m%d%H%M%S') + ".txt" # current time = file create time, log20171027113015.txt
out_f = open(filename, "w") # out file create

with open("tc.txt", "r") as tc_f:
    while True:
        line = tc_f.readline()
        
        if not line.strip(): # line null check 
            break
        else:
            line_split = line.split("\t")
            question = line_split[0]
            ref = line_split[1]

        with open("body.txt", "r") as body_f:
            body = body_f.read()
            dic = json.loads(body)

            dic["query"]["utter"] = question  # utter value add

            data = json.dumps(dic, indent=4)  # dictionary -> json

            response = requests.post(URL, data=data, headers=headers)
            res = json.loads(response.content)

            if res["resCode"] == "20000000":

                if ref == res["answer"]["utter"]:
                    pass_num +=1
                    print >> out_f, "Q :" + question + "\nA :" + res["answer"]["utter"] + "\nE :" + ref + "R : PASS\n"
                else:
                    fail_num +=1
                    print >> out_f, "Q :" + question + "\nA :" + res["answer"]["utter"] + "\nE :" + ref + "R : FAIL\n"
            else:
                fail_num +=1
                print >> out_f, res["resCode"] + "R : FAIL\n"

print "====================="
print "Test Case Total : " ,pass_num+fail_num
print "PASS Case Total : " ,pass_num
print "FAIL case Total : " ,fail_num
print "=====================" 

out_f.close()

def getxml(link,user_name,user_id,job_id):
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(200, 900))
    display.start()
    import imgkit
    from poc import poc
    import traceback
    import urllib3
    import xmltodict
    import urllib.request, json
    import requests
    from PIL import Image
    result = []
    question = str(link)
    question = question.replace('https://www.wolframalpha.com/input/?i=','')
    # question = "http://api.wolframalpha.com/v2/query?appid=G3GQTR-Q4TPKG7HP4&input="+question+"&podstate=Step-by-step%20solution&format=image&ip=1.1.1.1&output=json"
    question = "input="+question+"&podstate=Step-by-step&scantimeout=20.0&podstate=Step-by-step%20solution&format=image&ip=1.1.1.1&output=json"
    print(question)
    # x = requests.get(question)
    data = poc(question)
    # url = "http://api.wolframalpha.com/v2/query?appid=G3GQTR-Q4TPKG7HP4&input="+question+"&podstate=Step-by-step%20solution&output=json"

    content = ''
    data = json.loads(data)

    if  (data['queryresult']['recalculate'] != "" and 'pods' not in data['queryresult']):
        recalc = data['queryresult']['recalculate'].replace("\/" , '/')
        x = requests.get(recalc)
        data = x.text
        print("Recalculated...")
        data = json.loads(data)
    
    try:
        for pod in data['queryresult']['pods']:
            
            result.append('<POD>')
            result.append(pod['title'])
            for subpods in pod['subpods']:
                if subpods['title'] != '':
                    result.append(subpods['title'])
                result.append(subpods['img']['src'])
        
        for a in result:
            if "https://" not in a:
                if a == '<POD>':
                    content += "<div class='bar'></div>"
                if a == 'Possible intermediate steps':
                    content += "<div><h4 style='color:#ff6c00'>Step-By-Step Solution</h4></div>"
                else:
                    content += "<div><h1>"+a+"</h1></div>"
            else:
                content += "<div><img src='"+a+"'></div>"
        html = "<html><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><style>img{border-radius:10px;box-shadow: 0px 5px 13px rgba(0,0,0,0.19), 0px 5px 7px rgba(0,0,0,0.23);border: 11px solid white;}.bar{width:100%;height:1px;background-color:#00000033;padding-bottom:0;margin-top:10px}div{width: 100%;text-align: center;font-family: Arial, Helvetica, sans-serif;padding-bottom: 10px;}h1{font-size: 20px;}</style><body>"+content+"<script src='https://code.jquery.com/jquery-3.4.1.min.js' integrity='sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=' crossorigin='anonymous'></script></body></html>"
        name = job_id+'result.html'
        jpg_name = job_id+'result.jpg'
        html_file = open(name,'w+')
        html_file.write(html)
        html_file.close()
        print('[Browser] |HTML file done|')
        options = {'width': 660, 'disable-smart-width': ''}
        imgkit.from_file(name, jpg_name, options = options)
    
    except Exception:
        name = job_id+"_no_step_by_step.png"
        jpg_name = "no_step_by_step.png"


    job_status = open('job_status.txt','r')
    if job_status.readline() != 'writing':
        job_status.close()
        job_status = open('job_status.txt','w')
        job_status.write('temp writing')
        job_status.close()
        job = open('job.txt','a')
        print('[Browser] |Job Creating|')
        job.write(str([name,user_id,link])+'\n')
        job.close()
        job_status = open('job_status.txt','w')
        job_status.write('not writing')
        job_status.close()
    display.stop()
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup


#import pprint
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/contact')
def contact():
    return render_template('/contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/logedIN')
def logedIN():
    return render_template('logedIN')


@app.route("/", methods=["POST"])
def getvalue():
    site_name = request.form['website']
    ans = output(site_name)
    if ans == -1:
        return render_template('pass.html', n="Something went wrong")
    return render_template('pass.html', n=ans)


def output(site_name):
    #site_name = input("Please Enter The Website Name : ")
    try:
        res = requests.get('https://www.whois.com/whois/'+site_name)
        website = BeautifulSoup(res.text, 'html.parser')

        res1 = requests.get('https://www.urlvoid.com/scan/'+site_name)
        website1 = BeautifulSoup(res1.text, 'html.parser')

        domainInfo = website.select('.df-label')
        domainInfo_1 = website.select('.df-value')
        domainInfo_2 = website1.select('.label')

        abc = ''
        abc = str(domainInfo_2[0])
        abc = abc.replace('<span class="label label-success">', '').replace(
            "/43</span>", '').replace('<span class="label label-danger">', '')
        abc = int(abc)

        tag = []
        tag1 = []
        res = {}
        a = ''
        for items in range(len(domainInfo)):
            a = domainInfo[items].string
            tag.append(a)
        for items in range(len(domainInfo_1)):
            a = domainInfo_1[items].string
            tag1.append(a)

        res = {tag[i]: tag1[i] for i in range(len(tag))}
        # print(res)
        a = res.get('Registered On:')
        b = res.get('Expires On:')
        x = 0
        if a != None and b != None:
            reg = int(a[:4])
            exp = int(b[:4])
            x = exp-reg

        #global points
        points = 0
        risky = ['shopiiee.com', 'white-stones.in', 'jollyfashion.in',
                 'fabricmaniaa.com', 'takesaree.com', 'assuredkart.in',
                 'republicsaleoffers.myshopify.com', 'fabricwibes.com', 'efinancetic.com',
                 'thefabricshome.com', 'thermoclassic.site', 'kasmira.in', 'amaz0n.net', '', None]

        # To check using dates : --
        def dateCheck(points):
            if res.get('Domain:') != '':
                points += 1
                if (x) <= 1:
                    pass
                else:
                    points += 1
                return points

        # To check If domain is in risky : --
        def risk(points):
            a = res.get('Domain:')
            if a in risky:
                pass
            else:
                points += 1
            return points

        # To check Validity using urlvoid : --
        def url(points, abc):
            if abc == 0:
                points += 1
            return points

        # Final condition : --

        def final(points, abc):
            ans = ''
            points = dateCheck(points)
            points = risk(points)
            points = url(points, abc)

            if points <= 1:
                ans = 'Risky'
                risky.append(res.get('Domain:'))
            elif points > 1 and points <= 3:
                ans = 'Not Safe, Browse carefully '
            elif points > 3:
                ans = 'Safe'
            else:
                print('Error')
            return ans, points
        ans = final(points, abc)
        return ans
    except:
        return -1

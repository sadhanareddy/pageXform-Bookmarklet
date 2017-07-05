from flask import Flask
from flask import request
#import urllib2
import requests as req
import bs4
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

word_list = pickle.load( open( "word_list.p", "rb" ) )
translatekey = 'trnsl.1.1.20160620T044235Z.009e3fdaf079e045.51ec20ede6d14038c2cb193de1f8891c28dfc749'
#translatekey = 'AIzaSyAPI_4zgrW00mByLPzvFslg34qTgyQ7I84'
@app.route("/phonetic-trans", methods=['POST'])
def phonetictrans():
    sentence = request.json['sentence']
    words = sentence.split()
    answer = []
    for word in words :
    	word = word.lower()
        if word in word_list:
            answer.append(word_list[word])
        else :
            answer.append(word)
	return " ".join(answer)

@app.route("/language-translive", methods=['POST'])
def languagetranslive():
    try:
        sentence = request.json['sentence']
    except:
        return "sentence parameter not passed"
    try :
        fromlang = request.json['from-language']
    except:
        return "en"
    try :
        tolang = request.json['to-language']
    except:
        return "to language not passed"

    res = req.get('https://translate.yandex.net/api/v1.5/tr/translate?key='+translatekey+'&text='+sentence+'&lang='+fromlang+'-'+tolang+'&format=plain&options=0');
    #res = req.get('https://translation.googleapis.com/language/translate/v2?key='+translatekey+'&q='+sentence+'&target='+tolang)
    soup = bs4.BeautifulSoup(res.text)
    ret = soup.text
    return ret;


#currency_key = '54f53c7dfcde68edca973db6cec90ba1'
#currency_key = 'DFyMH2R9KL29yE2OqomV1rvxpUsBQKEsATexoBhC6K3nGNH8'
#currency_key = 'vh1JmXolhfcjFhB3E9ahcbyfL6MkDjCR34Ub96XdOr5ke9NS'
currency_key = 'sVvJ10cTxzXFWCEnE7MosSsMKK5RP5hZJ5VN6BZ6OBrGXWjI'
@app.route("/currency-conversion", methods=['POST'])
def currencyconversion():
    try :
        amount = request.json['amount']
        print amount
    except:
        return "amount parameter not passed"
    try:
        from_cur = request.json['from_cur']
        print from_cur
    except:
        return "from_cur parameter not passed"
    try :
        to_cur = request.json['to_cur']
        print to_cur
    except:
        return "to_cur parameter not passed"
    #res = req.get('https://www.google.com/finance/converter?a=60&from=INR&to=UAH&meta=ei%3DrSlHWeHxI8KXuATylqUI')
    #res = req.get('http://free.currencyconverterapi.com/api/v3/convert?q='+from_cur+'_'+to_cur+'&amount='+amount)
    res =req.get('https://neutrinoapi.com/convert?user-id=sara&api-key='+currency_key+'&from-value='+amount+'&from-type='+from_cur+'&to-type='+to_cur+'&output-format=JSON')
    #res =req.get('https://www.google.com/finance/converter?a=1&from=USD&to=INR&meta=ei%3DP3hbWbDONM3AuATbqoe4Aw')
    print res
    soup = bs4.BeautifulSoup(res.text)
    ret = soup.text
    print ret
    # page = urllib2.urlopen('https://neutrinoapi.com/convert?user-id=sadhanavirupaksha&api-key='+currency_key+'&from-value='+amount+'&from-type='+from_cur+'&to-type='+to_cur+'&output-format=XML').read()
    # soup = bs4.BeautifulSoup(page, 'xml')
    # ret = soup.find('result').get_text(strip=True)
    # print ret
    return ret;
    

if __name__ == '__main__':
   app.run()
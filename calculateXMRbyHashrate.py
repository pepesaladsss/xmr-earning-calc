def simplifyHashrate(hashrate):
    from string import ascii_lowercase
    hashMultiplierDictionary = {"kh": 1000,"mh": 1000000,"gh": 1000000000,"th": 1000000000000,"ph": 1000000000000000,"eh": 1000000000000000000,"zh": 1000000000000000000000,"yh": 1000000000000000000000000}
    hashrate = hashrate.lower()
    strippedHashrate = ""
    hashIdentifier = ""
    for digit in str(hashrate):
        for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']: # Comparing with strings, can't convert to integer without properly filtering out all characters that aren't numbers
            if digit == num: strippedHashrate += digit
        if digit in ascii_lowercase or digit == "/": hashIdentifier += digit
    try:
        hashMultiplier = hashMultiplierDictionary[hashIdentifier.split('/s')[0][-2:]]
    except KeyError:
        hashMultiplier = 1 # h/s
    return float(strippedHashrate) * hashMultiplier

def getNetworkHashrate():
    from bs4 import BeautifulSoup
    from requests import get
    hashrateElement = BeautifulSoup(get('https://2miners.com/xmr-network-hashrate').text, 'lxml').select_one('#app > div.another-pools-block > div > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(2)')
    return simplifyHashrate(hashrateElement.text)

def getXMRPrice():
    from bs4 import BeautifulSoup
    from requests import get
    headers = { # Coinmarketcap was being cringe
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36"
    }
    priceElement = BeautifulSoup(get('https://coinmarketcap.com/currencies/monero/', headers=headers).text, 'lxml').select_one('#__next > div.bywovg-1.fUzJes > div > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > div.sc-16r8icm-0.eMxKgr.container > div.n78udj-0.jskEGI > div > div.sc-16r8icm-0.kjciSH.priceSection > div.sc-16r8icm-0.kjciSH.priceTitle > div')
    return priceElement.text

def getBlockReward(): 
    from datetime import datetime
    if datetime.now().year > 2022 or datetime.now().month >= 5 and datetime.now().year == 2022: return 0.6
    else: return 0.75 # Arbitrary number

def calculateEarnings_(yourHashrate, networkHashrate, blockReward, xmrPrice):
    xmrEarnings = yourHashrate / networkHashrate * 720 * blockReward
    usdEarnings = float(xmrPrice.replace('$', '')) * xmrEarnings
    return f"Approximate Earnings per 24 hours:\nXMR: {xmrEarnings}\nUSD: {usdEarnings}"
if __name__ == "__main__":
    yourHashrate = input("Your Hashrate (Include KH/s, MH/s, GH/s, etc): ")
    print(calculateEarnings_(simplifyHashrate(yourHashrate), getNetworkHashrate(), getBlockReward(), getXMRPrice()))

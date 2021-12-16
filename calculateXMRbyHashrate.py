def simplifyHashrate(hashrate):
    '''Simplifies a hashrate value into h/s for simpler calculations. Supports `kh/s`, `mh/s`, `gh/s`, `th/s`, `ph/s`, 
    `eh/s`, `zh/s`, `yh/s` being in the `hashrate` value and will calculate accordingly based on which one is within the value. 
    If none are found, it falls back to assuming `hashrate` is in h/s (multiplier value set to 1) | Returns a `float`'''
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
    '''Gets the total XMR network hashrate from `https://2miners.com/xmr-network-hashrate` and then simplifies the value to h/s using `simplifyHashrate()` | Returns a `float`'''
    from bs4 import BeautifulSoup
    from requests import get
    hashrateElement = BeautifulSoup(get('https://2miners.com/xmr-network-hashrate').text, 'lxml').select_one('#app > div.another-pools-block > div > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(2)')
    return simplifyHashrate(hashrateElement.text)

def getXMRPrice():
    '''Gets the current XMR price (in USD, not including $ in value) from `https://coinmarketcap.com/currencies/monero/` using `requests.get()` and `bs4.BeautifulSoup()` | Returns a `float`'''
    from bs4 import BeautifulSoup
    from requests import get
    headers = { # Coinmarketcap was being cringe
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36"
    }
    priceElement = BeautifulSoup(get('https://coinmarketcap.com/currencies/monero/', headers=headers).text, 'lxml').select_one('#__next > div.bywovg-1.fUzJes > div > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > div.sc-16r8icm-0.eMxKgr.container > div.n78udj-0.jskEGI > div > div.sc-16r8icm-0.kjciSH.priceSection > div.sc-16r8icm-0.kjciSH.priceTitle > div')
    return float(priceElement.text.replace('$', ''))

def getBlockReward(): 
    '''Gets the current XMR block reward. I'm unsure how to calculate this properly, so I set it to an arbitrary `0.75XMR` until May 2022 where it will be set to a fixed `0.60XMR` and won't require calculation past that point | Returns a `float`'''
    from datetime import datetime
    if datetime.now().year > 2022 or datetime.now().month >= 5 and datetime.now().year == 2022: return 0.6
    else: return 0.75 # Arbitrary number

def calculateEarnings_(yourHashrate, networkHashrate, blockReward, xmrPrice):
    xmrEarnings = yourHashrate / networkHashrate * 720 * blockReward
    usdEarnings = float(xmrPrice) * xmrEarnings
    return f"Approximate Earnings per 24 hours:\nXMR: {xmrEarnings}\nUSD: {usdEarnings}"
if __name__ == "__main__":
    yourHashrate = input("Your Hashrate (Include KH/s, MH/s, GH/s, etc): ")
    print(calculateEarnings_(simplifyHashrate(yourHashrate), getNetworkHashrate(), getBlockReward(), getXMRPrice()))

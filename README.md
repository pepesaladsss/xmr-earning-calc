# xmr-earning-calc
Calculates XMR/Monero mining earnings based on hashrate. Accepts hashrate in `h/s`, `kh/s`, `mh/s`, `gh/s`, `th/s`, `ph/s`, `zh/s`, `yh/s`

Functions within `calculateXMRbyHashrate.py` are made with compatibility with other programs in mind, with the only complication I can foresee being getNetworkHashrate() returning a
simplified hashrate value by using simplifyHashrate()

## simplifyHashrate(`hashrate`)

Simplifies a hashrate value into h/s for simpler calculations. 
Supports `kh/s`, `mh/s`, `gh/s`, `th/s`, `ph/s`, `eh/s`, `zh/s`, `yh/s` being in the `hashrate` value and will calculate accordingly based on which one is within the value. 

If none are found, it falls back to assuming `hashrate` is in h/s (multiplier value set to 1) 

Returns a `float` value of the `hashrate` value in `h/s`

## getNetworkHashrate()

Gets the total XMR network hashrate from `https://2miners.com/xmr-network-hashrate` and then simplifies the value to h/s using `simplifyHashrate()` 

Returns a `float` value of the network hashrate in `h/s`

## getXMRPrice()

Gets the current XMR price (in USD, not including $ in value) from `https://coinmarketcap.com/currencies/monero/` using `requests.get()` and `bs4.BeautifulSoup()` 

Returns a `float` value of XMR's price in USD

## getBlockReward()

Gets the current XMR block reward. 
I'm unsure how to calculate this properly, so I set it to an arbitrary `0.75XMR` until May 2022 where it will be set to a fixed `0.60XMR` and won't require calculation past that point 

Returns a `float` value of the current block reward

## calculateEarnings_(`yourHashrate`, `networkHashrate`, `blockReward`, `xmrPrice`)

Not made for external use.

Returns the calculated earnings per 24 hours while mining, calculated with the formula (credits to u/jtgrassie on Reddit): 

`xmrEarnings = yourHashrate / networkHashrate * 720 * blockReward` and `usdEarnings = xmrPrice * xmrEarnings`

`720` is the total number of blocks mined per day. XMR tries to maintain a block per 2 minutes which is `720` blocks per day. 

Returns a `string` with the format:
`"Approximate Earnings per 24 hours:\nXMR: {xmrEarnings}\nUSD: {usdEarnings}"`

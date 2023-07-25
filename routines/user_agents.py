#############################################################################
# Custom user agents list, used to present each request to the Page or API
# as request from different device
#############################################################################
import random

custom_user_agent = [
	    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; InfoPath.2; .NET CLR 3.0.04506.648)",
	    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YPC 3.2.0; .NET CLR 2.0.50727)",
	    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/6.0; .NET4.0E; .NET4.0C; InfoPath.3; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 1.1.4322)",
	    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.0.3705; .NET CLR 1.1.4322; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
	    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.2; qihu theworld)",
	    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; 2345Explorer 4.1.0.13485)",
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36 OPR/25.0.1614.63",
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_7) AppleWebKit/536.13 (KHTML, like Gecko) Chrome/33.0.2019.53 Safari/536.13",
	    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-gb; Silk/1.0.13.81_10003810) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true",
	    "Mozilla/5.0 (PlayStation 4 1.62) AppleWebKit/536.26 (KHTML, like Gecko)",
	    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22 CoolNovo/2.0.8.33",
	    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.219 Safari/537.36 qPrCUxHdnelkutH3S0dG7+oqm9s= 2014-06-16T17:37:22.885Z",
	    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1705.153 Safari/537.36 MRCHROME SOC CHANNEL_profitraf3",
	    "Mozilla/5.0 (Windows NT 5.1; rv:30.0; WUID=b52d06b9588963cc3bb4ac42909f64b7; WTB=25624) Gecko/20100101 Firefox/30.0",
	    "Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.1.3000 Chrome/30.0.1599.101 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.71 (KHTML, like Gecko) Chrome/17.0.1142.90 Safari/536.71",
	    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.220 Safari/537.36 XcEV3c9G/VOCT8hcTahP1Mxtag4= 2014-06-24T08:56:02.054Z",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.18 Safari/535.1",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.83 Safari/535.11",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1521.3 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.68 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1703.124 Safari/537.36 MRCHROME SOC CHANNEL_openpart3",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 YaBrowser/14.4.1750.13599 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Diglo/28.0.1479.314 Chrome/28.0.1479.0 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/536.73 (KHTML, like Gecko) Chrome/22.0.1559.82 Safari/536.73",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/536.74 (KHTML, like Gecko) Chrome/23.0.1465.77 Safari/536.74",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/536.81 (KHTML, like Gecko) Chrome/27.0.1079.68 Safari/536.81",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/536.9 (KHTML, like Gecko) Chrome/26.0.1463.21 Safari/536.9",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.10 (KHTML, like Gecko) Chrome/21.0.1149.14 Safari/537.10",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/29.0.1332.46 Safari/537.2",
	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/20.0.1237.36 Safari/537.32",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.49 (Edition Campaign 05)",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.72 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 AppEngine-Google; (+http://code.google.com/appengine; appid: s~girik1002)",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; ; NCLIENT50_AAP77708463121) like Gecko",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.220 Safari/537.36 Qwk/VFblQbWFur2X8UKU8CLOTbc= 2014-06-13T10:34:34.086Z",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.224 Safari/537.36 3uV/FYM1uSdGlxLEk/jBiy8aXRI= 2014-06-20T23:22:53.047Z",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1712.2 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.224 Safari/537.36 5oo6sXv4UVFBagPZ9SX2WKt+IOw= 2014-06-08T15:39:48.753Z",
	    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:24.7) Gecko/20140907 Firefox/24.7 PaleMoon/24.7.2",
	    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MASMJS; rv:11.0) like Gecko",
	    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2051.3 Safari/537.36",
	    "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/536.34 (KHTML, like Gecko) Chrome/37.0.2008.49 Safari/536.34",
	    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15 sputnik 2.5.3.132",
	    "Mozilla/5.0 (X11; Linux x86_64; T320a; fr-ca) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24",
	    "Opera/9.0 (Macintosh; Intel Mac OS X 10.6; U; en-MT) Presto/2.9.00 Version/12.61",
	    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
	    "Opera/9.80 (Windows NT 5.2; Edition Yx) Presto/2.12.388 Version/12.12",
	    "Opera/9.80 (Windows NT 6.2; WOW64; Edition Ukraine Local) Presto/2.12.388 Version/12.17"
	    ] 

def get_user_agent(num=None):
    if not num:
        return custom_user_agent[random.randint(0, len(custom_user_agent)-1)]
    return custom_user_agent[num]

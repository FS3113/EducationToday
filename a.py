def subdomainVisits(cpdomains):
    # freq = {}
    # for cp in cpdomains:
    #     l = cp.split(' ')
    #     count, name = int(l[0]), l[1]
    #     if name not in freq.keys():
    #         freq[name] = 0
    #     freq[name] += count
    # names = list(freq.keys()).copy()
    # for i in names:
    #     t = i
    #     l = t.split('.')
    #     for i in range(1, len(l)):
    #         n = '.'.join(l[i:])
    #         if n not in freq:
    #             freq[n] = 0
    #         freq[n] += freq[t]
    # ret = []
    # for name, count in freq.items():
    #     ret.append(str(count) + ' ' + name)
    # return freq
    freq = {}
    names = []
    for cp in cpdomains:
        l = cp.split(' ')
        count, name = int(l[0]), l[1]
        flag = name not in freq
        if flag:
            names.append(name)
            freq[name] = count
        else:
            freq[name] += count
    for name in names:
        l = name.split('.')
        for i in range(1, len(l)):
            n = '.'.join(l[i:])
            flag = n in freq
            if flag:
                freq[n] += freq[name]
            else:
                freq[n] = freq[name]
    ret = []
    for name, count in freq.items():
        ret.append(str(count) + ' ' + name)
    return freq


t = ["2777 nak.mkw.co","654 yaw.lmm.ca","3528 jyx.arz.us","3215 bll.hoh.network","408 tdt.zfz.network","3322 xhe.team","8342 srp.team","9259 bfo.net","3875 brk.ato.network","2531 mce.ser.com","2471 czb.us","4806 xss.dfa.co","654 yls.yjt.co","767 irh.epf.us","1501 ara.ca","243 qay.network","9103 vbo.org","6890 bfo.network","4296 xtb.jre.us","2329 vva.qay.network","9846 fuw.org","4681 lwf.ytn.network","1781 lbk.ksc.co","7464 jpd.fff.co","2740 xhe.org","4602 weq.buf.team","3055 fdy.jkx.com","5705 mqa.wsv.net","6629 vdu.bfo.team","9897 lra.uyy.org","8167 ahm.jre.team","9374 jep.ato.co","3624 vmv.epf.network","6865 thk.net","6920 tlc.dfa.us","9372 hci.jia.network","7968 gjf.network","7292 zbl.ksc.net","2862 coh.sci.net","3855 yjt.network","1387 hju.gbq.org","817 sgp.htq.co","2406 hkb.ocf.co","622 wmt.cwn.net","9172 zfz.net","1523 suq.bhp.co","9581 gqi.team","2160 hsj.epf.org","32 ulz.com","1225 lmm.ca","1137 ujs.qzi.co","5041 cdf.hwu.us","4126 lir.ajl.team","3111 gdw.team","8928 arz.org","9531 hoh.co","7344 czb.com","2715 ubt.okv.us","1110 kdd.znq.us","5729 srp.com","6122 nqk.srp.org","7193 xth.fzx.ca","3496 ytn.com","3950 xuf.network","4521 weh.bfo.us","3262 mor.ixi.us","4975 okv.com","7089 ske.yls.com","4198 xfs.okv.co","2444 vks.gxz.team","1789 xcf.zqy.ca","7392 uyy.net","3449 tfm.us","5907 zfz.us","9530 omu.network","3314 ytd.hkt.net","9523 wyv.cgl.network","4439 gtu.us","8390 zqk.network","1627 bhp.ca","3609 bhp.team","8557 uai.lfn.net","2913 ret.ych.ca","2447 ksc.com","7476 cze.yvr.net","8544 xrj.bhp.com","6129 hkt.com","8274 ulz.co","9219 tfm.ca","5016 zwv.gqi.co","5738 lar.bfo.team","3377 jkx.network","2979 bhp.org","8176 ujm.gqs.ca","84 lmm.network","3090 ycc.yjt.us","7042 btv.com","2965 gxj.org","8263 cwn.org","1873 kse.gjf.ca"]
x = {'nak.mkw.co': 2777, 'yaw.lmm.ca': 654, 'jyx.arz.us': 3528, 'bll.hoh.network': 3215, 'tdt.zfz.network': 408, 'xhe.team': 3322, 'srp.team': 8342, 'bfo.net': 9259, 'brk.ato.network': 3875, 'mce.ser.com': 2531, 'czb.us': 2471, 'xss.dfa.co': 4806, 'yls.yjt.co': 654, 'irh.epf.us': 767, 'ara.ca': 1501, 'qay.network': 2572, 'vbo.org': 9103, 'bfo.network': 6890, 'xtb.jre.us': 4296, 'vva.qay.network': 2329, 'fuw.org': 9846, 'lwf.ytn.network': 4681, 'lbk.ksc.co': 1781, 'jpd.fff.co': 7464, 'xhe.org': 2740, 'weq.buf.team': 4602, 'fdy.jkx.com': 3055, 'mqa.wsv.net': 5705, 'vdu.bfo.team': 6629, 'lra.uyy.org': 9897, 'ahm.jre.team': 8167, 'jep.ato.co': 9374, 'vmv.epf.network': 3624, 'thk.net': 6865, 'tlc.dfa.us': 6920, 'hci.jia.network': 9372, 'gjf.network': 7968, 'zbl.ksc.net': 7292, 'coh.sci.net': 2862, 'yjt.network': 3855, 'hju.gbq.org': 1387, 'sgp.htq.co': 817, 'hkb.ocf.co': 2406, 'wmt.cwn.net': 622, 'zfz.net': 9172, 'suq.bhp.co': 1523, 'gqi.team': 9581, 'hsj.epf.org': 2160, 'ulz.com': 32, 'lmm.ca': 1879, 'ujs.qzi.co': 1137, 'cdf.hwu.us': 5041, 'lir.ajl.team': 4126, 'gdw.team': 3111, 'arz.org': 8928, 'hoh.co': 9531, 'czb.com': 7344, 'ubt.okv.us': 2715, 'kdd.znq.us': 1110, 'srp.com': 5729, 'nqk.srp.org': 6122, 'xth.fzx.ca': 7193, 'ytn.com': 3496, 'xuf.network': 3950, 'weh.bfo.us': 4521, 'mor.ixi.us': 3262, 'okv.com': 4975, 'ske.yls.com': 7089, 'xfs.okv.co': 4198, 'vks.gxz.team': 2444, 'xcf.zqy.ca': 1789, 'uyy.net': 7392, 'tfm.us': 3449, 'zfz.us': 5907, 'omu.network': 9530, 'ytd.hkt.net': 3314, 'wyv.cgl.network': 9523, 'gtu.us': 4439, 'zqk.network': 8390, 'bhp.ca': 1627, 'bhp.team': 3609, 'uai.lfn.net': 8557, 'ret.ych.ca': 2913, 'ksc.com': 2447, 'cze.yvr.net': 7476, 'xrj.bhp.com': 8544, 'hkt.com': 6129, 'ulz.co': 8274, 'tfm.ca': 9219, 'zwv.gqi.co': 5016, 'lar.bfo.team': 5738, 'jkx.network': 3377, 'bhp.org': 2979, 'ujm.gqs.ca': 8176, 'lmm.network': 84, 'ycc.yjt.us': 3090, 'btv.com': 7042, 'gxj.org': 2965, 'cwn.org': 8263, 'kse.gjf.ca': 1873, 'mkw.co': 2777, 'co': 59758, 'ca': 36824, 'arz.us': 3528, 'us': 51516, 'hoh.network': 3215, 'network': 81314, 'zfz.network': 408, 'team': 59671, 'net': 68516, 'ato.network': 3875, 'ser.com': 2531, 'com': 58413, 'dfa.co': 4806, 'yjt.co': 654, 'epf.us': 767, 'org': 64390, 'jre.us': 4296, 'ytn.network': 4681, 'ksc.co': 1781, 'fff.co': 7464, 'buf.team': 4602, 'jkx.com': 3055, 'wsv.net': 5705, 'bfo.team': 12367, 'uyy.org': 9897, 'jre.team': 8167, 'ato.co': 9374, 'epf.network': 3624, 'dfa.us': 6920, 'jia.network': 9372, 'ksc.net': 7292, 'sci.net': 2862, 'gbq.org': 1387, 'htq.co': 817, 'ocf.co': 2406, 'cwn.net': 622, 'bhp.co': 1523, 'epf.org': 2160, 'qzi.co': 1137, 'hwu.us': 5041, 'ajl.team': 4126, 'okv.us': 2715, 'znq.us': 1110, 'srp.org': 6122, 'fzx.ca': 7193, 'bfo.us': 4521, 'ixi.us': 3262, 'yls.com': 7089, 'okv.co': 4198, 'gxz.team': 2444, 'zqy.ca': 1789, 'hkt.net': 3314, 'cgl.network': 9523, 'lfn.net': 8557, 'ych.ca': 2913, 'yvr.net': 7476, 'bhp.com': 8544, 'gqi.co': 5016, 'gqs.ca': 8176, 'yjt.us': 3090, 'gjf.ca': 1873}

# print(subdomainVisits(t)  == x)
print(subdomainVisits(t) == x)

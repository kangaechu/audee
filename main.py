from Audee import Audee

if __name__ == '__main__':
    sauna_iko = Audee(url='https://park.gsj.mobi/program/voice/100000061',
                      album="清水みさとの、サウナいこ？")
    sauna_iko.download()

    sauna_iko = Audee(url='https://audee.jp/program/voice/40889',
                      album="伊藤沙莉のsaireek channel")
    sauna_iko.download()

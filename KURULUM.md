# Kurulum ve Kullanim Rehberi

Bu klasordeki her sey test edildi ve calisiyor (heatmap ve info-card
render'lari gorsel olarak, ASCII donusumu de ornek bir fotografla
dogrulandi).

## 0) Onkosul: "profil reposu"

GitHub'da kullanici adinla ayni isimde bir repo olusturursan, o reponun
README.md'si profil sayfanin en ustunde gorunur.

```
gh repo create KULLANICI_ADIN --public --clone
cd KULLANICI_ADIN
```

Bu klasordeki tum dosyalari o reponun icine kopyala.

## 1) config.py'yi doldur

`config.py` icindeki `GITHUB_USERNAME` degerini kendi kullanici adinla
degistir. `INFO_CARD` sozlugu de senin icin bir baslangic taslagi -
`now` / `prev` / `stack` / `highlights` alanlarini istedigin gibi duzenle.

## 2) Python ortami

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

`rembg`, `pillow`, `opencv-python-headless` gibi kutuphaneler portre
olustururken lokalde gerekiyor.

`rembg` ilk calistiginda ~176MB'lik bir model dosyasini
(u2net.onnx, GitHub release'inden) otomatik indirir - internet baglantisi
gerekiyor, ekstra bir sey yapmana gerek yok.

## 3) Portreyi olustur (bir kere, foto degisince tekrar)

```
python scripts/prep_photo.py senin-fotografin.jpg
python scripts/make_ascii_svg.py
```

Ilk komut `source-prepped.png` uretir (arka plan silinmis, kontrasti
artirilmis, beyaz zemine oturtulmus versiyon). Ikinci komut bunu
`avi-ascii.svg` olarak yaziyor - satir satir soldan saga "yazilan"
monokrom ASCII portre.

Sonuc cok koyu/gurultulu gorunuyorsa `scripts/prep_photo.py` icindeki
`clipLimit` degerini dusur (orn. 1.5); cok soluk gorunuyorsa artir.

## 4) Info card'i olustur

```
python scripts/make_info_card.py
```

`info-card.svg` yazilir. Statik (animasyonsuz) bir onizleme icin:

```
STATIC=1 python scripts/make_info_card.py
```

## 5) README'yi yerlestir

`README.md` iki SVG'yi ortali, terminal gorunumlu bir duzende
yerlestiriyor: ascii(370) + info-card(490). Kendi tercihine gore
basliklardaki fake shell komutlarini degistirebilirsin.

## 6) Push et

```
git add -A
git commit -m "profil sanati: ascii portre + neofetch kart"
git push
```

## GitHub markdown'in bilmen gereken tuhafliklari

- Inline `style="..."` GitHub tarafindan siliniyor. Dikey bosluk icin
  tek calisan yontem `<br>` etiketleri.
- `<h1>`/`<h2>` tam genislikte bir alt cizgi cizer; bunu istemiyorsan
  `<h3>` kullan.
- JavaScript hic calismiyor, harici CSS de engelli - butun animasyon
  SVG'lerin icinde (SMIL `<animate>` / CSS `@keyframes`) olmak zorunda.
  Bu yuzden her iki script animasyonu dogrudan SVG'nin icine gomuyor.

## Ozet - dosya haritasi

| Dosya | Ne yapiyor |
|---|---|
| `config.py` | Kullanici adi, dosya yollari, info-card icerigi |
| `scripts/prep_photo.py` | Foto -> arka plan silme + kontrast + beyaz zemin |
| `scripts/make_ascii_svg.py` | Prepped foto -> kendini yazan ASCII SVG |
| `scripts/make_info_card.py` | neofetch tarzi bilgi karti SVG |
| `README.md` | Iki SVG'yi terminal gorunumlu duzende birlestirir |

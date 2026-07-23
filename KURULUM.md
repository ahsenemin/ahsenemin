# Kurulum ve Kullanim Rehberi

Bu klasordeki her sey test edildi ve calisiyor (contributions cekme scripti
gercek bir GitHub profiliyle, heatmap ve info-card render'lari gorsel olarak,
ASCII donusumu de ornek bir fotografla dogrulandi).

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

Not: `rembg`, `pillow`, `opencv-python-headless` gibi kutuphaneler sadece
portre olustururken lokalde gerekiyor. Gunluk otomasyon (GitHub Actions)
sadece `requests` + `beautifulsoup4` kullaniyor, o yuzden workflow dosyasi
bu agir kutuphaneleri kurmuyor.

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

## 5) Contribution heatmap'i olustur

```
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

Ilk komut token/auth gerektirmeden `github.com/users/<kullanici>/contributions`
adresindeki genel HTML'i cekip `data/contributions.json`'a yazar (gunluk
sayilar, seviye 0-4, ve toplam/seri istatistikleri). Ikinci komut bunu
`contrib-heatmap.svg` olarak render eder - koseden kosegen sekilde,
satir satir asagi kayarak beliren kutucuklar.

## 6) README'yi yerlestir

`README.md` zaten uc SVG'yi ortali, terminal gorunumlu bir duzende
yerlestiriyor. Genislikler hizali kalsin diye heatmap 860px = ascii(370) +
info-card(490). Kendi tercihine gore basliklardaki fake shell komutlarini
degistirebilirsin.

## 7) Push et ve Actions'i ac

```
git add -A
git commit -m "profil sanati: ascii portre + neofetch kart + heatmap"
git push
```

Repoya girdikten sonra **Actions** sekmesinden workflow'u bir kere elle
tetikle (`Run workflow` / `workflow_dispatch`) ve heatmap'in commit
edildigini dogrula. Sonrasinda her gun ~06:17 UTC'de otomatik yenilenir.

## GitHub markdown'in bilmen gereken tuhafliklari

- Inline `style="..."` GitHub tarafindan siliniyor. Dikey bosluk icin
  tek calisan yontem `<br>` etiketleri.
- `<h1>`/`<h2>` tam genislikte bir alt cizgi cizer; bunu istemiyorsan
  `<h3>` kullan.
- JavaScript hic calismiyor, harici CSS de engelli - butun animasyon
  SVG'lerin icinde (SMIL `<animate>` / CSS `@keyframes`) olmak zorunda.
  Bu yuzden her uc script animasyonu dogrudan SVG'nin icine gomuyor.

## Ozet - dosya haritasi

| Dosya | Ne yapiyor |
|---|---|
| `config.py` | Kullanici adi, dosya yollari, info-card icerigi |
| `scripts/prep_photo.py` | Foto -> arka plan silme + kontrast + beyaz zemin |
| `scripts/make_ascii_svg.py` | Prepped foto -> kendini yazan ASCII SVG |
| `scripts/make_info_card.py` | neofetch tarzi bilgi karti SVG |
| `scripts/fetch_contributions.py` | GitHub contributions HTML'ini token'siz ceker |
| `scripts/render_heatmap_svg.py` | JSON -> animasyonlu heatmap SVG |
| `.github/workflows/update-profile-art.yml` | Heatmap'i her gun otomatik yeniler |
| `README.md` | Uc SVG'yi terminal gorunumlu duzende birlestirir |

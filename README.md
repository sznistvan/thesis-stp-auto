![BME Logo](https://github.com/sznistvan/thesis-stp-auto/blob/master/inverted_bmelogo.png)
# **SZAKDOLGOZAT FELADAT**
## Szepesi-Nagy István - Mérnökinformatikus hallgató részére
### **Hálózati feszítőfák automatizált átalakítása**

A második rétegbeli feszítőfák biztosítják, hogy a lokális hálózatokban ne képződjenek átviteli hurkok. A fák pontos formája nagy hatással lehet a teljesítményre. A kialakításért felelős protokollok (STP, PVSTP, RSTP, MSTP) megfelelő beállítások mellett optimálisan választják ki a forgalmazásban részt vevő éleket, akár eltérő halmazt alkalmazva az egyes virtuális LAN-okban.

A hálózat változásához adaptálódnak az egyes fák, de ezzel már könnyen eltávolodhat a fák formája az optimumtól. A beállítások módosítása ismét megfelelő fákhoz vezethet, de ennek kézi elvégzése nem hatékony, hiszen ezt több eszközön, összhangban kell megtenni. Az eszközök programozott átkonfigurálása viszont gyorsabb megoldás nyújt, és csökkenti a hibázás esélyét is.
A hallgató feladatának a következőkre kell kiterjednie:
- Tekintse át a feszítőfa protokollokat és a fák formáját befolyásoló beállításokat.
- Javasoljon módszert, mely a VLANok topológiájának, illetve forgalmának változásakor új formát határoz meg a fákhoz. A módszer azt is határozza meg, hogy milyen beállításokkal érhető el a fák megváltoztatása.
- Dolgozzon ki folyamatot a módszer automatizált alkalmazására.
- Válasszon ki egy megfelelő automatizáló eszközt, és valósítsa meg a folyamatot.
- Tesztelje a megoldást egy illusztratív szkenárióval valós vagy virtualizált hálózatban.

*Tanszéki konzulens: Zsóka Zoltán*

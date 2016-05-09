#!/usr/bin/env python

def go(numPins=2, pinPitch=1, strPrefix="", strSuffix="", isSmd=False, hasMount=True, mountIsSmd=False, pinWidth=0, pinHeight=0, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=False, mountY=0, mountX=0, lineNY=0, lineSY=0, lineVX=0, txtRefY=0, txtValY=0, hasBoss=False, bossX=0, bossY=0, bossDia=0):
    strTitle = strPrefix + str(numPins) + strSuffix
    print "Generating " + strTitle

    fout = open("footprints.pretty/" + strTitle + ".kicad_mod", "w")
    fout.write("(module " + strTitle + " (layer F.Cu)\n")
    fout.write("  (fp_text reference REF** (at 0 " + str(txtRefY) + ") (layer F.SilkS)\n")
    fout.write("    (effects (font (size 1 1) (thickness 0.17)))\n")
    fout.write("  )\n")
    fout.write("  (fp_text value " + strTitle + " (at 0 " + str(txtValY) + ") (layer F.Fab)\n")
    fout.write("    (effects (font (size 1 1) (thickness 0.17)))\n")
    fout.write("  )\n")

    xFromFirstToLastPin = (numPins - 1) * pinPitch
    xOfFirstPin = xFromFirstToLastPin / 2
    if pinDirRev == False:
        xOfFirstPin *= -1

    for i in range(0, numPins):
        ip1 = i + 1
        ln = "  (pad " + str(ip1) + " "
        if isSmd:
            ln += "smd rect "
        else:
            ln += "thru_hole "
            if i == 0:
                ln += "rect "
            else:
                ln += "circle "
        if pinDirRev:
            x = xOfFirstPin - (pinPitch * i)
        else:
            x = xOfFirstPin + (pinPitch * i)
        ln += "(at %4.8f %4.8f) " % (x, pinY)
        if isSmd:
            ln += "(size %4.8f %4.8f) " % (pinWidth, pinHeight)
        else:
            drill = pinHeight
            padDia = pinWidth
            ln += "(size %4.8f %4.8f) (drill %4.8f) " % (padDia, padDia, drill)
        if isSmd:
            ln += "(layers F.Cu F.Paste F.Mask))\n"
        else:
            ln += "(layers *.Cu *.Mask F.SilkS))\n"
        fout.write(ln)

    if hasMount:
        if pinDirRev:
            x = xOfFirstPin + mountX
        else:
            x = xOfFirstPin - mountX

        for i in range(1, 2+1):
            ln = "  (pad M" + str(i) + " "
            if i != 1:
                x *= -1
            if mountIsSmd:
                ln += "smd rect "
            else:
                ln += "thru_hole circle "
            ln += "(at %4.8f %4.8f) " % (x, mountY)
            if mountIsSmd:
                ln += "(size %4.8f %4.8f) " % (mountWidth, mountHeight)
            else:
                drill = mountHeight
                padDia = mountWidth
                ln += "(size %4.8f %4.8f) (drill %4.8f) " % (padDia, padDia, drill)
            if mountIsSmd:
                ln += "(layers F.Cu F.Paste F.Mask))\n"
            else:
                ln += "(layers *.Cu *.Mask F.SilkS))\n"
            fout.write(ln)

    if hasBoss:
        if pinDirRev:
            x = xOfFirstPin + bossX
        else:
            x = xOfFirstPin - bossX
        if hasMount:
            ln = "(pad M3 "
        else:
            ln = "(pad M1 "
        ln += "thru_hole circle "
        ln += "(at %4.8f %4.8f) " % (x, bossY)
        ln += "(size %4.8f %4.8f) (drill %4.8f) " % (bossDia, bossDia, bossDia)
        ln += "(layers *.Cu *.Mask F.SilkS))\n"
        fout.write(ln)

    if pinDirRev:
        xMax = xOfFirstPin + lineVX
        xMin = -xMax
    else:
        xMax = -xOfFirstPin + lineVX
        xMin = -xMax
    yMin = lineNY
    yMax = lineSY

    ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMin, yMin, xMax, yMin)
    fout.write(ln)
    ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMin, yMax, xMax, yMax)
    fout.write(ln)
    ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMin, yMax, xMin, yMin)
    fout.write(ln)
    ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMax, yMax, xMax, yMin)
    fout.write(ln)
    fout.write(")\n")
    fout.close()

def makeAll(limit):
    for i in range(2, limit + 1):
        if i <= 16:
            go(numPins=i, pinPitch=2, strPrefix="CONN-JST-PH-", strSuffix="-PTH", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=1.5, pinHeight=0.7, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-2.75, lineSY=1.75, lineVX=2, txtRefY=3.5, txtValY=5.5)
            go(numPins=i, pinPitch=2, strPrefix="CONN-JST-PH-", strSuffix="-PTH-RGT", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=1.5, pinHeight=0.7, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-6, lineSY=1.5, lineVX=2, txtRefY=3.5, txtValY=5.5)
            go(numPins=i, pinPitch=2, strPrefix="CONN-JST-PH-", strSuffix="-SMD", isSmd=True, hasMount=True, mountIsSmd=True, pinWidth=1, pinHeight=5.5, mountWidth=1.6, mountHeight=3, pinY=-2.75, pinDirRev=False, mountY=-5, mountX=2.4, lineNY=-7.5, lineSY=-2.5, lineVX=1.9, txtRefY=1, txtValY=-8.6)
            go(numPins=i, pinPitch=2, strPrefix="CONN-JST-PH-", strSuffix="-SMD-RGT", isSmd=True, hasMount=True, mountIsSmd=True, pinWidth=1, pinHeight=3.5, mountWidth=1.7, mountHeight=3.5, pinY=7.3, pinDirRev=True, mountY=1.5, mountX=2.4, lineNY=7.6, lineSY=0, lineVX=1.9, txtRefY=10, txtValY=-1.1)
        if i == 2:
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=2, pinHeight=1, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-3.4, lineSY=2.4, lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5)
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH-BOSS", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=2, pinHeight=1, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-3.4, lineSY=2.4, lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5, hasBoss=True, bossX=1.6, bossY=-2, bossDia=1.1)
        else:
            if i <= 16 or i == 20:
                go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=1.8, pinHeight=0.9, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-3.4, lineSY=2.4, lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5)
            if i <= 10 or i == 12:
                go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH-BOSS", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=1.8, pinHeight=0.9, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-3.4, lineSY=2.4, lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5, hasBoss=True, bossX=1.6, bossY=-2, bossDia=1.1)
        if i == 2 or i <= 16 or i == 20:
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH-RGT", isSmd=False, hasMount=False, mountIsSmd=False, pinWidth=1.8, pinHeight=0.9, mountWidth=0, mountHeight=0, pinY=0, pinDirRev=True, mountY=0, mountX=0, lineNY=-7.6, lineSY=2.4, lineVX=(3.7-1.25), txtRefY=3.5, txtValY=5.5)
        if i == 3 or i == 4 or i == 6:
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-SMD-RGT", isSmd=True, hasMount=True, mountIsSmd=True, pinWidth=1.3, pinHeight=4.5, mountWidth=1.8, mountHeight=4, pinY=-8.75, pinDirRev=False, mountY=-2, mountX=(4.45-1.25), lineNY=-8, lineSY=0, lineVX=(5-1.25), txtRefY=-12.3, txtValY=1.7)

if __name__ == '__main__':
    makeAll(20)
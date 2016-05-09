#!/usr/bin/env python

def go(numPins=2, pinPitch=1, strPrefix="", strSuffix="", isSmd=False, pinWidth=0, pinHeight=0, pinY=0, pinDirRev=False, mountPoints=[], lineYs=[], lineVX=0, txtRefY=0, txtValY=0, bosses=[]):
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

    yMax = -999
    yMin = 999

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
        if pinY > yMax:
            yMax = pinY
        if pinY < yMin:
            yMin = pinY
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

    mcnt = 1

    for mp in mountPoints:
        if pinDirRev:
            x = xOfFirstPin + mp.x
        else:
            x = xOfFirstPin - mp.x

        for i in range(1, 2+1):
            ln = "  (pad M" + str(mcnt) + " "
            mcnt += 1
            if i != 1:
                x *= -1
            if mp.isSmd:
                ln += "smd rect "
            else:
                ln += "thru_hole circle "
            ln += "(at %4.8f %4.8f) " % (x, mp.y)
            if mp.y > yMax:
                yMax = mp.y
            if mp.y < yMin:
                yMin = mp.y
            if mp.isSmd:
                ln += "(size %4.8f %4.8f) " % (mp.width, mp.height)
            else:
                drill = mp.height
                padDia = mp.width
                ln += "(size %4.8f %4.8f) (drill %4.8f) " % (padDia, padDia, drill)
            if mp.isSmd:
                ln += "(layers F.Cu F.Paste F.Mask))\n"
            else:
                ln += "(layers *.Cu *.Mask F.SilkS))\n"
            fout.write(ln)

    for b in bosses:
        if b.alignLast == False:
            if pinDirRev:
                x = xOfFirstPin + b.x
            else:
                x = xOfFirstPin - b.x
        else:
            if pinDirRev:
                x = (-xOfFirstPin) - b.x
            else:
                x = (-xOfFirstPin) + b.x
        ln = "(pad \"\" np_thru_hole circle "
        ln += "(at %4.8f %4.8f) " % (x, b.y)
        if b.y > yMax:
            yMax = b.y
        if b.y < yMin:
            yMin = b.y
        ln += "(size %4.8f %4.8f) (drill %4.8f) " % (b.drill, b.drill, b.drill)
        ln += "(layers *.Cu *.Mask F.SilkS))\n"
        fout.write(ln)

    yMax2 = -999
    yMin2 = 999

    if pinDirRev:
        xMax = xOfFirstPin + lineVX
        xMin = -xMax
    else:
        xMax = -xOfFirstPin + lineVX
        xMin = -xMax

    for hLine in lineYs:
        if hLine > yMax2:
            yMax2 = hLine
        if hLine < yMin2:
            yMin2 = hLine
        ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMin, hLine, xMax, hLine)
        fout.write(ln)

    if len(lineYs) > 0:
        yMax = yMax2
        yMin = yMin2

    ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMin, yMax, xMin, yMin)
    fout.write(ln)
    ln = "  (fp_line (start %4.8f %4.8f) (end %4.8f %4.8f) (layer F.SilkS) (width 0.17))\n" % (xMax, yMax, xMax, yMin)
    fout.write(ln)

    fout.write(")\n")
    fout.close()

def makeJst():
    for i in range(2, 21):
        if i <= 16:
            go(numPins=i, pinPitch=2.0, strPrefix="CONN-JST-PH-", strSuffix="-PTH", isSmd=False, pinWidth=1.5, pinHeight=0.7, pinY=0, pinDirRev=True, mountPoints=[], lineYs=[-2.75, 1.75], lineVX=2, txtRefY=3.5, txtValY=5.5)
            go(numPins=i, pinPitch=2.0, strPrefix="CONN-JST-PH-", strSuffix="-PTH-RGT", isSmd=False, pinWidth=1.5, pinHeight=0.7, pinY=0, pinDirRev=True, mountPoints=[], lineYs=[-6, 1.5], lineVX=2, txtRefY=3.5, txtValY=5.5)
            go(numPins=i, pinPitch=2.0, strPrefix="CONN-JST-PH-", strSuffix="-SMD", isSmd=True, pinWidth=1, pinHeight=5.5, pinY=-2.75, pinDirRev=False, mountPoints=[MountPoint(isSmd=True, width=1.6, height=3, y=-5, x=2.4)], lineYs=[-7.5, -2.5], lineVX=1.9, txtRefY=1, txtValY=-8.6)
            go(numPins=i, pinPitch=2.0, strPrefix="CONN-JST-PH-", strSuffix="-SMD-RGT", isSmd=True, pinWidth=1, pinHeight=3.5, pinY=7.3, pinDirRev=True, mountPoints=[MountPoint(isSmd=True, width=1.7, height=3.5, y=1.5, x=2.4)], lineYs=[7.6, 0], lineVX=1.9, txtRefY=10, txtValY=-1.1)
        if i == 2:
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH", isSmd=False, pinWidth=2, pinHeight=1, pinY=0, pinDirRev=True, lineYs=[-3.4, 2.4], lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5)
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH-BOSS", isSmd=False, pinWidth=2, pinHeight=1, pinY=0, pinDirRev=True, lineYs=[-3.4, 2.4], lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5, bosses=[BossPoint(y=-2, x=1.6, alignLast=False, drill=1.1)])
        else:
            if i <= 16 or i == 20:
                go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH", isSmd=False, pinWidth=1.8, pinHeight=0.9, pinY=0, pinDirRev=True, lineYs=[-3.4, 2.4], lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5)
            if i <= 10 or i == 12:
                go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH-BOSS", isSmd=False, pinWidth=1.8, pinHeight=0.9, pinY=0, pinDirRev=True, lineYs=[-3.4, 2.4], lineVX=(3.7-1.25), txtRefY=3.5, txtValY=-4.5, bosses=[BossPoint(y=-2, x=1.6, alignLast=False, drill=1.1)])
        if i == 2 or i <= 16 or i == 20:
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-PTH-RGT", isSmd=False, pinWidth=1.8, pinHeight=0.9, pinY=0, pinDirRev=True, lineYs=[-7.6, 2.4], lineVX=(3.7-1.25), txtRefY=3.5, txtValY=5.5)
        if i == 3 or i == 4 or i == 6:
            go(numPins=i, pinPitch=2.5, strPrefix="CONN-JST-XH-", strSuffix="-SMD-RGT", isSmd=True, pinWidth=1.3, pinHeight=4.5, pinY=-8.75, pinDirRev=False, mountPoints=[MountPoint(isSmd=True, width=1.8, height=4, y=-2, x=(4.45-1.25))], lineYs=[-8, 0], lineVX=(5-1.25), txtRefY=-12.3, txtValY=1.7)
        if i == 2 or i <= 10:
            go(numPins=i, pinPitch=3.96, strPrefix="CONN-JST-VH-", strSuffix="-PTH-RGT", isSmd=False, pinWidth=3, pinHeight=1.7, pinY=0, pinDirRev=False, lineYs=[14.9, 0], lineVX=(7.86-3.96)/2, txtRefY=-2.5, txtValY=-4.5)
            go(numPins=i, pinPitch=3.96, strPrefix="CONN-JST-VH-", strSuffix="-PTH-BOSS", isSmd=False, pinWidth=3, pinHeight=1.7, pinY=0, pinDirRev=False, lineYs=[-2, -2-1.7, -2+6.8], lineVX=(7.86-3.96)/2, txtRefY=-4.7, txtValY=-6.5, bosses=[BossPoint(alignLast=False, y=-3.5, x=1.5, drill=1.4)])
        if i == 2 or i <= 11:
            go(numPins=i, pinPitch=3.96, strPrefix="CONN-JST-VH-", strSuffix="-PTH", isSmd=False, pinWidth=3, pinHeight=1.7, pinY=0, pinDirRev=False, lineYs=[-2, -2-1.7, -2+6.8], lineVX=(7.86-3.96)/2, txtRefY=-4.7, txtValY=-6.5)

def makeTe():
    for i in range(3, 6):
        go(numPins=i, pinPitch=4.2, strPrefix="CONN-TE-VALULOK-", strSuffix="-PTH-BOSS", isSmd=False, pinWidth=2.8, pinHeight=1.4, pinY=0, pinDirRev=True, lineYs=[-2.1, 2.1], lineVX=(13.8-8.4)/2, txtRefY=-4.7, txtValY=-6.5, bosses=[BossPoint(alignLast=False, y=-3.85+9.4, x=-2.1, drill=3), BossPoint(alignLast=True, y=-3.85, x=0, drill=3)])
        go(numPins=i, pinPitch=4.2, strPrefix="CONN-TE-VALULOK-", strSuffix="-PTH-RGT-BOSS", isSmd=False, pinWidth=2.8, pinHeight=1.4, pinY=0, pinDirRev=True, lineYs=[13, 0], lineVX=(13.8-8.4)/2, txtRefY=-2.7, txtValY=-4.5, bosses=[BossPoint(alignLast=False, y=7.3, x=0, drill=3), BossPoint(alignLast=True, y=7.3, x=0, drill=3)])
    for i in range(2, 13):
        go(numPins=i, pinPitch=3.0, strPrefix="CONN-TE-MICROMNL-", strSuffix="-PTH-MALE-RGT", isSmd=False, pinWidth=2.4, pinHeight=1.1, pinY=0, pinDirRev=True, mountPoints=[MountPoint(isSmd=False, width=4, height=2.5, y=4.32, x=(3.715-1.5))], lineYs=[8.92, 0], lineVX=(3.715-1.5), txtRefY=-2.7, txtValY=-4.5)

class MountPoint:
    def __init__(self, isSmd=False, width=0, height=0, y=0, x=0):
        self.isSmd = isSmd
        self.width = width
        self.height = height
        self.y = y
        self.x = x

class BossPoint:
    def __init__(self, alignLast=False, drill=0, y=0, x=0):
        self.alignLast = alignLast
        self.drill = drill
        self.y = y
        self.x = x

if __name__ == '__main__':
    makeJst()
    makeTe()
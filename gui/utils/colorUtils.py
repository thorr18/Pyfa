import wx
import math

#Brightens a color (wx.Colour), factor = [0,1]

def BrightenColor(color, factor):

    r,g,b = color
    a = color.Alpha()

    factor = min(max(factor, 0), 1)

    r+=(255-r)*factor
    b+=(255-b)*factor
    g+=(255-g)*factor

    return wx.Colour(r,g,b,a)

#Darkens a color (wx.Colour), factor = [0, 1]

def DarkenColor(color, factor):
    bkR ,bkG , bkB = color

    alpha = color.Alpha()

    factor = min(max(factor, 0), 1)
    factor = 1 - factor

    r = float(bkR * factor)
    g = float(bkG * factor)
    b = float(bkB * factor)

    r = min(max(r,0),255)
    b = min(max(b,0),255)
    g = min(max(g,0),255)

    return wx.Colour(r, g, b, alpha)


#Calculates the brightness of a color, different options

def GetBrightnessO1(color):
    r,g,b,a = color
    return (0.299*r + 0.587*g + 0.114*b)

def GetBrightnessO2(color):
    r,g,b,a = color
    return math.sqrt( 0.241 * r * r + 0.691 * g * g + 0.068 * b * b )



#Calculates a suitable color based on original color (wx.Colour), its brightness, a factor=[0,1] (darken/brighten by factor depending on calculated brightness)

def GetSuitableColor(color, factor):

    brightness = GetBrightnessO1(color)

    if brightness >129:
        factor = factor*100
        return wx.Colour.ChangeLightness(color, factor)
    else:
        factor=factor*100+100
        return wx.Colour.ChangeLightness(color, factor)



#Calculates the color between a given start and end colors, delta = [0,1]
#Colors are wx.Colour objects

def CalculateTransitionColor(startColor, endColor, delta):
    sR,sG,sB,sA = startColor
    eR,eG,eB,eA = endColor

    alphaS = startColor.Alpha()
    alphaE = endColor.Alpha()

    tR = sR + (eR - sR) *  delta
    tG = sG + (eG - sG) *  delta
    tB = sB + (eB - sB) *  delta

    return wx.Colour(tR, tG, tB, (alphaS + alphaE)/2)

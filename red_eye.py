import cv2
import numpy as np
import os
import matplotlib.colors
from math import log10, sqrt
from skimage.metrics import mean_squared_error
from skimage.metrics import structural_similarity as ssim

def fill(mask):

    fill = mask.copy()
    h, w = fill.shape[:2]
    maskTemp = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(fill, maskTemp, (0, 0), 255)
    mask2 = cv2.bitwise_not(fill)
    return mask2 | mask

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

if __name__ == '__main__':
    redeyeimg = cv2.imread("red_eyes.jpg", cv2.IMREAD_COLOR)
    comp = cv2.imread("red_eyes_comp2.jpg", cv2.IMREAD_COLOR)
    dim=(540,540)
    redeyeimg = cv2.resize(redeyeimg, dim, interpolation = cv2.INTER_AREA)
    comp = cv2.resize(comp, dim, interpolation=cv2.INTER_AREA)
    rgb_redeyeimg = cv2.cvtColor(redeyeimg, cv2.COLOR_BGR2RGB)
    redeyeimg_out = redeyeimg.copy()
    gauimg_out = redeyeimg.copy()

    eyesCascade = cv2.CascadeClassifier("haarcascade.xml")
    redeyes = eyesCascade.detectMultiScale(redeyeimg, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
    rgb_redeyeimg = eyesCascade.detectMultiScale(rgb_redeyeimg, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in redeyes:
        redeye = redeyeimg[y:y + h, x:x + w]
        rgb_redeyeimg = redeyeimg[y:y + h, x:x + w]

        r = redeye[:, :, 2]
        b = redeye[:, :, 0]
        g = redeye[:, :, 1]

        hsv_arr = matplotlib.colors.rgb_to_hsv(rgb_redeyeimg/float(255))
        hue = (360 * hsv_arr[:, :, 0])
        s = (100 * hsv_arr[:, :, 1])
        v = (100 * hsv_arr[:, :, 2])

        bg_sum = cv2.add(b, g)
        sv_sum = cv2.add(s, v)

        mask = (r > 60) & (r > bg_sum) & (s > 10.0) & (v < 70.0) & (sv_sum < 160.0) & ((15 > hue) | (hue < 345))


        mask = mask.astype(np.uint8) * 255
        mask = fill(mask)
        mask = cv2.dilate(mask, None, anchor=(0, 0), iterations=2, borderType=0, borderValue=0)


        mean = bg_sum / 2
        mask = mask.astype(np.bool)[:, :, np.newaxis]
        mean = mean[:, :, np.newaxis]

        redeye_Out = redeye.copy()
        redeye_Out = np.where(mask, mean, redeye_Out)

        gau = cv2.GaussianBlur(redeye_Out, (3, 3), cv2.BORDER_DEFAULT)

        redeyeimg_out[y:y + h, x:x + w, :] = redeye_Out
        gauimg_out[y:y + h, x:x + w, :] = gau


    cv2.imshow('Red Eyes', redeyeimg)
    cv2.imshow('Red Eyes Removed', redeyeimg_out)
    cv2.imshow('gaussian', gauimg_out)
    cv2.waitKey(0)

    directory = r'C:\Users\dhaya\Desktop\output\1'
    os.chdir(directory)

    filename1 = 'redimg.jpg'
    filename2 = 'redremoval.jpg'
    filename3 = 'redgaussian.jpg'

    cv2.imwrite(filename1, redeyeimg)
    cv2.imwrite(filename2, redeyeimg_out)
    cv2.imwrite(filename3, gauimg_out)

    value = PSNR(comp, redeyeimg_out)
    print(f"PSNR value is {value} dB")
    value = PSNR(comp, gauimg_out)
    print(f"PSNR value is {value} dB")

    print("mean squared error  is ",mean_squared_error(redeyeimg_out ,comp))
    print("mean squared error  is ",mean_squared_error(gauimg_out ,comp))

    print("SSIM value is ",ssim(redeyeimg_out, comp, data_range=comp.max() - comp.min(),multichannel=True))
    print("SSIM value is ",ssim(gauimg_out, comp, data_range=comp.max() - comp.min(), multichannel=True))


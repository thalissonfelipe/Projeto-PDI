import numpy as np
import matplotlib.pyplot as plt


def imshow(image):
    plt.imshow(image, cmap=plt.get_cmap(name='gray'))
    plt.axis('off')
    plt.show()


def plot_hist(hist):
    x = [i for i in range(len(hist))]
    plt.bar(x, height=hist, width=1.0)
    plt.show()  


def subplot_hist(hist, histeq):
    fig, axes = plt.subplots(1, 2)
    x = [i for i in range(len(hist))]

    axes[0].bar(x, height=hist, width=1.0)
    axes[1].bar(x, height=histeq, width=1.0)
    plt.show()


def subplot_img(image, it):
    fig, axes = plt.subplots(1, 2)

    axes[0].imshow(image, cmap=plt.get_cmap(name='gray'))
    axes[0].axis('off')
    axes[1].imshow(it, cmap=plt.get_cmap(name='gray'))
    axes[1].axis('off')
    plt.show()


def cumulative_distribution(hist):
    if type(hist) != 'tuple':  # 2D Grayscale Image
        x = iter(hist)
        y = [next(x)]

        for i in x:
            y.append(y[-1] + i)

        y = np.array(y)
        numerator = (y - y.min()) * 255
        denominator = y.max() - y.min()
        y = numerator / denominator
        y = y.astype('uint8')

        return y
    else:  # RGB Image
        r, g, b = hist
        xr, yg, zb = iter(r), iter(g), iter(b)
        cr, cg, cb = [next(xr)], [next(yg)], [next(zb)]

        for x, y, z in zip(r, g, b):
            cr.append(cr[-1] + x)
            cg.append(cg[-1] + y)
            cb.append(cb[-1] + z)

        cr, cg, cb = np.array(cr), np.array(cg), np.array(cb)
        nr, ng, nb = (cr-cr.min())*255, (cg-cg.min())*255, (cb-cb.min())*255
        dr, dg, db = cr.max()-cr.min(), cg.max()-cg.min(), cb.max()-cb.min()
        cr, cg, cb = (nr/dr).astype('uint8'), (ng/dg).astype('uint8'), \
                                              (nb/db).astype('uint8')

        return (cr, cg, cb)


def geometric_mean_aux(kernel):
    kernel = np.ravel(np.array(kernel, dtype=np.float64))
    result = 1
    for x in kernel:
        result *= x
        
    return result


def harmonic_mean_aux(kernel):
    kernel = np.ravel(np.array(kernel, dtype=np.float64))
    result = 0
    for x in kernel:
        if x == 0:
            return 0
        result += (1. / x)

    return result


def contraharmonic_mean_aux(kernel, Q):
    kernel = np.ravel(np.array(kernel, dtype=np.float64))
    n, d = 0, 0
    for x in kernel:
        if x == 0 and (Q + 1 < 0 or Q < 0):
            return 0
        n += np.power(x, Q+1)
        d += np.power(x, Q)

    if d == 0:
        return 0

    return n / d


def split(image):
    red = image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,2]

    return (red, green, blue)


def merge(R, G, B):
    output = np.zeros((R.shape[0], R.shape[1], 3), dtype=np.uint8)
    output[:,:,0] = R
    output[:,:,1] = G
    output[:,:,2] = B

    return output
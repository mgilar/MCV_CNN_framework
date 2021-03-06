import numpy as np
import cv2 as cv
import matplotlib
import io
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def confm_metrics2image(conf_matrix, names=None):

    nLabels = np.shape(conf_matrix)[0]

    if names == None:
        plt_names = range(nLabels)
    else:
        plt_names = names

    conf_matrix = np.asarray(conf_matrix, dtype=np.float32)

    for i in range(nLabels):
        sum_row = sum(conf_matrix[i][:])
        for j in range(nLabels):
            if sum_row == 0:
                conf_matrix[i][j] = 0
            else:
                conf_matrix[i][j] = (conf_matrix[i][j]) / float(sum_row)

    img = io.BytesIO()
    print(img)
    plt.ioff()
    plt.cla()
    plt.clf()
    plt.imshow(conf_matrix,
               interpolation='nearest',
               cmap=plt.cm.Blues,
               vmin=0.0,
               vmax=1.0)
    plt.colorbar()
    plt.title('Confusion Matrix')
    plt.xticks(range(nLabels), plt_names, rotation=90)
    ystick = list(zip(plt_names, [conf_matrix[i][i] for i in range(nLabels)]))
    ystick_str = [str(ystick[i][0]) + '(%.2f)' % ystick[i][1] for i in range(nLabels)]

    plt.yticks(range(nLabels), ystick_str)

    plt.xlabel('Prediction Label')
    plt.ylabel('True Label')

    plt.draw()
    plt.pause(0.1)
    plt.savefig(img, format='png')
    img.seek(0)

    # data = np.asarray(bytearray(img.buf), dtype=np.uint8)
    data = np.fromstring(img.getvalue(), dtype=np.uint8)
    im = cv.imdecode(data, cv.IMREAD_UNCHANGED)[:, :, 0:3]
    print('Saving confussion matrix')
    img_file_path = "/home/grupo08/M5/results/conf_matrix_image.png"
    cv.imwrite(img_file_path, im)
    return im[..., ::-1]


def save_prediction(output_path, predictions, names):
    for img in range(len(names)):
        output_file = output_path + names[img]
        cv.imwrite(output_file, np.squeeze(predictions[img], axis=2))


class EarlyStopping():
    def __init__(self, cf):
        self.cf = cf
        self.best_loss_metric = float('inf')
        self.best_metric = 0
        self.counter = 0
        self.patience = self.cf.patience
        self.stop = False

    def check(self, train_loss, val_loss=None, val_mIoU=None, val_acc=None, val_f1score=None):
        if self.cf.stop_condition == 'train_loss':
            if train_loss < self.best_loss_metric:
                self.best_loss_metric = train_loss
                self.counter = 0
            else:
                self.counter += 1
        elif self.cf.stop_condition == 'valid_loss':
            if val_loss < self.best_loss_metric:
                self.best_loss_metric = val_loss
                self.counter = 0
            else:
                self.counter += 1
        elif self.cf.stop_condition == 'valid_mIoU':
            if val_mIoU > self.best_metric:
                self.best_metric = val_mIoU
            else:
                self.counter += 1
        elif self.cf.stop_condition == 'valid_mAcc':
            if val_acc > self.best_metric:
                self.best_metric = val_acc
                self.counter = 0
            else:
                self.counter += 1
        elif self.cf.stop_condition == 'f1_score':
            if val_f1score > self.best_metric:
                self.best_metric = val_f1score
                self.counter = 0
            else:
                self.counter += 1

        if self.counter == self.patience:
            print(' Early Stopping Interruption\n')
            self.stop = True


class AverageMeter(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

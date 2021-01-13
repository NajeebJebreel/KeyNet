'''VGG11/13/16/19 in Pytorch.'''
import torch
import torch.nn as nn
import torch.nn.functional as F


cfg = {
    'VGG11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'VGG19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}


class VGG(nn.Module):
    def __init__(self, vgg_name):
        super(VGG, self).__init__()
        self.features = self._make_layers(cfg[vgg_name])
        self.classifier = nn.Linear(512, 10, bias=True)

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return F.log_softmax(out, dim=1)

    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for x in cfg:
            if x == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
                           nn.BatchNorm2d(x),
                           nn.ReLU(inplace=True)]
                in_channels = x
        layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)

class VGGWM(nn.Module):
    def __init__(self, vgg_name):
        super(VGGWM, self).__init__()
        self.features = self._make_layers(cfg[vgg_name])
        self.classifier = nn.Linear(512, 10, bias=True)
        self.wmlinear1 = nn.Linear(10, 20)
        self.wmlinear2 = nn.Linear(20, 10)
        self.wmlinear3 = nn.Linear(10, 6)

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        out2 = F.log_softmax(out, dim=1)
        out2 = self.wmlinear1(out2)
        out2 = self.wmlinear2(out2)
        out2 = self.wmlinear3(out2)
        return F.log_softmax(out, dim=1), F.log_softmax(out2, dim=1)

    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for x in cfg:
            if x == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
                           nn.BatchNorm2d(x),
                           nn.ReLU(inplace=True)]
                in_channels = x
        layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)

class VGGATCRWM(nn.Module):
    def __init__(self, vgg_name):
        super(VGGATCRWM, self).__init__()
        self.features = self._make_layers(cfg[vgg_name])
        self.classifier = nn.Linear(512, 10, bias=True)
        self.wmlinear1 = nn.Linear(10, 20)
        self.wmlinear2 = nn.Linear(20, 20)
        self.wmlinear3 = nn.Linear(20, 6)

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        out2 = F.log_softmax(out, dim=1)
        out2 = self.wmlinear1(out)
        out2 = self.wmlinear2(out2)
        out2 = self.wmlinear3(out2)
        return F.log_softmax(out, dim=1), F.log_softmax(out2, dim=1)

    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for x in cfg:
            if x == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
                           nn.BatchNorm2d(x),
                           nn.ReLU(inplace=True)]
                in_channels = x
        layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)


def test():
    model = VGG('VGG16')
    x = torch.randn(2,3,32,32)
    y = model(x)
    print(y.size())
    #print model trainable parameters

    total = 0
    print('\nTrainable parameters:')
    for name, param in model.named_parameters():
        if param.requires_grad:
            print(name, '\t', param.numel())
            total += param.numel()
    print()
    print('Total', '\t', total, "trainable parametsers")

# test()
    



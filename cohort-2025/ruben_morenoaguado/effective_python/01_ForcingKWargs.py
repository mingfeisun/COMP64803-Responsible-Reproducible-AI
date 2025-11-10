import torch
import torch.nn as nn


class VisionTransformer(nn.Module):
    def __init__(
        self,
        *,
        embed_dim=768,
        patch_size=14,
        n_layers=24,
        img_size=224,
        dropout=0.5,
        droppath=0.0
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.patch_size = patch_size
        self.n_layers = n_layers
        self.img_size = img_size
        self.dropout = dropout
        self.droppath = droppath

        assert img_size % patch_size == 0

model = VisionTransformer(patch_size=14, img_size=224)

#model = VisionTransformer(768, 14, 24, 224, 0.1, 0.0)
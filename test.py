import torch
print(torch.cuda.is_available())

print(torch.__version__)

import os
print(os.path.dirname(torch.__file__))
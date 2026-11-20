import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import matplotlib.cm as cm

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Register forward and backward hooks
        self.target_layer.register_forward_hook(self._save_activations)
        self.target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, input, output):
        self.activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor, target_class=None):
        """
        input_tensor: shape (1, 3, 224, 224)
        target_class: integer index (0, 1, or 2)
        """
        self.model.zero_grad()
        output = self.model(input_tensor)

        if target_class is None:
            target_class = output.argmax(dim=1).item()

        score = output[0, target_class]
        score.backward()

        # Global average pooling of gradients across spatial dimensions (H, W)
        # gradients shape: (1, C, H, W)
        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True) # shape (1, C, 1, 1)

        # Weighted combination of forward activation maps
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True) # shape (1, 1, H, W)

        # Apply ReLU to retain only positive influences
        cam = F.relu(cam)

        # Normalize cam to [0, 1]
        cam_min, cam_max = cam.min(), cam.max()
        if cam_max - cam_min > 1e-8:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = torch.zeros_like(cam)

        cam_np = cam.squeeze().cpu().numpy()
        return cam_np

def overlay_heatmap_on_image(original_pil_img, heatmap_np, alpha=0.45, colormap_name='jet'):
    """
    Overlays a normalized 2D heatmap on a PIL Image.
    Returns: (PIL.Image overlay, PIL.Image heatmap_colored)
    """
    # Resize heatmap to match original image dimensions
    heatmap_img = Image.fromarray(np.uint8(255 * heatmap_np)).resize(original_pil_img.size, resample=Image.Resampling.BILINEAR)
    heatmap_resized = np.array(heatmap_img) / 255.0

    # Get colormap
    cmap = cm.get_cmap(colormap_name)
    colored_heatmap = cmap(heatmap_resized)[:, :, :3] # RGB in [0, 1]
    colored_heatmap_uint8 = np.uint8(255 * colored_heatmap)

    # Convert original to RGB array
    orig_np = np.array(original_pil_img.convert("RGB")) / 255.0

    # Blend
    blended = (1 - alpha) * orig_np + alpha * colored_heatmap
    blended = np.clip(blended, 0, 1)
    blended_uint8 = np.uint8(255 * blended)

    return Image.fromarray(blended_uint8), Image.fromarray(colored_heatmap_uint8)

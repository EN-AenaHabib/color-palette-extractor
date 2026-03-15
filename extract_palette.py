import cv2
import numpy as np
from sklearn.cluster import KMeans
import gradio as gr
from collections import Counter

def extract_palette(image, n_colors=5):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    img_small = cv2.resize(img, (100,100))  # speed up clustering
    img_flat = img_small.reshape((-1,3))

    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    labels = kmeans.fit_predict(img_flat)
    counts = Counter(labels)

    total = sum(counts.values())
    palette = []
    for i, color in enumerate(kmeans.cluster_centers_):
        pct = counts[i]/total*100
        palette.append((color.astype(int), round(pct,1)))

    # Create visual palette
    palette_img = np.zeros((50, n_colors*100, 3), dtype=np.uint8)
    for i, (color, pct) in enumerate(palette):
        palette_img[:, i*100:(i+1)*100, :] = color

    return palette_img

interface = gr.Interface(
    fn=extract_palette,
    inputs=[gr.Image(type="numpy", label="Upload Image"),
            gr.Slider(1,10, value=5, label="Number of Colors")],
    outputs=gr.Image(type="numpy", label="Extracted Palette"),
    title="🎨 Color Palette Extractor",
    description="Upload any image and extract its dominant colors as a neat palette."
)

interface.launch()

import cv2
import matplotlib.pyplot as plt


def display_image(image):
    plt.figure(figsize=(12, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def save_image(image, output_path):

    cv2.imwrite(
        output_path,
        cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    )
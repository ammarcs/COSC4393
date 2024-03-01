from dip import *

class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        regions = dict()
        height, width = image.shape
        label = 1

        def dfs(x, y):
            if x < 0 or y < 0 or x >= width or y >= height or image[y, x] != 255:
                return
            image[y, x] = label
            if label not in regions:
                regions[label] = []
            regions[label].append((x, y))
            dfs(x + 1, y)
            dfs(x - 1, y)
            dfs(x, y + 1)
            dfs(x, y - 1)

        for y in range(height):
            for x in range(width):
                if image[y, x] == 255:
                    dfs(x, y)
                    label += 1

        if not regions:
            print("No regions found.")
        return regions

    def compute_statistics(self, regions):
        for region_num, region in regions.items():
            area = len(region)
            x_sum, y_sum = 0, 0
            for x, y in region:
                x_sum += x
                y_sum += y
            centroid_x = x_sum // area
            centroid_y = y_sum // area
            print(f"Region: {region_num}, Area: {area}, Centroid: ({centroid_x}, {centroid_y})")

    def mark_image_regions(self, image, regions):
        try:
            for region_num, region in regions.items():
                area = len(region)
                x_sum, y_sum = 0, 0
                for x, y in region:
                    x_sum += x
                    y_sum += y
                centroid_x = x_sum // area
                centroid_y = y_sum // area

                # Mark the centroid with an asterisk
                putText(image, "*", (centroid_x, centroid_y), FONT_HERSHEY_SIMPLEX, 1, 255, 1)

                # Write region number and area
                putText(image, f"Region: {region_num}", (centroid_x - 20, centroid_y + 20), FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
                putText(image, f"Area: {area}", (centroid_x - 20, centroid_y + 40), FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
        except Exception as e:
            print("No regions found.")
            
        return image

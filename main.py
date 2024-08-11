import numpy as np
import svgwrite
from shapely.geometry import Polygon, LineString
from shapely.affinity import rotate

def read_csv(csv_path):
    print("Reading CSV file...")
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    print("CSV file read successfully.")
    return path_XYs

def make_symmetric(paths_XYs):
    print("Regularizing and making shapes symmetric...")
    symmetric_paths = []
    
    for XYs in paths_XYs:
        for XY in XYs:
            if len(XY) < 2:
                continue
            line = LineString(XY)
            if line.is_simple:
                polygon = Polygon(line.coords)
                if polygon.is_valid:
                    symmetric_polygon = polygon.convex_hull
                    symmetric_paths.append(np.array(symmetric_polygon.exterior.coords))
                else:
                    print("Warning: Polygon is not valid.")
            else:
                print("Warning: Line is not simple.")
    
    print("Shapes made symmetric.")
    return symmetric_paths

def save_to_svg(paths_XYs, svg_path):
    print(f"Saving to SVG file: {svg_path}")
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    
    for i, path in enumerate(paths_XYs):
        path_data = []
        color = 'black'  # Define your color here
        print(f"Processing path {i}: {path}")
        
        if len(path) == 0:
            print("Warning: Empty path data, skipping.")
            continue
        
        path_data.append(f"M {path[0, 0]},{path[0, 1]}")
        for j in range(1, len(path)):
            path_data.append(f"L {path[j, 0]},{path[j, 1]}")
        path_data.append("Z")
        
        path_str = " ".join(path_data)
        print(f"Writing path data: {path_str}")
        group.add(dwg.path(d=path_str, fill='none', stroke=color, stroke_width=2))
    
    dwg.add(group)
    dwg.save()
    print(f"SVG file saved: {svg_path}")

def main(csv_path, svg_path):
    path_XYs = read_csv(csv_path)
    symmetric_paths = make_symmetric(path_XYs)
    save_to_svg(symmetric_paths, svg_path)

if __name__ == "__main__":
    csv_path = "examples/isolated.csv"  # Replace with your CSV path
    svg_path = "output.svg"  # Replace with your desired SVG output path
    main(csv_path, svg_path)

import time
from ocsmesh import Raster, Geom, Hfun, Mesh, JigsawDriver, utils
import geopandas as gpd

start_total = time.perf_counter()  # Start total execution timer

print("Starting raster and geom initialization...")
start = time.perf_counter()
raster_for_geom = Raster('gebco_2024_n13.6794_s12.2594_w74.3307_e75.3223.tif')
geom = Geom(raster_for_geom, zmax=20)
end = time.perf_counter()
print(f"Raster and geom initialization time: {end - start:.6f} seconds")

start = time.perf_counter()
raster_for_hfun = Raster('gebco_2024_n13.6794_s12.2594_w74.3307_e75.3223.tif')
end = time.perf_counter()
print(f"Raster for hfun initialization time: {end - start:.6f} seconds")

print("Initializing hfun...")
start = time.perf_counter()
hfun = Hfun(raster_for_hfun, hmin=100, hmax=8000)  # Reduced hmax for efficiency
end = time.perf_counter()
print(f"Hfun initialization time: {end - start:.6f} seconds")

print("Adding flow limiter...")
start = time.perf_counter()
hfun.add_subtidal_flow_limiter()
end = time.perf_counter()
print(f"Flow limiter addition time: {end - start:.6f} seconds")

print("Adding constant value...")
start = time.perf_counter()
hfun.add_constant_value(100, 0)
end = time.perf_counter()
print(f"Constant value addition time: {end - start:.6f} seconds")

print("Adding contours...")
start = time.perf_counter()
hfun.add_contour(0, 0.001, 100)
end = time.perf_counter()
print(f"Contour addition (0m) time: {end - start:.6f} seconds")

start = time.perf_counter()
hfun.add_contour(-10, 0.001, 200)
end = time.perf_counter()
print(f"Contour addition (-10m) time: {end - start:.6f} seconds")

end_total = time.perf_counter()
print(f"Total script execution time: {end_total - start_total:.6f} seconds")


print("Creating mesh...")
driver = JigsawDriver(geom, hfun)

print("Starting mesh generation...")
mesh = driver.run()
print("Mesh generation complete.")

# Interpolation
print("Interpolating raster data onto mesh...")
raster_for_interp = Raster('gebco_2024_n13.6794_s12.2594_w74.3307_e75.3223.tif')
list_of_rasters = [raster_for_interp]
mesh.interpolate(list_of_rasters)

# Save mesh file
output_filename = 'newmesh8.2dm'
print(f"Saving mesh to {output_filename}...")
mesh.write("newmesh8", format='2dm', overwrite=True)
print('all done')

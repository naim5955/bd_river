from fastapi import FastAPI, Query
from starlette.responses import JSONResponse
from titiler.core.factory import TilerFactory
from titiler.core.dependencies import COGReader
from titiler.application.main import app as titiler_app
from fastapi.staticfiles import StaticFiles
from typing import Optional

app = FastAPI()

# Mount TiTiler app under /cog
app.mount("/cog", titiler_app)

# Serve static GeoTIFF files under /data
app.mount("/data", StaticFiles(directory="data"), name="data")

# Create a TilerFactory instance to customize
cog_tiler = TilerFactory(reader=COGReader)

# Add a new endpoint for NDVI
@cog_tiler.router.get("/ndvi")
async def ndvi(
    url: str = Query(..., description="URL to the GeoTIFF file"),
    rescale: Optional[str] = Query("0,1", description="Rescale output"),
):
    """Calculate NDVI dynamically on 4-band COG"""
    def ndvi_calc(src_data):
        # src_data is a numpy array with shape (bands, height, width)
        # For Sentinel-like 4 band TIFF: B1=Blue(0), B2=Green(1), B3=Red(2), B4=NIR(3)
        red = src_data[2].astype("float32")
        nir = src_data[3].astype("float32")
        ndvi = (nir - red) / (nir + red + 1e-10)  # avoid division by zero
        return ndvi

    return await cog_tiler.tile(
        url=url,
        calc=ndvi_calc,
        rescale=rescale,
        band_indexes=None,  # We use custom calc, so no band indexes needed
    )

# Add a new endpoint for NDWI
@cog_tiler.router.get("/ndwi")
async def ndwi(
    url: str = Query(..., description="URL to the GeoTIFF file"),
    rescale: Optional[str] = Query("0,1", description="Rescale output"),
):
    """Calculate NDWI dynamically on 4-band COG"""
    def ndwi_calc(src_data):
        green = src_data[1].astype("float32")
        nir = src_data[3].astype("float32")
        ndwi = (green - nir) / (green + nir + 1e-10)
        return ndwi

    return await cog_tiler.tile(
        url=url,
        calc=ndwi_calc,
        rescale=rescale,
        band_indexes=None,
    )

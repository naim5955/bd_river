# Use official TiTiler image as base
FROM ghcr.io/developmentseed/titiler:latest

# Copy your local 'data' folder with GeoTIFFs into the container at /data
COPY data /data

# Set working directory (optional)
WORKDIR /data

# Run TiTiler with default command to serve /data folder on port 8000
CMD ["uvicorn", "titiler.main:app", "--host", "0.0.0.0", "--port", "8000"]

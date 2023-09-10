import os
import subprocess
import nibabel as nib
from PIL import Image

# Specify the directory containing NIfTI files
#nifti_directory = r".\Dataset2\rp_lung_msk"
nifti_directory = r".\Dataset1"

# Output directory for PNG files
output_directory = r".\convertrd_masks"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through NIfTI files in the directory
for root, dirs, files in os.walk(nifti_directory):
    for file in files:
        if file.endswith(".nii") or file.endswith(".nii.gz"):
            nifti_file_path = os.path.join(root, file)

            # Load the NIfTI file
            nifti_img = nib.load(nifti_file_path)
            nifti_data = nifti_img.get_fdata()

            # Loop through the slices and save them as PNG
            for slice_idx in range(nifti_data.shape[2]):
                slice_data = nifti_data[:, :, slice_idx]
                output_filename = os.path.join(
                    output_directory, f"{file}_{slice_idx}.png")

                # Convert and save as PNG
                img_slice = Image.fromarray(slice_data.astype('uint8'))
                img_slice.save(output_filename)

                print(
                    f"Converted {nifti_file_path} slice {slice_idx} to PNG in {output_directory}")


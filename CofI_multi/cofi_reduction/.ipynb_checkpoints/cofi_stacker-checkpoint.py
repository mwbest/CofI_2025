import numpy as np
import ast
from astropy.io import fits
from astropy.nddata import CCDData
from ccdproc import Combiner
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
# --- 1. Define input files and load them ---
# Using a list makes the code cleaner and easier to extend
# file_list = [
#     'Star_JH-21Y252/M3_0007_reduction/2d_ad_5_M3real_TARG107_3.fits',
#     'Star_JH-21Y252/M3_0008_reduction/2d_ad_5_M3real_TARG107_3.fits',
#     #'Star_JH-21Y252/M3_0009_reduction/2d_ad_4_M3real_TARG107_3.fits'
    
# ]

def get_srt_or_list(widget_value):
    cleaned_value = widget_value.strip()
    if cleaned_value.startswith('[') and cleaned_value.endswith(']'):
        try:
            return ast.literal_eval(cleaned_value)
        except (ValueError, SyntaxError):
            return cleaned_value
    else:
        return cleaned_value

def stacker():
    
    file_entry = widgets.Text(description="""Files' paths""",
                              placeholder= 'e.g [file1.fits,file2.fits,file3.fits]')
    output_file = widgets.Text(description="Output file",
                              placeholder= 'e.g. M3_TARG101')
    
    button = widgets.Button(description='Stack', button_style='success')
    output = widgets.Output() # An area to print messages
    # file_list = get_srt_or_list(file_entry.value)
    # # Open all files and store their HDULists
    # hdul_list = [fits.open(f) for f in file_list]
    
    def on_button_clicked(b):
        with output:
            clear_output(wait=True)
            file_list = get_srt_or_list(file_entry.value)
            # Open all files and store their HDULists
            hdul_list = [fits.open(f) for f in file_list]
            # Let's inspect the first one to remember the structure
            print("Original FITS Structure:")
            hdul_list[0].info()
            print("-" * 30)
            
            
            # --- 2. Prepare data for combining ---
            # We will create lists of CCDData objects for both science and sky spectra
            science_ccd_list = []
            sky_ccd_list = []
            bitmasks = []
            
            for hdul in hdul_list:
                # Science data (HDU 1 and 2)
                science_ccd = CCDData(data=hdul[1].data, 
                                      uncertainty=hdul[2].data, 
                                      unit='adu') # Using 'adu' or 'electron' might be more accurate than 'pixel'
                science_ccd_list.append(science_ccd)
            
                # Sky data (HDU 5 and 6)
                sky_ccd = CCDData(data=hdul[5].data, 
                                  uncertainty=hdul[6].data, 
                                  unit='adu')
                sky_ccd_list.append(sky_ccd)
            
                # Collect bitmasks (HDU 3)
                bitmasks.append(hdul[3].data)
            
            
            # --- 3. Perform the combining operations ---
            
            # Combine the SCIENCE spectra
            combiner_sci = Combiner(science_ccd_list)
            combined_science = combiner_sci.average_combine()
            
            # Combine the SKY spectra
            combiner_sky = Combiner(sky_ccd_list)
            combined_sky = combiner_sky.average_combine()
            
            # Combine the BITMASKS using a bitwise OR
            # This ensures a flag is set in the output if it was set in ANY input mask.
            # np.bitwise_or.reduce() applies the OR operation across the list of arrays.
            combined_mask = np.bitwise_or.reduce(bitmasks)
            
            
            # --- 4. Build the new FITS file with the original structure ---
            
            # Use the first file as a template for headers.
            template_hdul = hdul_list[0]
            
            # Create the Primary HDU. It's good practice to copy the original header.
            # We add a HISTORY card to document the stacking.
            primary_hdu = fits.PrimaryHDU(header=template_hdul[0].header)
            primary_hdu.header['HISTORY'] = 'Stacked from {} files.'.format(len(file_list))
            for f in file_list:
                primary_hdu.header['HISTORY'] = f'  - {f.split("/")[-1]}' # Add source files to history
            
            # Create the new ImageHDUs for the combined data.
            # We copy the header from the corresponding extension in the template file.
            # Note: The original data had shape (4096, 1). Combiner returns a 1D array.
            # We reshape it back to match the original dimensions.
            # The data extension in the original is unnamed but corresponds to the science flux.
            science_hdu = fits.ImageHDU(data=combined_science.data,
                                         header=template_hdul[1].header,
                                         name=template_hdul[1].name) # Name is likely ' ' or can be set to 'SCI'
            
            uncert_hdu = fits.ImageHDU(data=combined_science.uncertainty.array,
                                        header=template_hdul[2].header,
                                        name='UNCERT')
            
            bitmask_hdu = fits.ImageHDU(data=combined_mask,
                                         header=template_hdul[3].header,
                                         name='BITMASK')
            
            # The Wavelength solution is the same, so we can just copy the whole HDU.
            wave_hdu = template_hdul['WAVE']
            
            # Create the new HDUs for the combined sky.
            sky_hdu = fits.ImageHDU(data=combined_sky.data,
                                     header=template_hdul[5].header,
                                     name='SKY')
            
            skyerr_hdu = fits.ImageHDU(data=combined_sky.uncertainty.array,
                                      header=template_hdul[6].header,
                                      name='SKYERR')
            
            # --- 5. Assemble and save the final FITS file ---
            
            # Create the final HDUList in the correct order
            final_hdul = fits.HDUList([
                primary_hdu,
                science_hdu,
                uncert_hdu,
                bitmask_hdu,
                wave_hdu,
                sky_hdu,
                skyerr_hdu
            ])
            
            # Define output filename
            output_filename = f'stacked_{output_file.value}.fits'
            
            # Write to FITS file
            final_hdul.writeto(output_filename, overwrite=True)
            
            
            # --- 6. Verify the output file structure ---
            print(f"Stacked file '{output_filename}' created. Verifying structure:")
            with fits.open(output_filename) as f:
                f.info()
            
            # --- Optional: Plot and compare ---
            plt.figure(figsize=(12, 6))
            # Plot one of the original spectra
            for i in range(len(file_list)):
                plt.plot(hdul_list[i]['WAVE'].data[0], hdul_list[i][1].data[0], 
                         label=f'Original Spectrum {hdul_list[i][0].header['OBJNAME']} {i}', alpha=0.7)
            # Plot the final stacked spectrum
            plt.plot(final_hdul['WAVE'].data[0], final_hdul[1].data[0], label='Stacked Spectrum', color='black', linewidth=1.5)
            plt.title('Comparison of Original and Stacked Spectrum')
            plt.xlabel('Wavelength (Angstrom)')
            plt.ylabel('Flux (ADU)')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.show()
            
            # Close all the opened FITS files
            for hdul in hdul_list:
                hdul.close()
    
    button.on_click(on_button_clicked)
    display(widgets.HBox([file_entry,output_file,button]), output)
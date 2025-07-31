# cofi_reduction/processor.py

import os
import copy
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd
from astropy.io import fits
from pyvista import imred, stars, slitmask, image, spectra
import time

# Assuming FunctionParameterWidget is in .paramwidget and will be passed
# from .paramwidget import FunctionParameterWidget # Not needed here, will be passed as instance

# Style HTML (same as before, for buttons and dropdowns used by processor's UI)
style_html = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700&family=Roboto:wght@300;400;700&display=swap');

/* General Button Styling */
.custom-button {
    border: none;
    border-radius: 18px;
    text-align: center;
    color: #000000; 
    font-family: 'Montserrat', sans-serif;
    font-size: 14px;
    font-weight: 500;
    padding: 8px 15px; 
    margin: 2px;
    cursor: pointer;
    transition: background-color 0.25s ease-in-out, transform 0.15s ease, box-shadow 0.25s ease;
    box-shadow: 0 3px 7px rgba(0,0,0,0.25);
    letter-spacing: 0.3px;
}
.custom-button:hover {
    transform: translateY(-2px); 
    box-shadow: 0 5px 12px rgba(0,0,0,0.3);
}
.custom-button:active {
    transform: translateY(0px);
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

/* Specific button theme colors */
.custom-button.extraction-2d { background: linear-gradient(145deg, #1abc9c, #16a085); color: white; }
.custom-button.extraction-2d:hover { background: linear-gradient(145deg, #20d4ac, #19bca4); box-shadow: 0 5px 12px rgba(41, 128, 185, 0.4); }

.custom-button.extraction-1d { background: linear-gradient(145deg, #f39c12, #e67e22); color: white; }
.custom-button.extraction-1d:hover { background: linear-gradient(145deg, #f5b041, #dc7633); box-shadow: 0 5px 12px rgba(46, 204, 113, 0.4); }

.custom-button.yes { background: linear-gradient(145deg, #2ecc71, #27ae60); color: white;} 
.custom-button.yes:hover { background: linear-gradient(145deg, #58d68d, #249f56); box-shadow: 0 5px 12px rgba(25, 135, 84, 0.4); }

.custom-button.no { background: linear-gradient(145deg, #e74c3c, #c0392b); color: white;} 
.custom-button.no:hover { background: linear-gradient(145deg, #ec7063, #a93226); box-shadow: 0 5px 12px rgba(220, 53, 69, 0.4); }
.custom-button.skip { background: linear-gradient(145deg, #f39c12, #e67e22); color: white; } /* Orange for skip */
.custom-button.skip:hover { background: linear-gradient(145deg, #f5b041, #dc7633); }


/* Input fields and Dropdowns */
.custom-input, .widget-text input[type="text"] {
    background-color:  #ffffff; 
    border: 1px solid #bdc3c7; 
    border-radius: 8px;
    padding: 8px; 
    margin: 3px;
    color: #2c3e50; 
    font-family: 'Roboto', sans-serif;
    font-size: 14px; 
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
    width: auto; 
    min-width: 180px; 
}
.custom-dropdown select, .widget-dropdown select { 
    background-color:  #ffffff; 
    border: 1px solid #bdc3c7; 
    border-radius: 8px;
    padding: 8px;
    margin: 3px;
    color: #2c3e50; 
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
    width: auto; 
    min-width: 200px; 
}
.custom-input:focus, .custom-dropdown select:focus, 
.widget-text input[type="text"]:focus, .widget-dropdown select:focus {
    box-shadow: 0 0 8px rgba(52, 152, 219, 0.6); 
    border-color: #3498db; 
    outline: none;
}
.custom-input::placeholder {
    color: #7f8c8d; 
}
.widget-text label, .widget-dropdown > label, .widget-checkbox label { 
    color: var(--cofi-text-color, #000000); 
    padding-right: 5px; 
}
[data-jp-theme-light="false"] .widget-text label, 
[data-jp-theme-light="false"] .widget-dropdown > label,
[data-jp-theme-light="false"] .widget-checkbox label {
    color: var(--cofi-text-color, #e0e0e0); 
}

.widget-dropdown { 
    display: flex;
    align-items: center;
}
</style>
"""



# Display the CSS style block when the module loads
def load_style():
    display(widgets.HTML(style_html))



class CofiProcessor1:
    def __init__(self, display_1=None):
        load_style()
        self.display = display_1

    
    def checking_shift_value(self,arcec, 
                             lamp_spec_file='KOSMOS/KOSMOS_red_waves.fits',
                             shift_multiplier=-22.5):
        try:
            shift_multiplier_ = float(shift_multiplier)
        except ValueError:
            shift_multiplier_ = -22.5
        plt.figure()
        wav2=spectra.WaveCal(lamp_spec_file)
        plt.plot(wav2.spectrum[0])
        for i, arc in enumerate(arcec[0:1]) :
            shift=(arc.header['XMM']*shift_multiplier_)
            plt.plot(arc.data[19][int(shift):]*30) # *30
            print(shift)
            plt.draw()


    
    def calibrate_wavelength(self, arcec, targets, clobber, lamp_spec_file, fit_degree, shift_multiplier,
                             lamp_file_for_identify, wave_fit_degree_after_identify, identify_thresh,
                             plot_first_identify, plot_inter_identify,
                             # Parameters from identify()
                             sky=False, wav=None, wref=None, inter=False, orders=None,
                             verbose=False, rad=5, fit=True, maxshift=10000000000.0, disp=None,
                             display=None, plot=None, pixplot=False, domain=False, xmin=None, xmax=None,
                             lags_offset=50, nskip=None, rows=None):
        
        try:
            lags_offset_ = lags_offset
        except ValueError:
            lags_offset_ = 50 # Default if parsing fails

        try:
            shift_multiplier_ = float(shift_multiplier)
        except ValueError:
            shift_multiplier_ = -22.5
        
        # clobber parameter: method argument takes precedence, then param_widget, then default False
        use_clobber = clobber

        for i, (arc, targ) in enumerate(zip(arcec, targets)):
            wavname = 'CofIwav_{:s}.fits'.format(targ['ID'])
            if use_clobber or not os.path.exists(wavname):
                wav = spectra.WaveCal(lamp_spec_file)
                wav.fit(degree=fit_degree)
                nrow = arc.shape[0]
                
                shift = int(arc.header['XMM'] * shift_multiplier_)
                
                # Initial lags based on calculated shift and configured offset
                lags_initial = np.arange(shift - lags_offset_, shift + lags_offset_)

                iter_flag = True
                while iter_flag:
                    iter_flag = wav.identify(arc[nrow // 2], plot=plot_first_identify, plotinter=plot_inter_identify,
                                             lags=lags_initial, thresh=identify_thresh, # Use initial lags here
                                             file=lamp_file_for_identify)
                    # Subsequent lags after first identify attempt, as per original logic, using configured offset
                    lags_initial = np.arange(-lags_offset_, lags_offset_) 
                    if plot_first_identify or plot_inter_identify: # Close plots if they were made
                        plt.close()

                bd = np.where(wav.weights < 0.5)[0]
                print("Identified weak weights at wavelengths:", wav.waves[bd])
                wav.degree = wave_fit_degree_after_identify
                # For the second identify call, the original code doesn't specify lags.
                # Assuming it should use the refined lags_initial or default behavior of the identify method.
                # Let's use the refined lags_initial:
                wav.identify(arc, plot=plot_first_identify, nskip=nrow // 10, thresh=identify_thresh) # lags=lags_initial
                if plot_first_identify:
                    plt.close()
                wav.write(wavname)
                wav.add_wave(arc)
                if self.display is not None:
                    self.display.tv(wav.correct(arc, arc.wave[nrow // 2]))

    # Interactive 2D Extraction (Restored to original interactive logic)
    def multi_extract2d(self, red, trace, targets, imcr,
                    # --- Main control parameters ---
                    param_area=None, output=None, update_callback=None,
                    
                    # --- Trace() parameters ---
                    trace_file=None, trace_inst=None, trace_type='Polynomial1D', trace_degree=2,
                    trace_sigdegree=0, trace_pix0=0, trace_rad=5, trace_model=None, trace_sc0=None,
                    trace_rows=None, trace_transpose=False, trace_lags=None, trace_channel=None, trace_hdu=1,
                    
                    # --- extract2d() parameters ---
                    extract2d_rows=None, extract2d_buffer=0,
                    
                    # --- findpeak() parameters ---
                    findpeak_sc0=None, findpeak_width=100, findpeak_thresh=50, findpeak_sort=False,
                    findpeak_back_percentile=10, findpeak_method='linear', findpeak_smooth=5,
                    findpeak_diff=10000, findpeak_bundle=10000, findpeak_verbose=False,
                    
                    # --- skyline() parameters ---
                    skyline_thresh=50, skyline_inter=True, skyline_linear=False,
                    skyline_file='skyline.dat', skyline_rows=None, skyline_obj_rad=5): # Renamed from 
        
        # m2d_params = self.param_widget.m2d_params if self.param_widget else {}

        # # Use parameters from param_widget if available, else method defaults, else hardcoded defaults
        # _thresh = thresh if thresh is not None else m2d_params.get('thresh', 10)
        # _rad = rad if rad is not None else m2d_params.get('rad', 5)
        # _back_percentile = back_percentile if back_percentile is not None else m2d_params.get('back_percentile', 10)
        # _degree = degree if degree is not None else m2d_params.get('degree', 3)
        # _sigdegree = sigdegree if sigdegree is not None else m2d_params.get('sigdegree', 3)
        # _linear = linear if linear is not None else m2d_params.get('linear', False)

        def plot_enabled(display_obj):
            if display_obj is not None:
                display_obj.clear()
                return True
            return False
        
        def process_slitlet(o, targ, adjust_wavelength, display_obj, skyline_obj_rad, findpeak_thresh, skyline_thresh, skyline_linear):
            wav = spectra.WaveCal(f'./CofIwav_{targ["ID"]}.fits')
            orig = wav.model.c0_0
            wav.add_wave(o)
            if adjust_wavelength:
                trace1 = spectra.Trace(transpose=trace_transpose, lags=trace_lags, # lags seems hardcoded here
                                       sc0=trace_sc0, degree=trace_degree, sigdegree=trace_sigdegree) # Use configured degree/sigdegree
                trace1.rows = [0, o.data.shape[0]]
                trace1.index = [0]
                center = o.shape[0] // 2
                peak, ind = trace1.findpeak(o, thresh=findpeak_thresh, width=center, sc0= findpeak_sc0, # Use configured thresh
                                            sort=findpeak_sort, back_percentile=findpeak_back_percentile, smooth=findpeak_smooth,
                                            method=findpeak_method,verbose=findpeak_verbose, diff=findpeak_diff,bundle=findpeak_bundle
                                           )
                if skyline_rows is None:
                    nrows = o.shape[0]
                    rows = [x for x in range(nrows) if abs(x - peak[0]) > skyline_obj_rad] # Use configured rad
                else:
                    rows = skyline_rows
                print(f'Processing rows for target {targ["ID"]}:', rows)
                wav.skyline(o, thresh=skyline_thresh, rows=rows, plot=plot_enabled(display_obj),
                            linear=skyline_linear, file=skyline_file,inter=skyline_inter) # Use configured linear
                wav.add_wave(o)
                if display_obj:
                    display_obj.tv(o)
                o = wav.correct(o, o.wave[nrows // 2])
                if display_obj:
                    display_obj.tv(o)
                name = o.header["FILE"].split(".")[0]
                o.write(f'{name}_{targ["ID"]}_2d.fits')
                return wav.model.c0_0 - orig
            else:
                nrows = o.shape[0]
                o = wav.correct(o, o.wave[nrows // 2])
                name = o.header["FILE"].split(".")[0]
                o.write(f'{name}_{targ["ID"]}_not_adjusted_2d.fits')
                plt.figure()
                plt.plot(o.wave[19], o.data[19], label='Approximated spec with sky')
                plt.title('Visualization of 2D Extraction')
                plt.legend(loc='upper right')
                return None


        val1 = widgets.Dropdown(
            options=[('2D wavelength adjustment', True), ('No 2D wavelength adjustment', False)],
            value=True, # This widget is internal to method, not in FunctionParameterWidget
            description='Adjustment Choice:',
            # layout=widgets.Layout(width='250px'),
            style={'description_width': 'initial'}
        )
        # self.slits_thresh_input.add_class('custom-dropdown')
        val1.add_class('custom-dropdown')
    
        run_button_2d = widgets.Button(
            description='Extraction', 
            tooltip='Click to extract',
            # layout=widgets.Layout(width='140px'),
            style={'button_color': '#2980B9'}
        )
        run_button_2d.add_class('custom-button')
        run_button_2d.add_class('extraction-2d')

        
        def on_click_run(b):
            out = trace.extract2d(imcr, rows=skyline_rows,display=self.display,buffer=extract2d_buffer)
            adjust_wavelength = val1.value if hasattr(val1, 'value') else True
            diffs = []
            for i, (o, targ) in enumerate(zip(out, targets)):
                diff = process_slitlet(o, targ, adjust_wavelength, 
                                       self.display, skyline_obj_rad, findpeak_thresh,
                                       skyline_thresh, skyline_linear)
                if diff is not None:
                    diffs.append(diff)
            if adjust_wavelength:
                print("Wavelength shifts:", diffs)
            # self.spec2d_out = out # This was trying to set an attribute on CofiProcessor
                                  # which might be short-lived. The update_callback handles this.
            print("\nExtraction complete! spec2d output ready.\n")
            if update_callback is not None:
                update_callback(out) # Pass the 'out' variable

        run_button_2d.on_click(on_click_run)
        container = widgets.VBox([val1, run_button_2d])
        if param_area is not None:
            param_area.clear_output()
            with param_area:
                display(container)
                
        # Ensure output is handled correctly
        if output is not None:
            with output:
                print("2D spectrum extraction initiated. Use controls above.")
        else: # Fallback if no output area is provided for messages
            print("2D spectrum extraction initiated. Use controls above.")



    # def multi_extract1d(self, spec2d, thresh_sky=None, linear=None, sky_cal=None, skip=None,
    #                     degree=None, sigdegree=None, thresh=None, back_percentile=None, method=None,
    #                     file= None, plot=None, targets=None,
    #                     param_area=None, param_area_1=None, param_area_2=None, output=None):

    # Interactive 1D Extraction (Restored to original interactive logic)
    def multi_extract1d(self, spec2d_list, targets_list,
                    # --- Main control parameters ---
                    param_area=None, param_area_1=None, param_area_2=None,
                    output=None, update_callback=None, plot_spectra=True,

                    # --- spectra.Trace() class constructor parameters ---
                    trace_class_file=None, trace_class_inst=None, trace_class_type='Polynomial1D',
                    trace_class_degree=2, trace_class_sigdegree=0, trace_class_pix0=0,
                    trace_class_rad=5, trace_class_model=None, trace_class_sc0=None,
                    trace_class_rows=None, trace_class_transpose=False, trace_class_lags=None,
                    trace_class_channel=None, trace_class_hdu=1,

                    # --- findpeak() method parameters ---
                    findpeak_sc0=None, findpeak_width=100, findpeak_thresh=50, findpeak_sort=False,
                    findpeak_back_percentile=10, findpeak_method='linear', findpeak_smooth=5,
                    findpeak_diff=10000, findpeak_bundle=10000, findpeak_verbose=False,

                    # --- trace() method parameters ---
                    trace_method_sc0=None, trace_method_rad=None, trace_method_thresh=20,
                    trace_method_index=None, trace_method_skip=10, trace_method_gaussian=False,
                    trace_method_verbose=False,

                    # --- extract() method parameters ---
                    extract_back=None, extract_fit=False, extract_old=False,
                    extract_nout=None, extract_threads=0,

                    # --- skyline() method parameters ---
                    skyline_thresh=50, skyline_inter=True, skyline_linear=False,
                    skyline_file='skyline.dat', skyline_rows=None):
        
        # m1d_params = self.param_widget.m1d_params if self.param_widget else {}
        
        # _thresh_sky = thresh_sky if thresh_sky is not None else m1d_params.get('thresh_sky', 12)
        # _linear = linear if linear is not None else m1d_params.get('linear', True)
        # # Use the sky_cal from param_widget for the *default behavior* of the interactive sky_choice dropdown
        # #_initial_sky_cal_param = sky_cal if sky_cal is not None else m1d_params.get('sky_cal', False)
        # _skip = skip if skip is not None else m1d_params.get('skip', 10)
        # _degree = degree if degree is not None else m1d_params.get('degree', 3)
        # _sigdegree = sigdegree if sigdegree is not None else m1d_params.get('sigdegree', 3)
        # _thresh = thresh if thresh is not None else m1d_params.get('thresh', 10)
        # _back_percentile = back_percentile if back_percentile is not None else m1d_params.get('back_percentile', 10)
        # _method = method if method is not None else m1d_params.get('method', 'linear')
        # _file = file if file is not None else m1d_params.get('file', 'new_wave_lamp/skyline.dat')
        # _plot = plot if plot is not None else m1d_params.get('plot', True)

        sky_choice = widgets.Dropdown(
            options=[('No sky adjustment', 'no_sky'), ('Sky adjustment', 'sky')],
            value='no_sky', #if _initial_sky_cal_param else 'no_sky', # Initialize based on param
            description='1D Calibration choice:', # Clarified description
            # layout=widgets.Layout(width='240px'), # Adjusted width
            style={'description_width': 'initial'}
        )
        sky_choice.add_class('custom-dropdown')

        radius_dropdown = widgets.Dropdown(
            options=[3, 4, 5, 6, 7, 8, 9, 10, 12, 15],
            value=5,
            description='Extraction radius:',
            # layout=widgets.Layout(width='180px'),
            style={'description_width': 'initial'}
        )
        radius_dropdown.add_class('custom-dropdown')
        
        run_button_1d = widgets.Button(
            description='Run Extraction',
            tooltip='Extract 1D spectra with chosen parameters',
            # layout=widgets.Layout(width='140px'),
            style={'button_color': '#27AE60'}
        )
        run_button_1d.add_class('custom-button')
        run_button_1d.add_class('extraction-1d')

        output_area = output
        
        def on_run_extraction_click(b):
            run_button_1d.disabled = True  # prevent double-click
            rad = radius_dropdown.value
            do_sky = (sky_choice.value == 'sky')
    
            with param_area_2:
                print("--- Running 1D Extraction ---")
                print(f"Extraction radius = {rad}")
                print(f"Sky calibration = {do_sky}\n")
    
            extracted_1d_spectra = []
    
            def process_single_target(i, spec2d_slice, targ):
                trace_obj = spectra.Trace(file= trace_class_file, inst=trace_class_inst, type=trace_class_type, degree=trace_class_sigdegree, 
                                           sigdegree=trace_class_sigdegree, pix0=trace_class_pix0, rad=trace_class_rad,
                                           sc0=trace_class_sc0, transpose=trace_class_transpose, lags=trace_class_lags,)
                #     transpose=False,
                #     lags=range(-39, 39),
                #     sc0=None,
                #     degree=_degree,
                #     sigdegree=_sigdegree
                # )
                if findpeak_width is None:
                    trace_obj.rows = [0, spec2d_slice.data.shape[0]]
                    trace_obj.index = [0]
                    center = spec2d_slice.shape[0] // 2
                else:
                    center =findpeak_width
                with output_area:
                    peak, _ = trace_obj.findpeak(
                        spec2d_slice, sc0=trace_method_sc0, width=center, thresh=findpeak_thresh, sort=findpeak_sort, 
                        back_percentile=findpeak_back_percentile, method=findpeak_method, smooth=findpeak_smooth, 
                        diff=findpeak_diff, bundle=findpeak_bundle, verbose=findpeak_verbose)
                    
                    #     spec2d_slice,
                    #     thresh=_thresh,
                    #     width=center,
                    #     sort=True,
                    #     back_percentile=_back_percentile,
                    #     method=_method
                    # )
                if len(peak) == 0:
                    with param_area_2:
                        print(f"   -> No peak found for slit {i}. Skipping.")
                    next_target()
                    return
    
                # trace_obj.model = [lambda x: x * 0. + peak[0]]
                with output_area:
                    trace_obj.trace(spec2d_slice, [peak[0]], skip=trace_method_skip, gaussian=trace_method_gaussian, display=self.display,
                                    sc0=trace_method_sc0, rad=trace_method_rad, thresh=trace_method_thresh, index=trace_method_index,
                                    verbose=trace_method_verbose
                                   )
                
                    trace_obj.model = [lambda x: x * 0. + peak[0]]

                def run_extraction_and_prompt():
                    rad = radius_dropdown.value
                    if back_regions is None:
                        sky_width = rad - 5 
                        back_regions = [[-10 + (-1 * sky_width), -rad], [10 + sky_width, rad]] # [[-10, -rad], [10, rad]]
                    else:
                        back_regions = extract_back
                    with output_area:
                        spec1d = trace_obj.extract(spec2d_slice, rad=rad, back=back_regions, display=self.display,
                                                    fit=extract_fit, old=extract_old, nout=extract_nout,
                                                    threads=extract_threads
                                                  )
                    spec1d.wave = spec2d_slice.wave[peak]
    
                    # Buttons for user confirmation
                    # self.yes_button = widgets.Button(description="Yes") # button_style="success")
                    # self.no_button = widgets.Button(description="No") #button_style="danger")
                    
                    yes_button = widgets.Button(description="Yes") #, button_style="success")
                    no_button = widgets.Button(description="No") #, button_style="danger")
                    
                    yes_button.add_class('custom-button')
                    yes_button.add_class('yes')
                    
                    no_button.add_class('custom-button')
                    no_button.add_class('no')
                    
                    prompt_label = widgets.Label("Are you satisfied with the extraction?")
                    button_box = widgets.HBox([yes_button, no_button])
    
                    def on_yes(b):
                        if do_sky:
                            wavcal = spectra.WaveCal(f'./CofIwav_{targ["ID"]}.fits')
                            swav = copy.deepcopy(wavcal)
                            swav.skyline(spec1d, thresh=skyline_thresh, linear=skyline_linear, plot=_plot, rows=skyline_rows, file=skyline_file)
                            with param_area_2:
                                print("   -> Skyline calibration applied.")
                        # --- begin auto‐save block ---
                        prefix = '2d_ad' if not do_sky else '1d_ad'
                        name   = spec2d_slice.header["FILE"].split(".")[0]
                        filename = f"{prefix}_{rad}_{name}_{targ['ID']}_{i}.fits"
                        spec1d.write(filename, overwrite=True)
                        with param_area_2:
                            print(f"   -> Saved spectrum to {filename}")
                        # --- end auto‐save block ---
                        # Show plot
                        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5))
                        ax1.plot(spec1d.wave[0], spec1d.data[0], label='1D Spectrum')
                        ax1.set_title(f"1D extracted: slit {i}, rad={rad}")
                        ax1.legend(loc='upper right')
                        ax2.plot(spec1d.wave[0], spec1d.sky[0], label='Sky')
                        ax2.set_title("Sky background")
                        ax2.legend(loc='upper right')
                        plt.tight_layout()
                        plt.show()
    
                        extracted_1d_spectra.append(spec1d)
    
                        with param_area_2:
                            print("   -> Extraction complete.\n")
    
                        next_target()
    
                    def on_no(b):
                        with param_area_2:
                            print(f"Repeating extraction with new radius = {radius_dropdown.value} ...\n")
                        run_extraction_and_prompt()
    
                    yes_button.on_click(on_yes)
                    no_button.on_click(on_no)
    
                    if param_area_1:
                        param_area_1.clear_output(wait=True)
                        with param_area_1:
                            display(widgets.VBox([prompt_label, button_box]))
    
                run_extraction_and_prompt()
    
            def next_target():
                try:
                    i, spec2d_slice, targ = next(target_iter)
                    with param_area_2:
                        print(f"Extracting slit {i}, target = {targ['ID'] if 'ID' in targ else i} ...")
                    process_single_target(i, spec2d_slice, targ)
                except StopIteration:
                    with param_area_2:
                        print("✅ All 1D extractions complete!\n")
                    if param_area_1:
                        param_area_1.clear_output()
                    self.spec1d_out = extracted_1d_spectra
                    run_button_1d.disabled = False  # re-enable for future runs
    
            target_iter = iter(list(zip(range(len(spec2d)), spec2d, targets)))
            next_target()
    
        run_button_1d.on_click(on_run_extraction_click)
    
        ui_box = widgets.VBox([
            widgets.HBox([sky_choice, radius_dropdown, run_button_1d])
        ])
        if param_area:
            param_area.clear_output()
            with param_area:
                display(ui_box)
        else:
            display(ui_box)
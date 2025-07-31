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

class CofiProcessor1:
    def __init__(self, display_1=None):
        #load_style()
        self.display = display_1

    
    def checking_shift_value(self,arcec, 
                             lamp_spec_file='KOSMOS/KOSMOS_red_waves.fits',
                             shift_multiplier=-22.5,arc_line=19):
        try:
            shift_multiplier_ = float(shift_multiplier)
        except ValueError:
            shift_multiplier_ = -22.5
        plt.figure()
        wav2=spectra.WaveCal(lamp_spec_file)
        plt.plot(wav2.spectrum[0], label='Lamp Spectrum')
        # Loop through the arc data
        for i, arc in enumerate(arcec[0:1]):
            # --- The Fix is Here ---
            
            # 1. Calculate your desired shift in pixels
            # Let's use a more obvious multiplier for testing, like -50.0
            # shift_multiplier = -50.0 
            shift = int(arc.header['XMM'] * shift_multiplier)
            
            # 2. Define your Y-data
            
            y_data = arc.data[arc_line] * 30
            
            # 3. Create an X-axis and ADD the shift to it
            # This creates an array [0, 1, 2, ...] and adds the shift to every element
            x_data = np.arange(len(y_data)) + shift
            
            # 4. Plot the (shifted x) vs (y)
            plt.plot(x_data, y_data, label=f'Shifted Arc (shift={shift})')
            
            # --- Debugging Print Statements ---
            print(f"Arc {i}:")
            print(f"  Header 'XMM' value: {arc.header['XMM']}")
            print(f"  Calculated Shift: {shift} pixels")
            print("-" * 20)
        
        plt.title("Spectrum Alignment")
        plt.xlabel("Pixel Index")
        plt.ylabel("Intensity / Counts")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.draw()


    
    def calibrate_wavelength(self, arcec, targets, clobber, lamp_spec_file, fit_degree, shift_multiplier,
                             # lamp_file_for_identify,
                             wave_fit_degree_after_identify, identify_thresh,
                             # plot_first_identify, plot_inter_identify,
                             # Parameters from identify()
                             sky=False, wav=None, wref=None, inter=False, orders=None, file =None,
                             verbose=False, rad=5, fit=True, maxshift=10000000000.0, disp=None,
                             display=None, plot=None, plotinter=True, pixplot=False, domain=False, xmin=None, xmax=None,
                             lags_offset=50, nskip=None, rows=None, sampling_value=10, correcting_value=2, 
                            weight_thresh=0.5, arc_line_position=2,):
        
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
            wavname = 'CofIwav_{:s}_{:s}.fits'.format(arc.header['OBJNAME'],targ['ID'])
            if use_clobber or not os.path.exists(wavname):
                wav = spectra.WaveCal(lamp_spec_file)
                wav.fit(degree=fit_degree)
                nrow = arc.shape[0]
                
                shift = int(arc.header['XMM'] * shift_multiplier_)
                
                # Initial lags based on calculated shift and configured offset
                lags_initial = np.arange(shift - lags_offset_, shift + lags_offset_)

                iter_flag = True
                while iter_flag:
                    iter_flag = wav.identify(arc[nrow // arc_line_position], plot=plot, plotinter=plotinter,
                                             lags=lags_initial, thresh=identify_thresh,
                                             file=file,sky=sky,inter=inter,pixplot=pixplot,domain=domain,fit=fit,maxshift=maxshift,
                                             rad=rad,xmin=xmin, xmax=xmax,nskip=nskip,orders=orders,wref=wref,rows=rows,
                                            )
                                            # wav=wav
                                            # )  # Use initial lags here
                    # Subsequent lags after first identify attempt, as per original logic, using configured offset
                    lags_initial = np.arange(-lags_offset_, lags_offset_) 
                    if plot or plot: # Close plots if they were made
                        plt.close()

                bd = np.where(wav.weights < weight_thresh)[0]
                print("Identified weak weights at wavelengths:", wav.waves[bd])
                wav.degree = wave_fit_degree_after_identify
                # For the second identify call, the original code doesn't specify lags.
                # Assuming it should use the refined lags_initial or default behavior of the identify method.
                # Let's use the refined lags_initial:
                wav.identify(arc, plot=plot, nskip=nrow // sampling_value, thresh=identify_thresh) # lags=lags_initial
                if plot:
                    plt.close()
                wav.write(wavname)
                wav.add_wave(arc)
                if self.display is not None:
                    self.display.tv(wav.correct(arc, arc.wave[nrow // correcting_value]))

    def multi_extract2d(self, red, trace, targets, imcr,
                    # --- Main control parameters ---
                    param_area=None, output=None, output_2=None, update_callback=None, param_area_feedback=None,
                    
                    # --- Trace() parameters ---
                    trace_file=None, trace_inst=None, trace_type='Polynomial1D', trace_degree=2,
                    trace_sigdegree=0, trace_pix0=0, trace_rad=5, trace_model=None, trace_sc0=None,
                    trace_rows=None, trace_transpose=False, trace_lags=None, trace_channel=None, trace_hdu=1,
                    trace_spectrum=None,
                    
                    # --- extract2d() parameters ---
                    extract2d_rows=None, extract2d_buffer=0,
                    
                    # --- findpeak() parameters ---
                    findpeak_sc0=None, findpeak_width=100, findpeak_thresh=50, findpeak_sort=False,
                    findpeak_back_percentile=10, findpeak_method='linear', findpeak_smooth=5,
                    findpeak_diff=10000, findpeak_bundle=10000, findpeak_verbose=False, findpeak_plot= False,
                    
                    # --- skyline() parameters ---
                    skyline_thresh=50, skyline_inter=True, skyline_linear=False,
                    skyline_file='skyline.dat', skyline_rows=None, skyline_obj_rad=5,correcting_value=2,
                    logger=None):

        def plot_enabled(display_obj):
            if display_obj is not None:
                display_obj.clear()
                return True
            return False

        val1 = widgets.Dropdown(
            options=[('2D wavelength adjustment', True), ('No 2D wavelength adjustment', False)],
            value=True,
            description='Adjustment Choice:',
            layout=widgets.Layout(width='auto'),
            style={'description_width': 'initial'},
        )

        run_button_2d = widgets.Button(
            description='Extraction',
            tooltip='Click to extract',
            layout=widgets.Layout(width='auto'),
            style={'button_color': '#2980B9'},
        )

        if logger:
            log_params = {'Adjustment Choice': val1.value}
            logger.log_action("Science & Extraction - 2D Extract", " Setup & Run 2D Extrction", log_params)

        def on_click_run(b):
            with output_2:
                clear_output(wait=True)
                out = trace.extract2d(imcr, rows=extract2d_rows, display=self.display, buffer=extract2d_buffer)
                adjust_wavelength = val1.value if hasattr(val1, 'value') else True
                diffs = []

                target_iter = iter(list(zip(out, targets)))
                
                def next_target():
                    try:
                        o, targ = next(target_iter)
                        process_slitlet(o, targ)
                    except StopIteration:
                        if adjust_wavelength:
                            print("Wavelength shifts:", diffs)
                        print("\nExtraction complete! spec2d output ready.\n")
                        if param_area_feedback:
                            param_area_feedback.children = []
                        if update_callback is not None:
                            update_callback(out)

                def process_slitlet(o, targ):
                    wav = spectra.WaveCal(f'./CofIwav_{o.header["OBJNAME"]}_{targ["ID"]}.fits')
                    orig = wav.model.c0_0
                    wav.add_wave(o)

                    if adjust_wavelength:
                        trace1 = spectra.Trace(file=trace_file, transpose=trace_transpose, lags=trace_lags,
                                               sc0=trace_sc0, degree=trace_degree, sigdegree=trace_sigdegree,
                                               inst=trace_inst, type=trace_type, pix0=trace_pix0, rad=trace_rad,
                                               model=trace_model,rows=trace_rows, channel=trace_channel,
                                               hdu=trace_hdu, spectrum=trace_spectrum)
                        if findpeak_width is None:
                            trace1.rows = [0, o.data.shape[0]]
                            trace1.index = [0]
                            center = o.shape[0] // 2
                        else:
                            center = findpeak_width
                        peak, ind = trace1.findpeak(o, thresh=findpeak_thresh, width=center, sc0=findpeak_sc0, plot=findpeak_plot,
                                                    sort=findpeak_sort, back_percentile=findpeak_back_percentile, smooth=findpeak_smooth,
                                                    method=findpeak_method,verbose=findpeak_verbose, diff=findpeak_diff,bundle=findpeak_bundle)

                        def run_skyline_and_prompt(current_rad):
                            if skyline_rows is None:
                                nrows = o.shape[0]
                                rows = [x for x in range(nrows) if abs(x - peak[0]) > current_rad]
                            else:
                                rows = skyline_rows
                            
                            print(f'Processing rows for target {targ["ID"]} with radius {current_rad}:', rows)
                            wav.skyline(o, thresh=skyline_thresh, rows=rows, plot=plot_enabled(self.display),
                                        linear=skyline_linear, file=skyline_file, inter=skyline_inter)

                            prompt_label = widgets.Label("Are you satisfied with the skyline result?")
                            yes_button = widgets.Button(description="Yes", button_style='success')
                            no_button = widgets.Button(description="No", button_style='danger')
                            radius_dropdown = widgets.Dropdown(options=list(range(2, 16)), value=current_rad, description='New Radius:')

                            def on_yes(b_inner):
                                if param_area_feedback:
                                    param_area_feedback.children = []
                                
                                wav.add_wave(o)
                                if self.display:
                                    self.display.tv(o)
                                o_corrected = wav.correct(o, o.wave[o.shape[0] // correcting_value])
                                if self.display:
                                    self.display.tv(o_corrected)
                                name = o.header["FILE"].split(".")[0]
                                o_corrected.write(f'{name}_{targ["ID"]}_2d.fits')
                                diffs.append(wav.model.c0_0 - orig)
                                next_target()

                            def on_no(b_inner):
                                run_skyline_and_prompt(radius_dropdown.value)
                            
                            yes_button.on_click(on_yes)
                            no_button.on_click(on_no)

                            if param_area_feedback:
                                param_area_feedback.children = [widgets.VBox([prompt_label, widgets.HBox([yes_button, no_button]), radius_dropdown])]

                        run_skyline_and_prompt(skyline_obj_rad)

                    else: # Not adjust_wavelength
                        nrows = o.shape[0]
                        o_corrected = wav.correct(o, o.wave[nrows // correcting_value])
                        name = o.header["FILE"].split(".")[0]
                        o_corrected.write(f'{name}_{targ["ID"]}_not_adjusted_2d.fits')
                        plt.figure()
                        plt.plot(o_corrected.wave[19], o_corrected.data[19], label='Approximated spec with sky')
                        plt.title('Visualization of 2D Extraction')
                        plt.legend(loc='upper right')
                        next_target()
                
                next_target()

        run_button_2d.on_click(on_click_run)
        container = widgets.VBox([val1, run_button_2d],layout=widgets.Layout(border='2px solid grey'))
        if param_area is not None:
            param_area.children = [container]
                
        if output is not None:
            clear_output(wait=True)
            with output:
                print("2D spectrum extraction initiated. Use controls above.")
        else:
            print("2D spectrum extraction initiated. Use controls above.")


    # Interactive 1D Extraction (Restored to original interactive logic)
    def multi_extract1d(self, spec2d_list, targets_list,
                    # --- Main control parameters ---
                    param_area=None, param_area_1=None, param_area_2=None,
                    output=None, #plot_spectra=True,

                    # --- spectra.Trace() class constructor parameters ---
                    trace_class_file=None, trace_class_inst=None, trace_class_type='Polynomial1D',
                    trace_class_degree=2, trace_class_sigdegree=0, trace_class_pix0=0,
                    trace_class_rad=5, trace_class_model=None, trace_class_sc0=None,
                    trace_class_rows=None, trace_class_transpose=False, trace_class_lags=None,
                    trace_class_channel=None, trace_class_hdu=1, trace_class_spectrum=None,


                    # --- findpeak() method parameters ---
                    findpeak_sc0=None, findpeak_width=None, findpeak_thresh=50, findpeak_sort=False,
                    findpeak_back_percentile=10, findpeak_method='linear', findpeak_smooth=5,
                    findpeak_diff=10000, findpeak_bundle=10000, findpeak_verbose=False,findpeak_plot= False,

                    # --- trace() method parameters ---
                    trace_method_sc0=None, trace_method_rad=None, trace_method_thresh=20,
                    trace_method_index=None, trace_method_skip=10, trace_method_gaussian=False,
                    trace_method_verbose=False, trace_method_srows=None,

                    # --- extract() method parameters ---
                    # extract_back=None, 
                    extract_fit=False, extract_old=False,
                    extract_nout=None, extract_threads=0,extract_medfilt=None,
                    # sky_width_back = 10,

                    # --- skyline() method parameters ---
                    skyline_thresh=50, skyline_inter=True, skyline_linear=False,
                    skyline_file='skyline.dat', skyline_rows=None, skyline_plot=True,
                    logger=None,):

        sky_choice = widgets.Dropdown(
            options=[('No sky adjustment', 'no_sky'), ('Sky adjustment', 'sky')],
            value='no_sky', #if _initial_sky_cal_param else 'no_sky', # Initialize based on param
            description='1D Calibration choice:', # Clarified description
            # layout=widgets.Layout(width='240px'), # Adjusted width
            style={'description_width': 'initial'},
            # layout=custom_input_layout
        )
        # sky_choice.add_class('custom-dropdown')

        radius_dropdown = widgets.Dropdown(
            options=[3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15],
            value=5,
            description='Extraction radius:',
            # layout=widgets.Layout(width='180px'),
            style={'description_width': 'initial'},
            # layout=custom_input_layout
        )
        # radius_dropdown.add_class('custom-dropdown')
        extract1d_back_input = widgets.IntText(value=10, description='Bkg. Regions:', 
                                                    placeholder='e.g., [[-15,-7],[7,15]]',
                                                style={'description_width': 'initial'})
        
        run_button_1d = widgets.Button(
            description='Run Extraction',
            tooltip='Extract 1D spectra with chosen parameters',
            # layout=widgets.Layout(width='140px'),
            style={'button_color': '#27AE60'}
        )
        # run_button_1d.add_class('custom-button')
        # run_button_1d.add_class('extraction-1d')

        output_area = output
        
        def on_run_extraction_click(b):
            run_button_1d.disabled = True  # prevent double-click
            rad = radius_dropdown.value
            extract_back = extract1d_back_input.value
            do_sky = (sky_choice.value == 'sky')
    
            with param_area_2:
                print("--- Running 1D Extraction ---")
                print(f"Extraction radius = {rad}")
                print(f"Sky calibration = {do_sky}\n")
    
            extracted_1d_spectra = []

            def process_single_target(i, spec2d_slice, targ):
                
                log_params = {
                    f'{targ['ID']}_rad': radius_dropdown.value,
                    f'{targ['ID']}_Bkg Region': extract1d_back_input.value,
                    '1d_calibration_choice': (sky_choice.value == 'sky'),
                }
                logger.log_action("Science & Extraction - 1D Extract", "Setup & Run 1D Extraction", log_params)
                
                trace_obj = spectra.Trace(file= trace_class_file, inst=trace_class_inst, type=trace_class_type, degree=trace_class_sigdegree, 
                                           sigdegree=trace_class_sigdegree, pix0=trace_class_pix0, rad=trace_class_rad,
                                           sc0=trace_class_sc0, transpose=trace_class_transpose, lags=trace_class_lags,
                                           model=trace_class_model, spectrum=trace_class_spectrum,)

                if findpeak_width is None:
                    trace_obj.rows = [0, spec2d_slice.data.shape[0]]
                    trace_obj.index = [0]
                    center = spec2d_slice.shape[0] // 2
                else:
                    center = findpeak_width
                with output_area:
                    peak, _ = trace_obj.findpeak(
                        spec2d_slice, sc0=findpeak_sc0, width=center, thresh=findpeak_thresh, sort=findpeak_sort, 
                        back_percentile=findpeak_back_percentile, method=findpeak_method, smooth=findpeak_smooth, 
                        diff=findpeak_diff, bundle=findpeak_bundle, verbose=findpeak_verbose, plot=findpeak_plot)
                    

                if len(peak) == 0:
                    with param_area_2:
                        print(f"   -> No peak found for slit {i}. Skipping.")
                    next_target()
                    return
                if trace_method_srows is None:
                    srows = [peak[0]]
                else:
                    srows = trace_method_srows
                trace_obj.model = [lambda x: x * 0. + peak[0]]
                with output_area:
                    trace_obj.trace(spec2d_slice, srows, skip=trace_method_skip, gaussian=trace_method_gaussian, display=self.display,
                                   sc0=trace_method_sc0,rad=trace_method_rad, thresh=trace_method_thresh,verbose=trace_method_verbose,
                                   )
                                   # )rad=trace_method_rad, thresh=trace_method_thresh, index=trace_method_index,
                                   #  verbose=trace_method_verbose
                                   # ) #sc0=trace_method_sc0,
                
                    # trace_obj.model = [lambda x: x * 0. + peak[0]]

                def run_extraction_and_prompt():
                    rad = radius_dropdown.value
                    # if extract_back is None:
                    sky_width = rad - 5 
                    extract_back = extract1d_back_input.value
                    back_regions = [[-1*extract_back + (-1 * sky_width), -rad], [extract_back + sky_width, rad]] # [[-10, -rad], [10, rad]]
                    # else:
                    #     back_regions = extract_back
                    with output_area:
                        spec1d = trace_obj.extract(spec2d_slice, rad=rad, back=back_regions, display=self.display,
                                                    fit=extract_fit, old=extract_old, nout=extract_nout,
                                                    threads=extract_threads,medfilt=extract_medfilt
                                                  )
                    spec1d.wave = spec2d_slice.wave[peak]
                    
                    yes_button = widgets.Button(description="Yes", button_style="success")
                    no_button = widgets.Button(description="No", button_style="danger")
                    
                    prompt_label = widgets.Label("Are you satisfied with the extraction?")
                    button_box = widgets.HBox([yes_button, no_button])
    
                    def on_yes(b):
                        if do_sky:
                            wavcal = spectra.WaveCal(f'./CofIwav_{spec2d_slice.header['OBJNAME']}_{targ["ID"]}.fits') # CofIwav_{o.header['OBJNAME']}_{targ["ID"]}.fits
                            swav = copy.deepcopy(wavcal)
                            swav.skyline(spec1d, thresh=skyline_thresh, linear=skyline_linear, plot=skyline_plot, rows=skyline_rows, file=skyline_file)
                            
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
                        # param_area_1.clear_output(wait=True)
                        #with param_area_1:
                        param_area_1.children = [widgets.VBox([prompt_label, button_box],layout=widgets.Layout(border='2px solid grey'))]
    
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
                        # param_area_1.clear_output()
                        param_area_1.children = []
                    self.spec1d_out = extracted_1d_spectra
                    run_button_1d.disabled = False  # re-enable for future runs
    
            target_iter = iter(list(zip(range(len(spec2d_list)), spec2d_list, targets_list)))
            next_target()
    
        run_button_1d.on_click(on_run_extraction_click)
    
        ui_box = widgets.VBox([
            widgets.HBox([sky_choice, radius_dropdown, extract1d_back_input, run_button_1d],layout=widgets.Layout(border='2px solid grey'))
        ])
        if param_area:
            # param_area.clear_output()
            # with param_area:
            param_area.children = [ui_box]
        else:
            display(ui_box)
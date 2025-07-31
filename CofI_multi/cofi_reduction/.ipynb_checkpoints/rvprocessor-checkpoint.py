import os
import datetime
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
from astropy.io import fits
from astropy.nddata import StdDevUncertainty
from astropy import units as u
from specutils import Spectrum1D
from specutils.fitting import fit_generic_continuum
from specutils.manipulation import box_smooth
from astropy.modeling import models, fitting
from scipy.stats import sem

class AstroAnalysis:
    # Rest wavelengths for the Ca II triplet
    REST_L, REST_C, REST_R = 8498.02, 8542.09, 8662.14

    def __init__(self):
        # place to hold data & results
        self.spectrum    = None
        self.normalized  = None
        self.file_name = None
        self.fit_results = []
        # build and display the UI once
        self._build_ui()

    def _build_ui(self):
        # File, user & output filename
        self.file_path    = widgets.Text(description='FITS Path:', placeholder='path/to/your/file.fits',
                                         layout=widgets.Layout(width='400px'))
        self.user_name    = widgets.Text(description='User Name:', layout=widgets.Layout(width='300px'),
                                        placeholder = 'e.g. Abdullah')
        
        self.csv_name     = widgets.Text(description='CSV File Name:', placeholder = 'e.g. M3_stacked',layout=widgets.Layout(width='300px'))
        # parameter sliders
        self.search_width = widgets.FloatSlider(value=30, min=5, max=100, step=1,
                                                description='Search Width (Å):', continuous_update=False,
                                               style={'description_width': 'initial'})
        self.smooth_width = widgets.IntSlider(value=0, min=0, max=20, step=1,
                                              description='Smooth Width (px):', continuous_update=False,
                                             style={'description_width': 'initial'})
        self.fit_width    = widgets.FloatSlider(value=17, min=1, max=50, step=1,
                                                description='Fit Half‑Width (Å):', continuous_update=False,
                                               style={'description_width': 'initial'})
        self.postfix = widgets.Dropdown(options=list(range(1,11)), value=4, description='ID Postfix:')
        # model selector and run button
        self.model_select = widgets.Dropdown(options=['Voigt','Gaussian'], value='Gaussian', description='Model:')
        self.run_button   = widgets.Button(description='Run Analysis', button_style='success')
        self.run_button.on_click(self._on_run)

        # output area
        self.output = widgets.Output()

        ui = widgets.VBox([
            widgets.HBox([self.file_path, self.user_name, self.postfix, self.csv_name]),
            widgets.HBox([self.search_width, self.smooth_width, self.fit_width]),
            widgets.HBox([self.model_select, self.run_button])
        ])
        display(ui, self.output)

    def _on_run(self, _):
        with self.output:
            clear_output()
            fp = self.file_path.value.strip()
            if not fp or not os.path.exists(fp):
                print(f"❌ FITS file not found: {fp!r}")
                return

            # header & default CSV name
            hdr = fits.getheader(fp, 0)
            obj = hdr.get('OBJNAME', 'unknown').strip().replace(' ','_')
            if not self.csv_name.value:
                self.csv_name.value = f"{obj}.csv"
            if not self.csv_name.value.lower().endswith('.csv'):
                self.csv_name.value += '.csv'

            # pipeline
            self._load_spectrum(fp)
            self._normalize()
            self._fit_and_plot()
            self._save_csv()
            print("✅ Analysis complete.")

    def _load_spectrum(self, fp):
        """Read FITS and build a Spectrum1D."""
        with fits.open(fp) as hdul:
            if hdul[0].header['INSTRUME'] == 'kosmos':
                flux = hdul[1].data.flatten()
                wl   = hdul[4].data[0].flatten()
                err  = hdul[2].data.flatten()
            else:
                flux = hdul[0].data.flatten()
                hdr  = hdul[0].header

                # 2. Read the WCS linear solution from header
                crval1 = hdr['CRVAL1']   # starting wavelength at reference pixel (Å)
                crpix1 = hdr['CRPIX1']   # reference pixel index (1-based)
                cdelt1 = hdr['CDELT1']   # wavelength increment per pixel (Å)
                
                # 3. Build pixel indices and compute wavelength array
                #    Note: header pixels are 1-based, numpy is 0-based:
                n_pix = hdr['NAXIS1']
                pixels = np.arange(n_pix)         # 0,1,2,...,4059
                wavelength = (pixels + 1 - crpix1) * cdelt1 + crval1
                wl = wavelength.flatten()

                gain = hdr['gain'] #1.48 # e-/ADU
                read_noise = hdr['RDNOISE'] #3.89 # e-
                
                # Convert flux from ADU to electrons to calculate Poisson noise
                flux_electrons = flux * gain
                
                # Calculate total error (read noise + Poisson noise) in electrons
                err_electrons = np.sqrt(flux_electrons + read_noise**2)
                
                # Convert error back to ADU
                err = err_electrons / gain
                
        self.spectrum = Spectrum1D(spectral_axis=wl*u.angstrom,
                                   flux=flux*u.adu,
                                   uncertainty=StdDevUncertainty(err))
    
    def _normalize(self):
        spec = self.spectrum
    
        # slice by wavelength with Quantity
        sub = spec[8450*u.angstrom : 8700*u.angstrom]
    
        # fit continuum
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cont_model = fit_generic_continuum(sub)
    
        # evaluate continuum & subtract
        cont_vals = cont_model(sub.spectral_axis)
        norm_flux = (sub.flux / cont_vals - 1) * u.adu
    
        # build a new normalized Spectrum1D
        self.normalized = Spectrum1D(
            spectral_axis = sub.spectral_axis,
            flux          = norm_flux,
            uncertainty   = StdDevUncertainty(sub.uncertainty.array),
        )

    # (your plotting code here, unchanged)


        # show continuum & normalized
        fig, (ax1,ax2) = plt.subplots(2,1,figsize=(10,8), sharex=True)
        ax1.plot(sub.spectral_axis.value, sub.flux.value, label='Raw')
        ax1.plot(sub.spectral_axis.value, cont_vals.value, '--', label='Continuum')
        ax1.set_ylabel('Counts'); ax1.legend(); ax1.grid(True)

        ax2.plot(self.normalized.spectral_axis.value,
                 self.normalized.flux.value, label='Normalized')
        ax2.axhline(0, color='r', ls='--')
        ax2.set_xlabel('Wavelength (Å)'); ax2.set_ylabel('Norm. Flux')
        ax2.legend(); ax2.grid(True)
        plt.tight_layout(); plt.show()


    def _fit_and_plot(self):
        """Detect the 3 CaT lines, fit each, plot the results, and compute S/N."""
        # 1) prepare spectrum
        spec = (box_smooth(self.normalized, width=self.smooth_width.value)
                if self.smooth_width.value > 0 else self.normalized)
        wl, fl = spec.spectral_axis.value, spec.flux.value

        # 2) detect approximate line centers
        centers = []
        for rest in (self.REST_L, self.REST_C, self.REST_R):
            mask = (wl >= rest - self.search_width.value) & (wl <= rest + self.search_width.value)
            if mask.any():
                idx = np.argmin(fl[mask])
                centers.append(wl[mask][idx])

        # 3) set up the plot
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(wl, fl, 'k', alpha=0.7, label='Normalized Spec', zorder=2)

        fitter = fitting.LevMarLSQFitter()
        self.fit_results = []

        # 4) fit each line
        for c, color, name in zip(centers, ['blue','green','red'], ['Blue','Center','Red']):
            window = (wl >= c - self.fit_width.value) & (wl <= c + self.fit_width.value)
            x, y   = wl[window], fl[window]
            if len(x) < 5:
                print(f"⚠️ Not enough data for {name} line at {c:.2f} Å")
                continue

            # original trough
            orig_idx  = np.argmin(y)
            orig_wave = x[orig_idx]
            orig_flux = y[orig_idx]

            # initial model
            if self.model_select.value == 'Voigt':
                init = models.Voigt1D(x_0=orig_wave, amplitude_L=orig_flux,
                                      fwhm_G=5, fwhm_L=5)
            else:
                init = models.Gaussian1D(amplitude=orig_flux,
                                        mean=orig_wave, stddev=2)

            fit = fitter(init, x, y)

            # profile center
            center_val = (fit.x_0.value if self.model_select.value=='Voigt'
                          else fit.mean.value)

            # evaluate fit on a fine grid
            x_full = np.linspace(orig_wave - self.fit_width.value,
                                 orig_wave + self.fit_width.value, 300)
            y_full = fit(x_full)

            # fitted trough
            fit_idx   = np.argmin(y_full)
            fit_wave  = x_full[fit_idx]
            fit_flux  = y_full[fit_idx]

            # assemble parameters
            self.file_name = os.path.basename(self.file_path.value)
            split_name    = self.file_name.strip('fits').split('_')
            star_id       = ( split_name[self.postfix.value]
                              if len(split_name)>self.postfix.value else "N/A" )

            rez = {
                'File name':               self.file_name,
                'Star ID':                 star_id,
                'Line':                    name,
                'Model_Type':              self.model_select.value,
                'Orig_Trough_Wavelength':  orig_wave,
                'Orig_Trough_Flux':        orig_flux,
                'Fit_Trough_Wavelength':   fit_wave,
                'Fit_Trough_Flux':         fit_flux,
                'Fit_Center':              center_val,
            }

            # amplitudes & widths
            if self.model_select.value=='Voigt':
                rez.update({
                    'Amplitude_L': fit.amplitude_L.value,
                    'FWHM_G':      fit.fwhm_G.value,
                    'FWHM_L':      fit.fwhm_L.value
                })
            else:
                rez.update({
                    'Amplitude': fit.amplitude.value,
                    'Stddev':    fit.stddev.value
                })

            self.fit_results.append(rez)

            # overplot fit
            ax.plot(x_full, y_full, '--', color=color,
                    label=f'{name} {self.model_select.value} Fit', zorder=3)
            ax.axvline(center_val, color=color, ls=':', zorder=3)

        # 5) compute & show noise region on top
        mask_all = np.zeros_like(wl, dtype=bool)
        for c in centers:
            mask_all |= ((wl >= c - self.fit_width.value) &
                         (wl <= c + self.fit_width.value))
        noise_mask = ~mask_all

        # scatter noise points *on top* in magenta
        ax.scatter(wl[noise_mask], fl[noise_mask],
                   s=15, color='magenta', alpha=0.6,
                   label='Noise Samples', zorder=4)

        # compute noise σ
        noise_std = np.std(fl[noise_mask])

        # 6) compute S/N for each line
        for rez in self.fit_results:
            snr = (abs(rez['Orig_Trough_Flux']) / noise_std
                   if noise_std>0 else np.nan)
            rez['S/N'] = snr

        # 7) finalize
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('gray')
        ax.spines['bottom'].set_color('gray')
        ax.set_title('Calcium Triplet fits', fontsize=26, fontweight='bold', color='#333333')
        ax.set_xlabel('Wavelength (Å)',fontsize=24, fontweight='bold', labelpad=15)
        ax.set_ylabel('Normalized Flux',fontsize=24, fontweight='bold', labelpad=15)
        ax.tick_params(axis='both', which='major', labelsize=22, colors='#444444')
        # ax.legend(frameon=True, loc='center', fontsize=18, framealpha=0.8)
        ax.legend(loc='center left', bbox_to_anchor=(0.44, 0.3), frameon=True, fontsize=18, framealpha=0.8)
        ax.grid(True)
        plt.tight_layout()
        plt.show()




    def _save_csv(self):
        """Append or create a CSV of all fit parameters."""
        if not self.fit_results:
            print("⚠️ No fit results to save.")
            return

        # build DataFrame directly from the list of dicts
        df = pd.DataFrame(self.fit_results)

        # insert User & timestamp at front
        df.insert(0, 'User',        self.user_name.value)
        df.insert(1, 'Date & Time', datetime.datetime.now().isoformat(sep=' '))

        # write or append
        path   = self.csv_name.value
        
        name = path.split("_")[0]

        
        folder_name = f"{name}_rv_analysis"
        os.makedirs(folder_name, exist_ok=True) # Safely create directory
        
        full_path = os.path.join(folder_name, f'{path}')
        
        mode   = 'a' if os.path.exists(full_path) else 'w'
        header = not os.path.exists(full_path)
        df.to_csv(full_path, index=False, mode=mode, header=header)

        print(f"💾 Results saved to '{full_path}'")


    def _on_rv(self, _):
        """Triggered by the 'Calc RV' button."""
        csvf = self.csv_name.value.strip()
        if not csvf or not os.path.exists(csvf):
            with self.output:
                print(f"❌ CSV not found: {csvf!r}. Cannot calculate RV.")
            return
        self.calculate_radial_velocity(csvf)

    def calculate_radial_velocity(self, csv_path):
        import numpy as np
        from scipy.stats import sem
    
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"❌ CSV not found: {csv_path!r}")
            return
    
        # Check required columns
        required = {'Star ID','Line','Fit_Center'}
        if not required.issubset(df.columns):
            print(f"❌ CSV missing columns: {required - set(df.columns)}")
            return
    
        # Widgets
        star_ids = sorted(df['Star ID'].unique())
        star_dd  = widgets.Dropdown(options=star_ids, description='Star ID:')
        # src_rb   = widgets.RadioButtons(
        #     options=[('Fit Center','Fit_Center')],
        #     description='Use:', layout={'width':'max-content'}
        # )
        src_rb = widgets.RadioButtons(
            options=[('Fit Center','Fit_Center'), ('Fit trough','Fit_Trough_Wavelength'),
                     ('Original trough','Orig_Trough_Wavelength')],
            description='Use:', layout={'width':'max-content'}
        )
        
        go       = widgets.Button(description='Compute RV', button_style='success')
        out      = widgets.Output()
    
        def mean_sem(rows):
            vals = rows[src_rb.value].dropna().values
            if vals.size == 0:
                return np.nan, np.nan
            m = vals.mean()
            u = sem(vals) if vals.size > 1 else np.nan
            return m, u
    
        def _compute(b):
            with out:
                clear_output()
                star_id = star_dd.value
                sub     = df[df['Star ID']==star_id]
    
                left_rows   = sub[sub['Line']=='Blue']
                center_rows= sub[sub['Line']=='Center']
                right_rows = sub[sub['Line']=='Red']
    
                mean_L, unc_L = mean_sem(left_rows)
                mean_C, unc_C = mean_sem(center_rows)
                mean_R, unc_R = mean_sem(right_rows)
    
                # Doppler shifts
                rv_L = self._doppler_shift(self.REST_L, mean_L)   if not np.isnan(mean_L) else np.nan
                rv_C = self._doppler_shift(self.REST_C, mean_C)   if not np.isnan(mean_C) else np.nan
                rv_R = self._doppler_shift(self.REST_R, mean_R)   if not np.isnan(mean_R) else np.nan
    
                valid = [rv for rv in (rv_L,rv_C,rv_R) if not np.isnan(rv)]
                rv_mean        = np.mean(valid) if valid else np.nan
                rv_uncertainty = sem(valid, nan_policy='omit') if len(valid)>1 else np.nan
    
                # --- formatted summary + save to .dat ---
                output_data = f"""
Analysis Results for Star: {star_id} from file {csv_path}

Line Statistics:
----------------
Total Blue   ({self.REST_L} Å): {len(left_rows)} measurements
Total Center ({self.REST_C} Å): {len(center_rows)} measurements
Total Red    ({self.REST_R} Å): {len(right_rows)} measurements

Observed Line {src_rb.value} ({src_rb.value} ± SEM):
---------------------------------
{src_rb.value} (Blue):   {mean_L:.3f} ± {unc_L:.3f} Å
{src_rb.value} (Center): {mean_C:.3f} ± {unc_C:.3f} Å
{src_rb.value} (Red):    {mean_R:.3f} ± {unc_R:.3f} Å

Individual Radial Velocities:
-----------------------------
Radial Velocity (Blue):   {rv_L:.3f} km/s
Radial Velocity (Center): {rv_C:.3f} km/s
Radial Velocity (Red):    {rv_R:.3f} km/s

Final Result:
-------------
Final Radial Velocity: {rv_mean:.3f} ± {rv_uncertainty:.3f} km/s
"""
                dat_file = csv_path.replace('.csv', f'_{star_id}_{src_rb.label}.dat')
                with open(dat_file, 'w', encoding='utf-8') as f:
                    f.write(output_data)
    
                print(f"\nAnalysis complete. Results saved to {dat_file}")
                print(output_data)
    
        go.on_click(_compute)
        display(widgets.VBox([star_dd, src_rb, go, out]))



    @staticmethod
    def _doppler_shift(rest, obs):
        c = 2.99792458e5  # km/s
        return c * ( (obs - rest) / rest )
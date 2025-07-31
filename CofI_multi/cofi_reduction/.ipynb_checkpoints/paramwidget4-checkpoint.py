import ipywidgets as widgets
from IPython.display import display, clear_output
class FunctionParameterWidget1:
    """
    A widget class to allow users to customize function parameters for
    calibrate_wavelength, multi_extract2d, and multi_extract1d.
    
    Each section is hidden unless its associated checkbox is checked.
    When active, the user may adjust the parameters via input fields and
    then click a commit button to lock in the changes.
    
    The updated parameters are stored in:
      - self.cw_params for calibrate_wavelength settings
      - self.m2d_params for multi_extract2d settings
      - self.m1d_params for multi_extract1d settings
    """
    
    def __init__(self):
        # --- Section: Calibrate Wavelength Parameters ---
        self.cw_checkbox = widgets.Checkbox(
            value=False, description="Customize Calibrate Wavelength Parameters"
        )
        self.cw_degree = widgets.IntText(
            value=3, description="Fit Degree:", layout=widgets.Layout(width='200px')
        )
        self.cw_thresh = widgets.IntText(
            value=10, description="Threshold:", layout=widgets.Layout(width='200px')
        )
        self.cw_lamp_file = widgets.Text(
            value="new_wave_lamp/old_neon_red_center.dat", description="Lamp File:",
            layout=widgets.Layout(width='300px')
        )

        self.cw_lamp_spec = widgets.Text(
            value="KOSMOS/KOSMOS_red_waves.fits", description="WaveCal_spec:",
            layout=widgets.Layout(width='300px')
        )


        ###################################################
        self.cw_lags = widgets.Text(
            placeholder = "default 50",
            value= "50" , description="Lags value (+/-):",  # Clarified description
            layout=widgets.Layout(width='300px'))

        self.cw_shift_adjust = widgets.Text( # Matches key used in processor
                    placeholder = "default -22.5", # Removed "(center_red_wave )" for clarity
                    value= "-22.5" , description="XMM Shift Multiplier:", # Clarified description
                    layout=widgets.Layout(width='300px'))


        self.cw_clobber = widgets.Dropdown(
            options = [("Yes, recalibrate", True), ("No, use existing", False)], # Clearer options
            value = False, # Default to False to avoid accidental overwrite
            description = "Recalibrate Wave (clobber):", # Clarified description
            layout=widgets.Layout(width='300px'))

        self.cw_plot = widgets.Checkbox(
            value=True, description='Plot initial identify', # Clarified
            style = {"description_width": 'initial'})


        self.cw_plotinter = widgets.Checkbox(
            value=True, description='Plot interactive identify', # Clarified
        style = {'description_width': 'initial'})

        self.cw_sample_over_degree = widgets.Dropdown(
            options = [1,2,3,4,5,6,7,8,9,10],
            value=5, description="Refit Degree (full slit):",  # Clarified description
            layout=widgets.Layout(width='200px')
        )

####################################################
            
        self.cw_commit = widgets.Button(
            description="Commit Cal_Wave Params", # More specific button text
            button_style="success",
            layout=widgets.Layout(width='200px') # Made button wider
        )
            
        self.cw_container = widgets.VBox(
            [self.cw_degree, self.cw_sample_over_degree, self.cw_thresh, 
             self.cw_lamp_spec, self.cw_lamp_file, self.cw_lags, self.cw_shift_adjust,
             self.cw_clobber, self.cw_plot, self.cw_plotinter, self.cw_commit] # Removed duplicate cw_sample_over_degree
        )
        
        # Hide the parameter inputs until enabled.
        self.cw_container.layout.display = "none"

######################################################################
        
        # --- Section: Multi Extract 2D Parameters ---
        self.m2d_checkbox = widgets.Checkbox(
            value=False, description="Customize Multi Extract 2D Parameters"
        )
        self.m2d_thresh = widgets.IntText(
            value=10, description="Thresh:", layout=widgets.Layout(width='200px')
        )
        self.m2d_rad = widgets.IntText(
            value=5, description="Radius:", layout=widgets.Layout(width='200px')
        )
        self.m2d_back_percentile = widgets.IntText(
            value=10, description="Back Percentile:", layout=widgets.Layout(width='200px')
        )
        self.m2d_degree = widgets.IntText(
            value=3, description="Degree:", layout=widgets.Layout(width='200px')
        )
        self.m2d_sigdegree = widgets.IntText(
            value=3, description="SigDegree:", layout=widgets.Layout(width='200px')
        )
        self.m2d_linear = widgets.Checkbox(
            value=False, description="Linear Sky Adjust:" # Clarified
        )
        self.m2d_commit = widgets.Button(
            description="Commit Ext2D Params", # More specific
            button_style="success",
            layout=widgets.Layout(width='180px') # Made button wider
        )
        self.m2d_container = widgets.VBox([
            self.m2d_thresh, self.m2d_rad, self.m2d_back_percentile,
            self.m2d_degree, self.m2d_sigdegree, self.m2d_linear, self.m2d_commit
        ])
        self.m2d_container.layout.display = "none"

##########################################################################
        
        # --- Section: Multi Extract 1D Parameters ---
        self.m1d_checkbox = widgets.Checkbox(
            value=False, description="Customize Multi Extract 1D Parameters"
        )
        self.m1d_thresh_sky = widgets.IntText(
            value=12, description="Thresh Sky:", layout=widgets.Layout(width='200px')
        )
        self.m1d_linear = widgets.Checkbox(
            value=True, description="Linear Sky Fit:" # Clarified
        )
        # self.m1d_sky_cal = widgets.Checkbox( # This is the primary toggle for sky cal in FunctionParameterWidget
        #     value=False, description="Enable Sky Cal (param):" # Clarified this is the parameter for sky_cal method arg
        # )
        self.m1d_skip = widgets.IntText(
            value=10, description="Skip (trace):", layout=widgets.Layout(width='200px')
        )
        self.m1d_degree = widgets.IntText(
            value=3, description="Degree (trace):", layout=widgets.Layout(width='200px')
        )
        self.m1d_sigdegree = widgets.IntText(
            value=3, description="SigDegree (trace):", layout=widgets.Layout(width='200px')
        )
        self.m1d_thresh = widgets.IntText(
            value=10, description="Thresh (findpeak):", layout=widgets.Layout(width='200px')
        )
        self.m1d_back_percentile = widgets.IntText(
            value=10, description="Back Percentile (findpeak):", layout=widgets.Layout(width='220px') # Adjusted width
        )
        self.m1d_method = widgets.Dropdown(
            options=["linear","inverted_cdf","averaged_inverted_cdf","closest_observation","interpolated_inverted_cdf","hazen","weibull","median_unbiased","normal_unbiased"],
            value="linear",
            description="Method (findpeak):",
            layout=widgets.Layout(width='280px') # Adjusted width
        )
        self.m1d_file = widgets.Text(
            value="new_wave_lamp/skyline.dat", description="Skyline File:", # Clarified
            layout=widgets.Layout(width='300px')
        )
        self.m1d_plot = widgets.Checkbox(
            value=True, description="Plot Sky Cal & Result:" # Clarified
        )
        self.m1d_commit = widgets.Button(
            description="Commit Ext1D Params", # More specific
            button_style="success",
            layout=widgets.Layout(width='180px') # Made button wider
        )
        self.m1d_container = widgets.VBox([
            self.m1d_thresh_sky, self.m1d_linear, #self.m1d_sky_cal,
            self.m1d_skip, self.m1d_degree, self.m1d_sigdegree,
            self.m1d_thresh, self.m1d_back_percentile, self.m1d_method,
            self.m1d_file, self.m1d_plot, self.m1d_commit
        ])
        self.m1d_container.layout.display = "none"
        
        # Output widget for messages
        self.output = widgets.Output()
        
        # Set up observers for checkboxes to toggle visibility
        self.cw_checkbox.observe(self._toggle_cw_container, names='value')
        self.m2d_checkbox.observe(self._toggle_m2d_container, names='value')
        self.m1d_checkbox.observe(self._toggle_m1d_container, names='value')
        
        # Commit button click events
        self.cw_commit.on_click(self._commit_cw)
        self.m2d_commit.on_click(self._commit_m2d)
        self.m1d_commit.on_click(self._commit_m1d)
        
        # Parameters stored after commitment
        # Initialize with default *values* from the widgets
        self.cw_params = {
            'degree': self.cw_degree.value,
            'average fit degree': self.cw_sample_over_degree.value,
            'thresh': self.cw_thresh.value,
            'lamp_spec': self.cw_lamp_spec.value,  # <--- FIXED: Store .value
            'lamp_file': self.cw_lamp_file.value,
            'lags': self.cw_lags.value,
            'shift_adjust': self.cw_shift_adjust.value, # <--- Ensure key matches processor
            'weve_cal choice': self.cw_clobber.value, 
            'first plot': self.cw_plot.value, 
            'second plot': self.cw_plotinter.value 
        }
        self.m2d_params = {
            'thresh': self.m2d_thresh.value,
            'rad': self.m2d_rad.value,
            'back_percentile': self.m2d_back_percentile.value,
            'degree': self.m2d_degree.value,
            'sigdegree': self.m2d_sigdegree.value,
            'linear': self.m2d_linear.value
        }
        self.m1d_params = {
            'thresh_sky': self.m1d_thresh_sky.value,
            'linear': self.m1d_linear.value,
            #'sky_cal': self.m1d_sky_cal.value,
            'skip': self.m1d_skip.value,
            'degree': self.m1d_degree.value,
            'sigdegree': self.m1d_sigdegree.value,
            'thresh': self.m1d_thresh.value,
            'back_percentile': self.m1d_back_percentile.value,
            'method': self.m1d_method.value,
            'file': self.m1d_file.value,
            'plot': self.m1d_plot.value
        }
        
    def _toggle_cw_container(self, change):
        if change['new']:
            self.cw_container.layout.display = ""
            self.cw_commit.disabled = False # Re-enable commit if needed.
        else:
            self.cw_container.layout.display = "none"

    def _toggle_m2d_container(self, change):
        if change['new']:
            self.m2d_container.layout.display = ""
            self.m2d_commit.disabled = False
        else:
            self.m2d_container.layout.display = "none"

    def _toggle_m1d_container(self, change):
        if change['new']:
            self.m1d_container.layout.display = ""
            self.m1d_commit.disabled = False
        else:
            self.m1d_container.layout.display = "none"

    def _commit_cw(self, b):
        self.cw_params['degree'] = self.cw_degree.value 
        self.cw_params['average fit degree'] = self.cw_sample_over_degree.value 
        self.cw_params['thresh'] = self.cw_thresh.value
        self.cw_params['lamp_spec'] = self.cw_lamp_spec.value # Ensures .value is stored
        self.cw_params['lamp_file'] = self.cw_lamp_file.value 
        self.cw_params['lags'] = self.cw_lags.value
        self.cw_params['shift_adjust'] = self.cw_shift_adjust.value # Ensure key matches processor
        self.cw_params['weve_cal choice'] = self.cw_clobber.value
        self.cw_params['first plot'] = self.cw_plot.value
        self.cw_params['second plot'] = self.cw_plotinter.value
        
        with self.output:
            clear_output(wait=True)
            print("Calibrate Wavelength parameters updated and committed:", self.cw_params)
        self.cw_commit.disabled = True


    def _commit_m2d(self, b):
        self.m2d_params['thresh'] = self.m2d_thresh.value
        self.m2d_params['rad'] = self.m2d_rad.value
        self.m2d_params['back_percentile'] = self.m2d_back_percentile.value
        self.m2d_params['degree'] = self.m2d_degree.value
        self.m2d_params['sigdegree'] = self.m2d_sigdegree.value
        self.m2d_params['linear'] = self.m2d_linear.value
        with self.output:
            clear_output(wait=True)
            print("Multi Extract 2D parameters updated and committed:", self.m2d_params)
        self.m2d_commit.disabled = True

    def _commit_m1d(self, b):
        self.m1d_params['thresh_sky'] = self.m1d_thresh_sky.value
        self.m1d_params['linear'] = self.m1d_linear.value
        #self.m1d_params['sky_cal'] = self.m1d_sky_cal.value
        self.m1d_params['skip'] = self.m1d_skip.value
        self.m1d_params['degree'] = self.m1d_degree.value
        self.m1d_params['sigdegree'] = self.m1d_sigdegree.value
        self.m1d_params['thresh'] = self.m1d_thresh.value
        self.m1d_params['back_percentile'] = self.m1d_back_percentile.value
        self.m1d_params['method'] = self.m1d_method.value
        self.m1d_params['file'] = self.m1d_file.value
        self.m1d_params['plot'] = self.m1d_plot.value
        with self.output:
            clear_output(wait=True)
            print("Multi Extract 1D parameters updated and committed:", self.m1d_params)
        self.m1d_commit.disabled = True

    def display(self):
        """
        Returns a VBox widget containing all parameter controls.
        """
        return widgets.VBox([
            self.cw_checkbox, self.cw_container,
            widgets.HTML("<hr>"), # Added separator
            self.m2d_checkbox, self.m2d_container,
            widgets.HTML("<hr>"), # Added separator
            self.m1d_checkbox, self.m1d_container,
            self.output
        ])
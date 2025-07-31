import ipywidgets as widgets
from IPython.display import display, HTML

class CofiGuideWidget:
    def __init__(self):
        self._create_guide_elements()

    def _toggle_help_section_factory(self, container):
        def _toggle_section(change):
            container.layout.display = "" if change['new'] else "none"
        return _toggle_section

    def _create_guide_elements(self):
        self.detailed_steps_title = widgets.HTML("""
            <h2>Widget Tabs & Reduction Steps Explanations</h2>
            <p>This section details the operations within each tab and sub-tab of the CofiReductionWidget1.</p>
        """)

        self.help_steps_data = [
            ("📁 Data Input", self._get_tab0_data_input_html()),
            ("⚙️ Calibration Frames", self._get_tab1_calibration_html()),
            ("   - Bias", self._get_master_bias_html()),
            ("   - Dark", self._get_master_dark_html()),
            ("   - Flat", self._get_master_flat_html()),
            ("   - Arc(s)", self._get_master_arc_html()),
            ("🔎 Slits & Targets", self._get_tab2_slits_targets_html()),
            ("   - Find Slits", self._get_slit_id_html()),
            ("   - Filter Targets", self._get_target_selection_html()),
            ("🔬 Science & Extraction", self._get_tab3_science_extraction_html()),
            ("   - Reduce", self._get_science_reduction_html()),
            ("   - Wave Cal", self._get_wavelength_cal_html()),
            ("   - 2D Extract", self._get_2d_extraction_html()),
            ("   - 1D Extract", self._get_1d_extraction_html()),
        ]
        
        # ... (rest of the class remains the same, but the HTML content methods are updated) ...

    # UPDATED HTML CONTENT METHODS
    def _get_tab0_data_input_html(self):
        return """
        <h4>Purpose:</h4>
        <p>This tab is for specifying the directory containing your raw FITS image files.</p>
        <h4>GUI Elements & Actions:</h4>
        <ul>
            <li><b>Folder Path (text input):</b> Enter the path to your FITS files directory.</li>
            <li><b>Read Folder (button):</b> Click to initialize the reducer and log all FITS files found. The log will appear in the output area at the bottom.</li>
        </ul>
        """

    def _get_tab1_calibration_html(self):
        return """
        <h4>Purpose:</h4>
        <p>This tab is dedicated to creating the master calibration frames. Use the sub-tabs for each calibration type.</p>
        <h4>General Workflow:</h4>
        <p>For each sub-tab (Bias, Dark, Flat, Arc):</p>
        <ol>
            <li>Enter a comma-separated list of file numbers for that calibration type.</li>
            <li>Adjust any relevant parameters (e.g., Combine Type, Sigma Reject).</li>
            <li>Click the "Compute" button for that type. The result will appear in the main output area.</li>
        </ol>
        """

    def _get_master_bias_html(self):
        return """
        <h5>Bias Sub-tab</h5>
        <p>Creates a Master Bias to remove electronic readout noise.</p>
        <p><b>Parameters:</b> 'Combine Type' (e.g., median, mean) and 'Sigma Reject' for outlier removal.</p>
        """

    def _get_master_dark_html(self):
        return """
        <h5>Dark Sub-tab</h5>
        <p>Creates a Master Dark to remove thermal signal (dark current).</p>
        <p><b>Parameters:</b> Similar to Bias, with an added 'Clip' value to set a floor on dark current values relative to the uncertainty.</p>
        """

    def _get_master_flat_html(self):
        return """
        <h5>Flat Sub-tab</h5>
        <p>Creates a Master Flat to correct for pixel-to-pixel sensitivity variations.</p>
        <p><b>Parameters:</b> Includes 'Spectral Flat' checkbox to normalize the wavelength shape and 'Window Width' for the normalization filter.</p>
        """
        
    def _get_master_arc_html(self):
        return """
        <h5>Arcs Sub-tab</h5>
        <p>Combines multiple arc lamp exposures into a single, high S/N master arc frame for wavelength calibration.</p>
        """

    def _get_tab2_slits_targets_html(self):
        return """
        <h4>Purpose:</h4>
        <p>This tab handles identifying slit locations on the detector, linking them to targets via a KMS file, and filtering them.</p>
        """
        
    def _get_slit_id_html(self):
        return """
        <h5>Find Slits Sub-tab</h5>
        <p>Locates slit positions on the CCD using a flat-field image and correlates them with a KOSMOS slit mask (KMS) file.</p>
        <p><b>Actions:</b> After finding slits, click 'Update Arc Headers' to embed the slit position data (XMM/YMM) into the master arc frames, preparing them for wavelength calibration.</p>
        """

    def _get_target_selection_html(self):
        return """
        <h5>Filter Targets Sub-tab</h5>
        <p>Allows you to select a subset of the identified slits/targets for processing.</p>
        <p><b>GUI:</b> Choose a selection method ('Index', 'ID', 'Name'), enter the values, and click 'Filter Slits'.</p>
        """

    def _get_tab3_science_extraction_html(self):
        return """
        <h4>Purpose:</h4>
        <p>The core of the pipeline. Use the sub-tabs to perform wavelength calibration, reduce your science image, and extract 2D and 1D spectra.</p>
        """

    def _get_science_reduction_html(self):
        return """
        <h5>Reduce Sub-tab</h5>
        <p>Applies all instrumental corrections to your raw science image.</p>
        <p><b>Parameters:</b> Set the science frame number and cosmic ray rejection parameters. Check 'Apply Calibrations' to use the master bias, dark, and flat frames created earlier.</p>
        """

    def _get_wavelength_cal_html(self):
        return """
        <h5>Wave Cal Sub-tab</h5>
        <p>Determines the precise wavelength solution for each slit using the master arc frames.</p>
        <p><b>Parameters:</b> You can specify the reference lamp files, fit degrees, and the shift multiplier. Check 'Clobber' to force recalibration.</p>
        <p><b>Shift Check:</b> Before running the full calibration, use the 'Check Shift' button to visually inspect the initial shift guess based on the XMM header value.</p>
        """

    def _get_2d_extraction_html(self):
        return """
        <h5>2D Extract Sub-tab</h5>
        <p>Extracts individual, wavelength-calibrated 2D spectra ("slitlets") for each target from the reduced science frame.</p>
        <p><b>Parameters:</b> Choose whether to perform a final wavelength adjustment using sky lines and set the relevant tracing parameters.</p>
        """

    def _get_1d_extraction_html(self):
        return """
        <h5>1D Extract Sub-tab</h5>
        <p>The final step. Traces the object in the 2D spectrum, sums the flux, subtracts the sky, and produces a 1D spectrum (flux vs. wavelength).</p>
        <p><b>Parameters:</b> Set the extraction radius and choose whether to apply a final 1D sky-based wavelength calibration.</p>
        """
    def display(self):
        # Main container VBox that holds all the guide elements
        guide_elements = [self.detailed_steps_title]
        for title, html_content in self.help_steps_data:
            is_indented = title.strip().startswith('-')
            
            # Create a container for the checkbox and its associated help text
            # This makes toggling visibility easier
            help_text_container = widgets.HTML(value=f"<div class='help-section-text'>{html_content}</div>", layout={'display': 'none', 'margin': '5px 0 10px 25px', 'padding': '10px', 'border-left': '3px solid var(--cofi-accent-color)', 'background-color': 'var(--cofi-bg-color-2)'})
            
            # The checkbox toggles the visibility of the help_text_container
            checkbox = widgets.Checkbox(description=title.replace('-', '').strip(), value=False, indent=is_indented)
            checkbox.observe(self._toggle_help_section_factory(help_text_container), names='value')
            
            guide_elements.append(checkbox)
            guide_elements.append(help_text_container)
            
        return widgets.VBox(guide_elements, layout=widgets.Layout(padding='10px'))
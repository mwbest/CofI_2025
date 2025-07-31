import ipywidgets as widgets
from IPython.display import display, HTML

class CofiGuideWidget:
    def __init__(self):
        self._create_guide_elements()

    def _toggle_help_section_factory(self, container):
        """Creates a toggle function for a given container."""
        def _toggle_section(change):
            container.layout.display = "" if change['new'] else "none"
        return _toggle_section

    def _create_guide_elements(self):
        self.detailed_steps_title = widgets.HTML("""
            <style>
                /* This style applies ONLY to the paragraphs inside this HTML widget */
                .help-section-text p, .help-section-text li {
                    font-size: 16px; /* Standard font size */
                    line-height: 1.5; /* Improves readability */
                    font-family: 'Montserrat', sans-serif;
                }
                .help-section-text h4 {
                    font-size: 1.2em;
                    margin-top: 1em;
                }
                 .help-section-text h5 {
                    font-size: 1.1em;
                    margin-top: 1em;
                }
            </style>
            
            <h2>Guide to the Reduction Pipeline</h2>
            <p>This guide explains the purpose of each tab and the steps required to reduce your KOSMOS multi-slit data. Follow the tabs in order from left to right for the best results.</p>
        
            <h3>A Note on Defaults</h3>
            <p>All parameters in the widget are set to sensible default values. For advanced users who wish to modify these, the parameters are organized within each step's respective sub-tab.</p>
        """)
        
        # Structure: (Title for checkbox, HTML content string)
        self.help_steps_data = [
            ("Data Input Tab", self._get_tab0_data_input_html()),
            ("Calibration Tab", self._get_tab1_calibration_html()),
            ("Slits & Targets Tab", self._get_tab2_slits_targets_html()),
            ("Science & Extraction Tab", self._get_tab3_science_extraction_html()),
            ("   - Science Frame Reduction", self._get_science_reduction_html()),
            ("   - Wavelength Calibration", self._get_wavelength_cal_html()),
            ("   - 2D Spectral Extraction", self._get_2d_extraction_html()),
            ("   - 1D Spectral Extraction", self._get_1d_extraction_html()),
        ]

        self.guide_checkboxes_containers = []
        for title, html_content_string in self.help_steps_data:
            is_indented = title.startswith("   -")
            checkbox_description = title.replace("   -", "").strip()
            
            checkbox = widgets.Checkbox(
                description=checkbox_description, 
                value=False, 
                indent=is_indented,
                layout=widgets.Layout(margin='0 0 0 20px' if is_indented else '0')
            )

            text_area = widgets.HTML(value=f"<div class='help-section-text'>{html_content_string}</div>")
            container = widgets.VBox([text_area], layout={'margin': '0 0 0 25px', 'padding': '8px', 'border-left': '4px solid #add8e6', 'background-color': '#f0f8ff', 'display': 'none'})
            
            checkbox.observe(self._toggle_help_section_factory(container), names='value')
            self.guide_checkboxes_containers.append(checkbox)
            self.guide_checkboxes_containers.append(container)
        
        self.main_container = widgets.VBox([
            self.detailed_steps_title,
            widgets.HTML("<hr style='border: 1px solid #ccc; margin: 15px 0;'>"),
            *self.guide_checkboxes_containers
        ], layout=widgets.Layout(padding='10px'))

    def _get_tab0_data_input_html(self):
        return """
            <h4>Purpose:</h4>
            <p>To load your observation data and optionally apply settings from a previous session.</p>
            <h4>Workflow:</h4>
            <ol>
                <li><b>Folder Path:</b> Enter the path to the directory containing your raw FITS files (e.g., <code>Star_JH-21Y252</code>).</li>
                <li><b>Read Folder:</b> Click this to load the FITS files. A log of all found files will appear in the main output area below the widget.</li>
                <li><b>(Optional) Upload Log File:</b> You can upload a <code>.txt</code> log file from a previous reduction session.</li>
                 <li><b>(Optional) Apply Settings from Log:</b> Click this to automatically populate the widget's fields with the parameters from the uploaded log file.</li>
            </ol>
            <p><b>!Note:</b> Before going any further I will advice users to asses the their folder and make sure that there are no files with conflicting numbering. Take the time to numeber your files poperly if they are not it will save a lot of time.</p> 
        """

    def _get_tab1_calibration_html(self):
        return """
            <h4>Purpose:</h4>
            <p>To create the master calibration frames (Bias, Dark, Flat, Arc) needed to correct your science data.</p>
            <h4>Workflow:</h4>
            <p>For each sub-tab (Bias, Dark, Flat, Arcs):</p>
            <ol>
                <li><b>Frames:</b> Enter a comma-separated list of the file numbers for that frame type (e.g., for biases <code>74,75,76</code>).</li>
                <li><b>Compute:</b> Click the "Compute" button. The master frame will be created and displayed in a separate window if the display is enabled.</li>
            </ol>
        """

    def _get_tab2_slits_targets_html(self):
        return """
            <h4>Purpose:</h4>
            <p>To identify the location of the slits on the detector, link them to your targets, and prepare the arc frames for wavelength calibration.</p>
            <h4>Workflow:</h4>
            <ol>
                <li><b>Flat Frame for Slits:</b> Enter the file number of a single, well-exposed flat frame.</li>
                <li><b>KMS File:</b> Provide the full path to your <code>.kms</code> slit mask design file.</li>
                <li><b>Find Slits:</b> Click to detect the slit edges on the flat and display a table of all targets found in the KMS file.</li>
                <li><b>(Optional) Filter Slits:</b> To process only a subset of targets, select a method (Index, ID, or Name), enter a comma-separated list of values (e.g., <code>TARG101,TARG102,TARG106,TARG107</code>), and click "Filter Slits".</li>
                <li><b>Update Arc Headers:</b> Click this to extract a 2D arc spectrum for each selected slit and add its corresponding position (XMM/YMM) to its FITS header. This is a critical step for wavelength calibration.</li>
            </ol>
        """

    def _get_tab3_science_extraction_html(self):
        return """
            <h4>Purpose:</h4>
            <p>This is the main processing tab where you will reduce your science frame and extract the final 2D and 1D spectra.</p>
             <h4>Workflow:</h4>
             <p>The steps in this tab should be performed in order. Each step is detailed in the expandable sections below.</p>
        """

    def _get_science_reduction_html(self):
        return """
            <h5>1. Science Frame Reduction</h5>
            <p><b>Goal:</b> To apply all instrumental corrections to your raw science image.</p>
            <p><b>Action:</b></p>
            <ol>
                <li><b>Science Frame:</b> Enter the file number of your raw science exposure.</li>
                <li><b>Apply Calibrations:</b> Check the boxes to apply the master bias, dark, and flat frames you created in the Calibration Tab. Do not apply flat in this section, but can apply to it effect. The flats will be applied in the 2D extraction section.</li>
                <li><b>Reduce Science Frame:</b> Click this button. The code will apply the selected calibrations and perform cosmic ray rejection. The cleaned 2D science image will be stored for the next steps.</li>
            </ol>
        """

    def _get_wavelength_cal_html(self):
        return """
            <h5>2. Wavelength Calibration</h5>
            <p><b>Goal:</b> To determine the precise relationship between CCD pixels and wavelength for each slit.</p>
            <p><b>Action:</b></p>
            <ol>
                <li><b>(Optional) Check Shift:</b> Click this to see a plot comparing your arc lamp to the reference spectrum. This helps verify that the initial shift guess (set in the advanced parameters) is reasonable.</li>
                <li><b>Run Wavelength Calibration:</b> Click this to start the main calibration process. It will use the prepared 2D arc spectra to find known emission lines and fit a wavelength solution. A <code>.fits</code> file containing this solution is saved for each slit.</li>
            </ol>
        """

    def _get_2d_extraction_html(self):
        return """
            <h5>3. 2D Spectral Extraction</h5>
            <p><b>Goal:</b> To extract individual, flat-fielded, and wavelength-calibrated 2D spectra ("slitlets") for each target.</p>
            <p><b>Action:</b></p>
            <ol>
                <li><b>Setup & Run 2D Extraction:</b> Click this to begin. Start the process by clicking on the (Extraction). The process will first extract the science and flat-field slitlets.Click time you make changes in advance parameters for causion. To off the flat-fielding process unchek the "Apply flat" under <b>Extraction Parameters</b>. Offing it is NOT RECOMMENDED</li>
                <li>An interactive prompt will then appear for each slitlet:
                    <ul>
                    <p>If user choose "No 2D wavelength adjustment" the <b>(default)</b></p>
                    <li> The code will apply flat-field to each accordingly and give a visual rapresentation of what the pectrum might look like </li>
                    <p> If user choose "2D wavelength adjustment"</P>
                    <li>The 2D slitlet is displayed with lines showing the science aperture and the rows selected for sky analysis.</li>
                    <li>You are asked if you are satisfied. If you click <b>"No"</b>, you can select a new radius for the sky rows and the process will repeat for that slitlet.</li>
                    <li>If you click <b>"Yes"</b>, the final wavelength-adjusted 2D spectrum is saved, and the pipeline moves to the next target.</li>
                    </ul>
                </li>
            </ol>
        """

    def _get_1d_extraction_html(self):
        return """
            <h5>4. 1D Spectral Extraction</h5>
            <p><b>Goal:</b> To produce the final, background-subtracted 1D spectrum (flux vs. wavelength) for each target.</p>
            <p><b>Action:</b></p>
            <ol>
                <li><b>Setup & Run 1D Extraction:</b> Click this button to begin the final extraction step.</li>
                <li>An interactive control panel will appear. Here you can:
                    <ul>
                        <li>Choose to apply a final sky-line based wavelength adjustment.</li>
                        <li>Set the <b>Extraction Radius</b> for the science aperture.</li>
                        <li>Define the <b>Bkg. Regions</b> (width of the background windows) and the <b>Sky window offset</b> (the gap between the science and background regions).</li>
                    </ul>
                </li>
                 <li><b>Run Extraction:</b> Click this to start. An interactive "Yes/No" prompt will appear for each spectrum, allowing you to re-run the extraction with a different radius if you are not satisfied.</li>
            </ol>
        """

    def display(self):
        """Returns the main VBox widget containing all organized guide content."""
        return self.main_container
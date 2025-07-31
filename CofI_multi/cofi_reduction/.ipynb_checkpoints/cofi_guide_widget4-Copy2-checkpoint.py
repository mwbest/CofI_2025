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
        # Part 1: How to use march_2025.ipynb
#         self.march_2025_intro_html = widgets.HTML(value="""
#             <h2>Guide to Using <code>march_2025.ipynb</code> with CofiReductionWidget1</h2>
#             <p>The <code>march_2025.ipynb</code> notebook provides an interactive graphical user interface (GUI) for performing KOSMOS slitmask data reduction. This guide explains how to use the notebook and the GUI.</p>
            
#             <h3>1. Initial Setup in <code>march_2025.ipynb</code></h3>
#             <p>The first few cells in the notebook are for setup:</p>
#             <ul>
#                 <li><code>from cofi_reduction1 import CofiReductionWidget1</code>: Imports the main GUI class from your local <code>cofi_reduction1</code> package.</li>
#                 <li><code>import matplotlib.pyplot as plt; from PyQt5 import QtWidgets</code>: Standard imports for enabling Matplotlib's plotting functionalities with the Qt backend.</li>
#                 <li><code>%matplotlib qt</code>: This crucial 'magic' command sets up Matplotlib to use the Qt backend. This allows plots and the TV display tool (if enabled) to open in separate, interactive windows rather than being embedded statically in the notebook. This is essential for interactive elements like line identification in wavelength calibration.</li>
#                 <li><code>reduction_widget = CofiReductionWidget1(display_enabled=True)</code>: This line creates an instance of the reduction widget. <code>display_enabled=True</code> ensures that the <code>pyvista.tv</code> tool will be initialized for displaying images during the reduction process. If set to <code>False</code>, no graphical display will be attempted.</li>
#                 <li><code>reduction_widget.show()</code>: This line displays the CofiReductionWidget1 interface within the Jupyter notebook cell output.</li>
#             </ul>
#             <p><b>Action:</b> Run these initial cells in <code>march_2025.ipynb</code> to load and display the widget.</p>

#             <h3>2. Using the CofiReductionWidget1 Interface</h3>
#             <p>Once the widget is displayed, you will interact with its various tabs to perform the data reduction steps. The comments in <code>march_2025.ipynb</code> provide example inputs which you can use as a starting point:</p>
#             <pre><code>
# # folder path: UT230909 # Star_JH-21Y252
# # KMS file path: kms/Copy of kosmos.23.seg3g2.kms # march_2025_kms/kosmos.36.M3new.kms
# # Bias file numbers: 74,75,76,77,78 
# # Dark file numbers: 94,95,96
# # Flat file numbers: 21,22
# # Arcs file numbers: 23,24
# # Filter slits index: 6,7,9,11,13 # TARG101,TARG102,TARG104,TARG106,TARG107
#             </code></pre>
#             <p>You will enter these paths and numbers into the corresponding fields in the widget's tabs. Detailed explanations for each tab and its functions are provided below. Ensure that the paths to your data folder and KMS file are correct for your system.</p>
#         """)

        self.detailed_steps_title = widgets.HTML("""
            <h2>Widget Tabs & Reduction Steps Explanations</h2>
            <p>This section details the operations within each tab of the CofiReductionWidget1. It explains the GUI elements, the actions they perform, and references the corresponding processes and code logic primarily drawn from the <code>CofI KOSMOS slitmask reduction final draft-optimized.ipynb</code> notebook (referred to as 'KOSMOS Notebook' below for brevity).</p>
        """)

        # Structure: (Title for checkbox, method to get HTML content string)
        self.help_steps_data = [
            ("Tab 0: 📁 Data Input", self._get_tab0_data_input_html()),
            ("Tab 1: ⚙️ Calibration Frames", self._get_tab1_calibration_html()),
            ("   L1: Master Bias Creation", self._get_master_bias_html()),
            ("   L1: Master Dark Creation", self._get_master_dark_html()),
            ("   L1: Master Flat Creation", self._get_master_flat_html()),
            ("   L1: Master Arc(s) Preparation", self._get_master_arc_html()),
            ("Tab 2: 🔎 Slits & Targets", self._get_tab2_slits_targets_html()),
            ("   L2: Slit Identification & Referencing", self._get_slit_id_html()),
            ("   L2: Target Selection / Filtering", self._get_target_selection_html()),
            ("   L2: Arc Header Update (XMM/YMM)", self._get_arc_header_update_html()),
            ("Tab 3: 🔬 Science & Extraction", self._get_tab3_science_extraction_html()), 
            ("   L3: Checiking shift values", self._get_checking_shift_value_html()),
            ("   L3: Wavelength Calibration", self._get_wavelength_cal_html()),
            ("   L3: Science Image Reduction", self._get_science_reduction_html()),
            ("   L3: 2D Spectral Extraction", self._get_2d_extraction_html()),
            ("   L3: 1D Spectral Extraction", self._get_1d_extraction_html()),
            ("Tab 4: 🛠️ Parameters", self._get_tab4_parameters_html()),
        ]

        self.guide_checkboxes_containers = []
        for title, html_content_string in self.help_steps_data:
            is_level_1 = title.startswith("   L")
            checkbox_description = title[title.find(":")+1:].strip() if ":" in title else title
            if is_level_1:
                 # For Level 1, adjust description and add indent to checkbox visual
                checkbox = widgets.Checkbox(description=checkbox_description, value=False, indent=True, layout=widgets.Layout(margin='0 0 0 20px'))
            else:
                checkbox = widgets.Checkbox(description=checkbox_description, value=False, indent=False)

            # html_content will be a string now
            text_area = widgets.HTML(value=html_content_string) 
            container = widgets.VBox([text_area], layout={'margin': '0 0 0 25px', 'padding': '8px', 'border-left': '4px solid #add8e6', 'background-color': '#f0f8ff'})
            container.layout.display = "none"
            checkbox.observe(self._toggle_help_section_factory(container), names='value')
            self.guide_checkboxes_containers.append(checkbox)
            self.guide_checkboxes_containers.append(container)
        
        self.main_container = widgets.VBox([
            # self.march_2025_intro_html,
            widgets.HTML("<hr style='border: 1px solid #ccc; margin: 15px 0;'>"), # Visually distinct hr
            self.detailed_steps_title,
            *self.guide_checkboxes_containers
        ], layout=widgets.Layout(padding='10px'))

    def _get_tab0_data_input_html(self):
        return """
        <div class='help-section-text'>
            <h4>Purpose:</h4>
            <p>This tab is for specifying the directory containing your raw FITS image files (bias, dark, flat, arc, science frames).</p>
            <h4>GUI Elements & Actions:</h4>
            <ul>
                <li><b>Folder name (text input):</b> Enter the path to the directory where your FITS files are stored.
                    <br/><em>Example: <code>UT230909</code> or <code>Star_JH-21Y252</code>. Ensure this path is correct for your system.</em></li>
                <li><b>Read folder (button):</b> After entering the path, click this button.
                    <ul>
                        <li><b>Action:</b> Initializes the <code>pyvista.imred.Reducer</code> object, configured for KOSMOS data, pointing to your specified directory.</em></li>
                        <li><b>Output:</b> Reads and logs all FITS files in that directory. A summary table of the files (filename, object, exposure time, etc.) will appear in the main output area below the tabs.</em></li>
                    </ul>
                </li>
            </ul>
            <h4>Output Area:</h4>
            <p>Messages from this tab, including any errors during folder reading or the log of FITS files, will be displayed in the main output area at the bottom of the widget (below all tabs).</p>
        </div>
        """

    def _get_tab1_calibration_html(self):
        return """
        <div class='help-section-text'>
            <h4>Purpose:</h4>
            <p>This tab is dedicated to creating the master calibration frames: Master Bias, Master Dark, Master Flat, and Master Arc(s). These are essential for correcting instrumental effects in your science data.</p>
            <h4>General Workflow for this Tab:</h4>
            <p>For each type of calibration frame (Bias, Dark, Flat, Arc):</p>
            <ol>
                <li>Locate the "Frames" text input field for that type (e.g., "Bias Frames:").</li>
                <li>Enter a comma-separated list of file numbers corresponding to the raw frames of that type. These file numbers are typically the sequence numbers seen in the filenames (e.g., if you have <code>Bias.0074.fits</code>, <code>Bias.0075.fits</code>, you'd enter <code>74,75</code>). Or enter a comma-separated name of the files, if your numbering is not that good.</li>
                <li>Click the associated "Compute" button (e.g., "Compute Bias").</li>
                <li><b>Output:</b> The master frame will be computed. A confirmation message (or error) will appear in the main output area below the tabs. If the TV display is enabled (<code>display_enabled=True</code> at widget initialization), the resulting master frame will be shown in the PyVista TV window.</li>
            </ol>
            <p>Detailed explanations for creating each specific master frame type are provided in the expandable sections below.</p>
        </div>
        """

    def _get_master_bias_html(self):
        return """
        <div class='help-section-text'>
            <h5>Master Bias Creation</h5>
            <p><b>What it is:</b> A Master Bias frame is created by combining multiple zero-second exposures (bias frames) to characterize and remove electronic readout noise or fixed-pattern noise from the CCD sensor.</p>
            <p><b>GUI Interaction:</b> Enter the file numbers of your raw bias frames (e.g., <code>74,75,76,77,78</code>) into the "Bias Frames:" input field. Click the "Compute Bias" button.</p>
        </div>
        """

    def _get_master_dark_html(self):
        return """
        <div class='help-section-text'>
            <h5>Master Dark Creation</h5>
            <p><b>What it is:</b> A Master Dark frame is used to remove 'dark current' – signal generated by thermal electrons in the CCD that accumulates over time, even in the absence of light. It's dependent on exposure time and CCD temperature.</p>
            <p><b>GUI Interaction:</b> Enter dark frame numbers (e.g., <code>94,95,96</code>) in "Dark Frames:" and click "Compute Dark".</p>
            
        </div>
        """

    def _get_master_flat_html(self):
        return """
        <div class='help-section-text'>
            <h5>Master Flat Creation</h5>
            <p><b>What it is:</b> A Master Flat corrects for pixel-to-pixel sensitivity variations across the CCD, as well as imperfections in the optical path such as dust particles (which cause "donuts") or vignetting (darkening at image edges).</p>
            <p><b>GUI Interaction:</b> Enter flat frame numbers (e.g., <code>21,22</code>) in "Flat Frames:" and click "Compute Flat".</p>
        </div>
        """

    def _get_master_arc_html(self):
        return """
        <div class='help-section-text'>
            <h5>Master Arc(s) Preparation</h5>
            <p><b>What it is:</b> Arc lamp exposures provide spectra with known emission lines at very specific wavelengths. These are crucial for wavelength calibration – mapping CCD pixel positions to physical wavelengths.</p>
            <p><b>GUI Interaction:</b> Enter arc frame numbers (e.g., <code>23,24</code>) in "Arc Frames:" and click "Compute Arcs".</p>
        
        </div>
        """

    def _get_tab2_slits_targets_html(self):
        return """
        <div class='help-section-text'>
            <h4>Purpose:</h4>
            <p>This tab handles the crucial steps of identifying where the slits fall on the detector, associating them with target information from a slit mask design file (KMS file), allowing the user to select a subset of these targets for processing, and preparing the arc frames for wavelength calibration by embedding slit position data into their headers.</p>
            <h4>General Workflow & GUI Elements for this Tab:</h4>
            <p>It's generally recommended to perform the actions in this tab in the order presented by the buttons, from left to right or top to bottom as they appear, after providing the necessary inputs.</p>
            <ol>
                <li><b>Provide Inputs:</b>
                    <ul>
                        <li><b>Slit Finding Flat (text input):</b> Enter the file number of a single, well-exposed flat-field image. The illumination in this flat should clearly show the edges of all slitlets cut into the mask. Example: <code>21</code> (referring to <code>Flat_SEG3G2.0021.fits</code>).</li>
                        <li><b>KMS file (text input):</b> Enter the full path to your KOSMOS Slit Mask (<code>.kms</code>) file. This file contains the design specifications for your slit mask, including slit IDs, target names, and their X/Y positions (XMM/YMM) on the mask focal plane. Example: <code>kms/Copy of kosmos.23.seg3g2.kms</code>.</li>
                    </ul>
                </li>
                <li><b>Click "Find Slits" button:</b> This initiates slit identification and KMS file reading.</li>
                <li><b>Click "Filter Slits" button:</b> (Optional but common) This allows selection of specific targets/slits if you don't want to process all of them.</li>
                <li><b>Click "Update xmm and ymm" button:</b> This prepares the master arc frames for wavelength calibration by adding positional information.</li>
            </ol>
            <p>Detailed explanations for these operations are in the expandable sections below.</p>
            <p><b>Parameter Area (Output box within this tab):</b> Some operations, like "Filter Slits", will display their own interactive controls (dropdowns, text boxes, buttons) within this area when activated.</p>
            <p><b>Main Output Area:</b> General messages, tables of targets, and errors from this tab will appear in the main output area below all tabs.</p>
        </div>
        """

    def _get_slit_id_html(self):
        return """
        <div class='help-section-text'>
            <h5>Slit Identification & Referencing</h5>
            <p><b>What it is:</b> Locating the positions of all individual slits on the CCD detector using a flat-field image, and then correlating these found slits with the target information provided in a KOSMOS slit mask (KMS) file.</p>
            <p><b>GUI Actions:</b> After entering the "Slit Finding Flat" number and "KMS file" path in Tab 4, click the "Find Slits" button.</p>
            <p><b>Details & Process:</b>
            <br/>1. Reduce the specified flat: <code>flat1 = red.reduce(21)</code> (using file 21 as example)
            <br/>2. Initialize trace object: <code>trace0=spectra.Trace(transpose=True)</code> (<code>transpose=True</code> is specific to KOSMOS data orientation where dispersion is along rows after transpose).
            <br/>3. Find slit edges on the flat: <code>bottom,top = trace0.findslits(flat1,display=t,thresh=0.5,sn=True)</code>. The <code>thresh</code> parameter controls sensitivity to detect slit edges; I All input are correct and you encounter an error of finding slits increse the <code>thresh</code>. <code>sn=True</code> Imply a signal-to-noise based thresholding (leave it checked...recommended). The TV tool (if enabled) can display the identified slit edges overlaid on the flat. The <code>trace0</code> object now stores the geometric definitions (polynomial fits to edges) of these found slits.
            <br/>4. Read target data from KMS file: <code>targets=slitmask.read_kms(kmsfile,sort='YMM')</code>. This loads slits XMM/YMM coordinates from the <code>.kms</code> file, sorting them by their Y/X-position on the mask (<code>YMM/XMM</code>).
            <br/>5. Validation: <code>if len(targets) != len(bottom) : print('ERROR, number of identified slits does not match number of targets')</code>. A warning is printed in the output area if there's a mismatch.
            <br/>6. Display Targets: The loaded <code>targets</code> table is converted to a Pandas DataFrame and displayed in the main output area for user review.
            </p>
            <p><b>Widget State:</b> The widget stores the created <code>trace</code> (from <code>trace0</code>) and <code>targets</code> objects internally for subsequent steps.</p>
        </div>
        """

    def _get_target_selection_html(self):
        return """
        <div class='help-section-text'>
            <h5>Target Selection / Filtering</h5>
            <p><b>What it is:</b> Allowing the user to choose a specific subset of the identified slits (and their associated targets) for further processing, rather than reducing all slits found on the mask.</p>
            <p><b>GUI Actions:</b> After "Find Slits" has been successfully run, click the "Filter Slits" button in Tab 4. This will make a new set of UI controls appear in the "parameter area" (the output box located within Tab 4 itself).</p>
            <p><b>Dynamic UI in Parameter Area:</b>
            <ul>
                <li><b>Selection Method (dropdown):</b> Choose how you want to specify targets: by 'Index' (their 0-based order in the displayed table), 'ID' (e.g., 'TARG113'), or 'Name' (if names are unique in the KMS file).</li>
                <li><b>Targets (text input):</b> Based on your chosen method, enter a comma-separated list of values. For 'Index', use numbers (e.g., <code>6,7,9,11,13</code>). For 'ID' or 'Name', enter the strings (e.g., <code>TARG108,TARG107,TARG106</code>).</li>
                <li><b>Run Selection (button within param_area):</b> Click this button to perform the filtering.</li>
            </ul>
            </p>
            <p><b>Details & Process:</b>
            <br/>The "Filter Slits" button click triggers a call to <code>CofiProcessor1.TargetSelector.select_targets(...)</code>. This method is based on the <code>select_targets</code> function defined in the KOSMOS notebook.
            <br/>Example logic from KOSMOS <code>select_targets</code> function for index-based selection: <code>indices = input("Enter the indices (comma-separated): "); gd = [int(idx.strip()) for idx in indices.split(',')]</code>.
            <br/>The processor method then filters both the <code>trace</code> object (keeping only the geometric models for selected slits) and the <code>targets</code> table.
            <br/><code>gdtrace = copy.deepcopy(trace); gdtrace.model = [trace.model[i] for i in gd]; gdtrace.rows = [trace.rows[i] for i in gd]; trace = copy.deepcopy(gdtrace); selected_targets = targets[gd]</code>
            </p>
            <p><b>Output:</b> The main output area will show a confirmation message "Selection complete!", the number of selected targets, and a display of the newly filtered <code>targets</code> table. The widget's internal <code>self.trace</code> and <code>self.targets</code> are updated to these filtered versions.</p>
        </div>
        """

    def _get_arc_header_update_html(self):
        return """
        <div class='help-section-text'>
            <h5>Arc Header Update (XMM/YMM)</h5>
            <p><b>What it is:</b> This step prepares the master arc lamp spectra for detailed wavelength calibration. It extracts 2D spectral cutouts from the master arc frame for each selected slit and, crucially, embeds the slit's designed XMM and YMM coordinates (from the KMS file) into the FITS header of each cutout. These coordinates help provide an accurate initial guess for the wavelength shift in the subsequent calibration step.</p>
            <p><b>GUI Actions:</b> After slits are found (and optionally filtered), and a master arc frame has been computed (Tab 1), click the "Update xmm and ymm" button in Tab 4.</p>
            <p><b>Details & Process:</b>
            <br/>1. Extract 2D arc spectra: <code>arcec=trace.extract2d(arcs,display=t)</code>. This uses the current <code>trace</code> object (which defines slit locations and shapes, possibly filtered) to cut out the corresponding regions from the master arc frame (<code>self.arcs_frame</code>). The result <code>arcec</code> is a list of 2D <code>CCDData</code> objects, one for each slit.
            <br/>2. Update headers: <code>for arc,target in zip(arcec,targets) : arc.header['XMM'] = target['XMM']; arc.header['YMM'] = target['YMM']</code>. This loop iterates through the extracted 2D arc spectra (<code>arcec</code>) and the corresponding entries in the (possibly filtered) <code>targets</code> table. It takes the 'XMM' and 'YMM' values for each target and writes them into the FITS header of the associated 2D arc spectrum.
            </p>
            <p><b>Widget State:</b> The list of these header-updated 2D arc spectra is stored internally in the widget as <code>self.arcec</code>. This <code>self.arcec</code> is then used as input for the "Wavelength calibration" process in Tab 3. A confirmation "Arc headers updated..." is shown in the main output area.</p>
        </div>
        """

    def _get_tab3_science_extraction_html(self):
        return """
        <div class='help-section-text'>
            <h4>Purpose:</h4>
            <p>This tab is the core of the spectroscopic data processing pipeline. It handles the wavelength calibration of your instrument setup using arc lamp spectra, the reduction of your raw science images (applying calibrations and cosmic ray cleaning), and finally, the extraction of 2D and 1D spectra for your selected science targets.</p>
            <h4>General Workflow & GUI Elements for this Tab:</h4>
            <p>Ensure that master calibration frames (Tab 3) have been computed and that slit/target definitions, including the XMM/YMM header update for arcs (Tab 4), are complete before proceeding with this tab.</p>
            <ol>
                <li><b>Click "Wavelength calibration" button:</b> This performs detailed wavelength calibration for each selected slit using the prepared 2D arc spectra (<code>self.arcec</code>). The results (wavelength solution files) are saved to disk.</li>
                <li><b>Provide Science Frame Input:</b>
                    <ul>
                        <li><b>Science Frame (text input):</b> Enter the file number of your raw science exposure that you wish to process. Example: <code>20</code>.</li>
                    </ul>
                </li>
                <li><b>Click "Run Reduction" button:</b> This applies calibrations (bias, dark, flat if available and configured) and cosmic ray rejection to the specified science frame.</li>
                <li><b>Click "Extract Spectrum 2D" button:</b> This takes the reduced science frame and, using the slit traces and wavelength solutions, extracts individual 2D wavelength-calibrated spectra for each target.</li>
                <li><b>Click "Extract Spectrum 1D" button:</b> This processes the 2D extracted spectra to produce final 1D spectra (flux vs. wavelength) for each target, including sky subtraction.</li>
            </ol>
            <p>Detailed explanations for these critical operations are in the expandable sections below.</p>
            <p><b>Parameter Area (within Tab 5 and other output areas):</b> The 2D and 1D extraction steps will display their own interactive controls (dropdowns for choices, buttons for confirmation) in the parameter areas (<code>self.param_area</code>, <code>self.param_area_1</code>, <code>self.param_area_2</code>) and provide feedback in        <code>self.output_area_1</code> and <code>self.output_area</code> when Tab 5 is active.</p>
            <p><b>Advanced Parameters:</b> The detailed numerical parameters governing these processes (e.g., fit degrees, thresholds, line lists) can be fine-tuned in "Tab 6: Parameters".</p>
        </div>
        """

    def _get_checking_shift_value_html(self):
        return """
         <div class='help-section-text'>
               <h5>Checking the Lamp Shift Value</h5>
               <p><b>What it is:</b> It checks how much the arc has shifted relative to the lamp's reference solution from KOSMOS. This indicates the shift value you should use for wavelength calibration with your specific lamp (Ne, Ar, or Kr). We usually use Ne, which is the default in the notebook, but for users of Ar or Kr, this step is crucial.</p>
               <p><b>GUI Interaction:</b> Click <b>"Shift check"</b> to view the plot comparison.</p>
               <p>If you are using a lamp type other than the default (e.g., Ar or Kr instead of Ne) or a different reference file than <code>'KOSMOS/KOSMOS_red_waves.fits'</code>, run <b>"Shift check"</b> before performing wavelength calibration. This also means that you need to make the necessary changes in the <b>Advanced Parameters</b> as follows:</p>
               <ul>
                     <li><code>WaveCal_spec</code> (<code>lamp_spec_file</code>, path to the reference FITS WaveCal file, e.g., <code>'KOSMOS/KOSMOS_red_waves.fits'</code>).</li>
                     <li><code>XMM Shift Multiplier</code> (<code>shift_multiplier</code>, multiplier to convert XMM mask coordinates to an initial pixel shift guess).</li>
               </ul>
               <p>Once you have achieved the desired shift, these values and the file will be used in the wavelength calibration. Make sure you save them somewhere because the widget will revert to its default settings if you rerun the cell.</p> 
         </div>
        """


    
    def _get_wavelength_cal_html(self):
        return """
        <div class='help-section-text'>
            <h5>Wavelength Calibration</h5>
            <p><b>What it is:</b> This critical process determines the precise mathematical relationship (wavelength solution) between pixel positions along the dispersion axis on the CCD and the actual physical wavelength of light for each slit. It uses the previously prepared 2D arc lamp spectra (<code>self.arcec</code>) which have XMM/YMM information in their headers.</p>
            <p><b>GUI Actions:</b> In Tab 5, after completing Tab 4 (especially "Update xmm and ymm"), click the "Wavelength calibration" button.</p>
            <p><b>Details & Process (simplified from the loop <code>for i,(arc,targ) in enumerate(zip(arcec,targets)):</code>):</b>
            <br/>The widget calls <code>processor.calibrate_wavelength(self.arcec, self.targets, clobber=None)</code>. Inside <code>calibrate_wavelength</code>:
            <ol>
                <li>For each 2D arc spectrum (<code>arc</code> from <code>self.arcec</code>) and its target info (<code>targ</code>):
                    <ul>
                        <li>A filename for the solution is defined: <code>wavname = 'CofIwav_{:s}.fits'.format(targ['ID'])</code>.</li>
                        <li>If <code>clobber=True</code> (or the file doesn't exist, or <code>clobber=None</code> and the widget's parameter for clobber is True), the calibration proceeds:
                            <ul>
                                <li>Initialize WaveCal object: <code>wav=spectra.WaveCal(lamp_spec_file)</code> (e.g., <code>'KOSMOS/KOSMOS_red_waves.fits'</code> as default from <code>paramwidget1</code>, which is a reference spectrum).</li>
                                <li>Fit to reference: <code>wav.fit(degree=fit_degree)</code> (e.g., <code>degree=3</code>).</li>
                                <li>Estimate initial pixel shift: <code>shift = int(arc.header['XMM'] * shift_multiplier)</code> (e.g., <code>shift_multiplier=-22.5</code> from <code>paramwidget1</code>). This uses the XMM value from the arc's header.</li>
                                <li>Define initial lag range for cross-correlation: <code>lags_initial = np.arange(shift - lags_offset, shift + lags_offset)</code> (e.g., <code>lags_offset=50</code>).</li>
                                <li><b>Iterative Line Identification (1D):</b> A <code>while</code> loop calls <code>wav.identify(arc[nrow//2], plot=plot_first_identify, plotinter=plot_inter_identify, lags=lags_initial, thresh=identify_thresh, file=lamp_file_for_identify)</code>. This is for the central row of the 2D arc.
                                    <ul><li><code>plot=True/plotinter=True</code> (defaults from <code>paramwidget1</code>) enables interactive plots where the user can verify and adjust line identifications against a lamp line list (e.g., <code>'new_wave_lamp/old_neon_red_center.dat'</code>).</li>
                                    <li><code>thresh</code> (e.g., 10) is for peak detection. Lags are adjusted after the first attempt.</li>
                                    </ul>
                                </li>
                                <li><b>Refine and Fit 2D Solution:</b> After interactive 1D identification, weak lines might be checked. The polynomial degree for the full 2D fit is set: <code>wav.degree = wave_fit_degree_after_identify</code> (e.g., 5). Then, <code>wav.identify(arc, plot=plot_first_identify, nskip=nrow//10, thresh=identify_thresh)</code> performs the 2D wavelength solution across the slit, sampling at multiple spatial positions (<code>nskip=nrow//10</code>).</li>
                                <li>Save solution: <code>wav.write(wavname)</code> saves the polynomial coefficients to the <code>CofIwav_TARGETID.fits</code> file.</li>
                                <li>Verify: <code>wav.add_wave(arc)</code> applies the solution to the arc, and <code>self.display.tv(wav.correct(arc, ...))</code> can show the wavelength-rectified arc if display is on.</li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ol>
            </p>
            <p><b>Parameters:</b> Many parameters (fit degrees, thresholds, lamp files, clobber option, plot toggles) are configurable via "Tab 6: Parameters" in the "Customize Calibrate Wavelength Parameters" section. The defaults are generally taken from the KOSMOS notebook procedures or <code>paramwidget1.py</code>.</p>
        </div>
        """

    def _get_science_reduction_html(self):
        return """
        <div class='help-section-text'>
            <h5>Science Image Reduction</h5>
            <p><b>What it is:</b> Applying all necessary instrumental corrections to your raw science image. This typically includes overscan correction, bias subtraction, dark subtraction, flat-field division, and cosmic ray rejection.</p>
            <p><b>GUI Actions:</b> In Tab 3, enter the file number of your raw science exposure into the "Science Frame:" input field. Then, click the "Run Reduction" button.</p>
            <p><b>Details & Process:</b>
            <br/>The widget calls <code>self.red.reduce(...)</code>. The exact arguments depend on the <code>self.calibration</code> flag of the widget.
            <ul>
                <li><b>If <code>self.calibration</code> (Science_cal checked) is True (and master frames exist):</b> Full calibration is attempted.
                    <br/><em>Conceptual: <code>star1=red.reduce(20, crbox='lacosmic', bias=self.bias_frame, flat=self.flat_frame, dark=self.dark_frame, display=t)</code>.</em>
                    <br/>The process involves: overscan correction (by <code>Reducer</code>), subtraction of <code>self.bias_frame</code>, subtraction of <code>self.dark_frame</code> (scaled to science exposure time), division by <code>self.flat_frame</code>, and cosmic ray rejection (e.g., <code>crbox='lacosmic'</code>).</li>
                <li><b>If <code>self.calibration</code> (Science_cal not checked)is False (widget default) or master frames are missing:</b> Basic reduction, focusing on cosmic ray removal.
                    <br/><em>Recommended: <code>imcr=red.reduce(20,crbox='lacosmic',crsig=6,display=t, objlim=10 )</code></em>
                    <br/>This performs overscan correction as defined by the <code>Reducer</code>'s default behavior and applies cosmic ray rejection using <code>astroscrappy.detect_cosmics</code> (via <code>crbox='lacosmic'</code>). Parameters like <code>crsig</code> (Laplacian-to-noise limit) and <code>objlim</code> (contrast limit for CR detection) control its sensitivity.</li>
            </ul>
            </p>
            <p><b>Widget State:</b> The fully calibrated and cosmic-ray-cleaned 2D science image is stored as <code>self.reduced_frame</code>, ready for spectral extraction.</p>
        </div>
        """

    def _get_2d_extraction_html(self):
        return """
        <div class='help-section-text'>
            <h5>2D Spectral Extraction</h5>
            <p><b>What it is:</b> This step takes the fully reduced 2D science frame (<code>self.reduced_frame</code>) and extracts the individual 2D spectrum (a "slitlet") for each targeted object. Crucially, the wavelength solution derived from the arc lamps is applied during this process, so the output 2D spectra are wavelength-calibrated.</p>
            <p><b>GUI Actions:</b> In Tab 5, after "Run Reduction" is complete, click the "Extract Spectrum 2D" button.</p>
            <p><b>Details & Process:</b>
            <br/>The widget calls <code>processor.multi_extract2d(...)</code> which is based on the <code>multi_extract2d</code> function in the KOSMOS notebook: <code>out=multi_extract2d(red,trace,targets,imcr,display=t, linear=False)</code>.
            <br/>Inside <code>processor.multi_extract2d</code>:
            <ol>
                <li><b>Initial Cutouts:</b> <code>out = trace.extract2d(imcr, display=self.display)</code> uses the slit traces (<code>self.trace</code>) to cut out the regions corresponding to each target from the reduced science image (<code>self.reduced_frame</code>, which is <code>imcr</code>).</li>
                <li><b>Wavelength Adjustment Choice (Interactive UI in <code>param_area</code> of Tab 3):</b> A dropdown appears: "Adjustment Choice:" with options ('2D wavelength adjustment', 'No 2D wavelength adjustment').</li>
                <li>For each extracted 2D slitlet (<code>o</code>) and its target information (<code>targ</code>):
                    <ul>
                        <li>Load Wavelength Solution: <code>wav = spectra.WaveCal(f'./CofIwav_{targ["ID"]}.fits')</code> (loads the <code>.fits</code> file saved during Wavelength Calibration).</li>
                        <li>Apply Solution: <code>wav.add_wave(o)</code> maps pixels to wavelengths.</li>
                        <li><b>If "2D wavelength adjustment" was chosen by user:</b>
                            <ul>
                                <li>A new trace (<code>trace1</code>) is defined.</li>
                                <li><code>trace1.findpeak(o, thresh=_thresh, ...)</code> finds the object's peak within the slitlet to guide sky line identification. (<code>_thresh</code> comes from <code>paramwidget1</code> or method defaults).</li>
                                <li><code>wav.skyline(o, thresh=_thresh, rows=rows, plot=plot_enabled(display_obj), linear=_linear)</code> uses known night sky emission lines present in the science data itself to perform a final adjustment to the wavelength solution. <code>rows</code> are defined to exclude the object. <code>_linear</code> from <code>paramwidget1</code>. Plots may appear if display is on.</li>
                                <li>The wavelength solution is re-applied: <code>wav.add_wave(o)</code>.</li>
                                <li>Image is wavelength-rectified: <code>o = wav.correct(o, o.wave[nrows // 2])</code>.</li>
                                <li>The 2D spectrum is saved: <code>o.write(f'{name}_{targ["ID"]}_2d.fits')</code>.</li>
                            </ul>
                        </li>
                        <li><b>If "No 2D wavelength adjustment" was chosen:</b>
                            <ul>
                                <li>Image is wavelength-rectified using the existing solution: <code>o = wav.correct(o, o.wave[nrows // 2])</code>.</li>
                                <li>The 2D spectrum is saved: <code>o.write(f'{name}_{targ["ID"]}_not_adjusted_2d.fits')</code>. A diagnostic plot of a central row might be generated.</li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ol>
            </p>
            <p><b>Widget State:</b> The collection of these final, wavelength-calibrated 2D extracted spectra is stored as <code>self.spec2d_out</code> by a callback mechanism.
            <br/><b>Parameters:</b> Settings for <code>findpeak</code>, <code>skyline</code> (thresholds, radii, polynomial degrees, linearity) within this step are configurable via "Tab 6: Parameters" under "Customize Multi Extract 2D Parameters".</p>
        </div>
        """

    def _get_1d_extraction_html(self):
        return """
        <div class='help-section-text'>
            <h5>1D Spectral Extraction</h5>
            <p><b>What it is:</b> This is the final step to obtain a 1D spectrum (flux versus wavelength) for each target. It involves tracing the object along the slit in the 2D extracted spectrum, defining sky regions, summing the object flux, and subtracting the sky background.</p>
            <p><b>GUI Actions:</b> In Tab 5, after "Extract Spectrum 2D" is complete (so <code>self.spec2d_out</code> is populated), click the "Extract Spectrum 1D" button.</p>
            <p><b>Details & Process:</b>
            <br/>The widget calls <code>processor.multi_extract1d(self.spec2d_out, targets=self.targets, ...)</code> which is based on the <code>multi_extract1d</code> function in the KOSMOS notebook: <code>spec1d = multi_extract1d(out)</code>.
            <br/>Inside <code>processor.multi_extract1d</code>:
            <ol>
                <li><b>Interactive UI in <code>param_area</code> of Tab 5:</b> Controls appear:
                    <ul>
                        <li>"1D Calibration choice" dropdown ('No sky adjustment', 'Sky adjustment').</li>
                        <li>"Extraction radius:" dropdown (e.g., 3-15 pixels).</li>
                        <li>"Run Extraction" button.</li>
                    </ul>
                </li>
                <li>When "Run Extraction" is clicked:
                    <ul>
                        <li>For each 2D spectrum (<code>spec2d_slice</code> from <code>self.spec2d_out</code>) and its target (<code>targ</code>):
                            <ul>
                                <li>Initialize trace: <code>trace_obj = spectra.Trace(...)</code> (parameters like <code>_degree</code>, <code>_sigdegree</code> from <code>paramwidget1</code>).</li>
                                <li>Find object peak: <code>peak, _ = trace_obj.findpeak(spec2d_slice, thresh=_thresh, ..., method=_method)</code> (parameters from <code>paramwidget1</code>). If no peak, skips.</li>
                                <li>Trace object: <code>trace_obj.trace(spec2d_slice, [peak[0]], skip=_skip, gaussian=True, ...)</code>.</li>
                                <li><b>Interactive Extraction Loop (UI in <code>param_area_1</code>):</b>
                                    <ul>
                                        <li>Extract with current radius: <code>rad = radius_dropdown.value</code>. Sky regions (<code>back_regions</code>) are defined relative to <code>rad</code> (e.g., <code>[[ -10 + (-1 * sky_width), -rad], [10 + sky_width, rad]]</code> where <code>sky_width = rad - 5</code>).
                                        <br/><code>spec1d = trace_obj.extract(spec2d_slice, rad=rad, back=back_regions, display=self.display)</code>.</li>
                                        <li>Assign wavelength: <code>spec1d.wave = spec2d_slice.wave[peak]</code>.</li>
                                        <li>Confirmation UI: "Are you satisfied with the extraction?" with "Yes"/"No" buttons appears in <code>param_area_1</code>.
                                            <ul>
                                                <li>If "Yes":
                                                    <ul>
                                                        <li>If "Sky adjustment" was chosen via dropdown: <code>wavcal = spectra.WaveCal(...)</code>, then <code>swav.skyline(spec1d, thresh=_thresh_sky, linear=_linear, file=_file, plot=_plot)</code> performs 1D sky line recalibration (params from <code>paramwidget1</code>).</li>
                                                        <li>Save 1D spectrum: <code>spec1d.write(filename, overwrite=True)</code>. Filename includes prefix like '1d_ad' or '2d_ad' and radius.</li>
                                                        <li>Plot 1D spectrum and sky.</li>
                                                        <li>Spectrum added to <code>extracted_1d_spectra</code> list. Proceeds to next target.</li>
                                                    </ul>
                                                </li>
                                                <li>If "No": Prints "Repeating extraction...", user can change radius in dropdown and the extraction for this slit repeats.</li>
                                            </ul>
                                        </li>
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ol>
            </p>
            <p><b>Widget State:</b> The list of final 1D spectra is stored as <code>self.spec1d_out</code>.
            <br/><b>Parameters:</b> Many parameters for <code>findpeak</code>, <code>trace</code>, <code>extract</code>, and <code>skyline</code> (thresholds, degrees, skip values, methods, sky line file, plot toggle) are configurable via "Tab 6: Parameters" under "Customize Multi Extract 1D Parameters".</p>
        </div>
        """

    def _get_tab4_parameters_html(self):
        return """
        <div class='help-section-text'>
            <h4>Purpose:</h4>
            <p>This tab provides advanced users with the ability to customize many of the underlying numerical parameters used by the core data processing functions (<code>calibrate_wavelength</code>, <code>multi_extract2d</code>, <code>multi_extract1d</code>) located within the <code>CofiProcessor1.py</code> module. These functions are invoked by the main action buttons in Tab 5 (Slits & Targets) and Tab 5 (Science & Extraction).</p>
            <h4>GUI Elements & Actions:</h4>
            <p>The tab is organized into collapsible sections using checkboxes. Ticking a checkbox reveals the parameters for the corresponding function. After adjusting values, click the "Commit [Function] Params" button for that section to save your changes. These committed parameters will then be used in subsequent tabs actions.</p>
            <ul>
                <li><b>Customize Calibrate Wavelength Parameters:</b>
                    <ul>
                        <li><b>Controls for:</b> <code>processor.calibrate_wavelength()</code>.</li>
                        <li><b>Key Parameters Exposed:</b>
                            <ul>
                                <li><code>Fit Degree</code> (<code>fit_degree</code> for initial 1D polynomial fit to reference spectrum).</li>
                                <li><code>Refit Degree (full slit)</code> (<code>wave_fit_degree_after_identify</code> for 2D polynomial fit across the slit).</li>
                                <li><code>Threshold</code> (<code>identify_thresh</code> for line identification peak significance).</li>
                                <li><code>WaveCal_spec</code> (<code>lamp_spec_file</code>, path to reference FITS WaveCal file, e.g., <code>'KOSMOS/KOSMOS_red_waves.fits'</code>).</li>
                                <li><code>Lamp File</code> (<code>lamp_file_for_identify</code>, path to arc lamp line list <code>.dat</code> file, e.g., <code>'new_wave_lamp/old_neon_red_center.dat'</code>).</li>
                                <li><code>Lags value (+/-)</code> (<code>lags_offset</code> for defining the search range in cross-correlation).</li>
                                <li><code>XMM Shift Multiplier</code> (<code>shift_multiplier</code> to convert XMM mask coordinate to initial pixel shift guess).</li>
                                <li><code>Recalibrate Wave (clobber)</code> (<code>use_clobber</code> / <code>weve_cal choice</code>, to force recalibration even if solution files exist).</li>
                                <li><code>Plot initial identify</code> (<code>plot_first_identify</code>) and <code>Plot interactive identify</code> (<code>plot_inter_identify</code>) toggles, allows you visually inspect calibration steps.</li>
                            </ul>
                        </li>
                        <li><b>Commit Cal_Wave Params (button):</b> Saves these settings to <code>self.param_config_widget.cw_params</code>.</li>
                    </ul>
                </li>
                <li><b>Customize Multi Extract 2D Parameters:</b>
                    <ul>
                        <li><b>Controls for:</b> <code>processor.multi_extract2d()</code>, specifically the optional skyline adjustment part.</li>
                        <li><b>Key Parameters Exposed:</b>
                            <ul>
                                <li><code>Thresh</code> (<code>_thresh</code> for <code>trace1.findpeak</code> and <code>wav.skyline</code>).</li>
                                <li><code>Radius</code> (<code>_rad</code> for defining rows to exclude object data during <code>wav.skyline</code>).</li>
                                <li><code>Back Percentile</code> (<code>_back_percentile</code> for <code>trace1.findpeak</code> sky estimation).</li>
                                <li><code>Degree</code> & <code>SigDegree</code> (<code>_degree</code>, <code>_sigdegree</code> for <code>trace1</code> fitting within skyline adjustment).</li>
                                <li><code>Linear Sky Adjust</code> (<code>_linear</code> for <code>wav.skyline</code> fitting method).</li>
                            </ul>
                        </li>
                        <li><b>Commit Ext2D Params (button):</b> Saves to <code>self.param_config_widget.m2d_params</code>.</li>
                    </ul>
                </li>
                <li><b>Customize Multi Extract 1D Parameters:</b>
                    <ul>
                        <li><b>Controls for:</b> <code>processor.multi_extract1d()</code>.</li>
                        <li><b>Key Parameters Exposed:</b>
                            <ul>
                                <li><code>Thresh Sky</code> (<code>_thresh_sky</code> for 1D <code>swav.skyline</code>).</li>
                                <li><code>Linear Sky Fit</code> (<code>_linear</code> for 1D <code>swav.skyline</code>).</li>
                                <li><code>Skip (trace)</code> (<code>_skip</code> for <code>trace_obj.trace</code>).</li>
                                <li><code>Degree (trace)</code> & <code>SigDegree (trace)</code> (<code>_degree</code>, <code>_sigdegree</code> for <code>trace_obj</code> fitting).</li>
                                <li><code>Thresh (findpeak)</code> (<code>_thresh</code> for <code>trace_obj.findpeak</code>).</li>
                                <li><code>Back Percentile (findpeak)</code> (<code>_back_percentile</code> for <code>trace_obj.findpeak</code>).</li>
                                <li><code>Method (findpeak)</code> (<code>_method</code> for percentile estimation in <code>findpeak</code>).</li>
                                <li><code>Skyline File</code> (<code>_file</code> for 1D <code>swav.skyline</code> line list, e.g., <code>'new_wave_lamp/skyline.dat'</code>).</li>
                                <li><code>Plot Sky Cal & Result</code> (<code>_plot</code> for 1D <code>swav.skyline</code> and final 1D spectrum plot).</li>
                            </ul>
                        </li>
                        <li><b>Commit Ext1D Params (button):</b> Saves to <code>self.param_config_widget.m1d_params</code>.</li>
                    </ul>
                </li>
            </ul>
            <p><b>Output:</b> Confirmation messages for committed parameters are displayed within this tab by the <code>FunctionParameterWidget1</code>'s own output area.</p>
            <h4>Important Note on Defaults:</h4>
            <p>All parameters have default values, initially set in <code>paramwidget1.py</code> and used by <code>processor1.py</code>. These defaults are generally sensible starting points based on experience. Modifying these parameters requires understanding their specific role and potential impact on the data reduction outcomes. It's advisable to consult the <code>astro-pyvista</code> library documentation, the KOSMOS MULTI-SLIT REDUCTION TUTORIAL, or the KOSMOS notebook for more context on each parameter if unsure.</p>
        </div>
        """

    def display(self):
        """
        Returns the main VBox widget containing all organized guide content.
        This VBox is intended to be displayed in a tab of the main CofiReductionWidget1.
        """
        return self.main_container
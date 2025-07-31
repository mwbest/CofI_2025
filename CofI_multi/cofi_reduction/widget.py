import os
import ast
import json
import numpy as np
import copy
import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd
from pyvista import imred, tv, stars, slitmask, image, spectra
from .processor import CofiProcessor
from .cofi_guide_widget import CofiGuideWidget
from .log import CofiLogger

# --------------------------------------------------------------------
# START OF CORRECTED SECTION
# --------------------------------------------------------------------
# Modern, theme-aware CSS
style_html = """
<style>
:root {
    --jp-widgets-font-family: 'Montserrat', sans-serif;
    --cofi-primary-color: #007acc;
    --cofi-secondary-color: #005a99;
    --cofi-accent-color: #00a8ff;
    --cofi-text-color: #000000;
    --cofi-bg-color: #ffffff;
    --cofi-bg-color-2: #f0f0f0;
    --cofi-border-color: #e0e0e0;
    --cofi-button-text-color: #ffffff;
    --cofi-error-color: #ff4d4d;
}

[data-jp-theme-light="false"] {
    --cofi-primary-color: #00a8ff;
    --cofi-secondary-color: #007acc;
    --cofi-accent-color: #00c8ff;
    --cofi-text-color: #e0e0e0;
    --cofi-bg-color: #1e1e1e;
    --cofi-bg-color-2: #2a2a2a;
    --cofi-border-color: #3c3c3c;
    --cofi-button-text-color: #ffffff;
}

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700&family=Roboto:wght@300;400;700&display=swap');

.cofi-main-title {
    text-align:center;
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 2.3em;
    margin: 15px 0 20px 0;
    color: var(--cofi-primary-color);
}

.widget-tab > .p-TabBar .p-TabBar-tab {
    background: var(--cofi-bg-color-2);
    color: var(--cofi-text-color);
    border: 2px solid var(--cofi-border-color);
    border-bottom: none;
    padding: 10px 20px;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    border-radius: 8px 8px 0 0;
    transition: background 0.3s ease, color 0.3s ease;
    z-index: 2;
}

.widget-tab > .p-TabBar .p-TabBar-tab:hover {
    background: var(--cofi-secondary-color);
    color: var(--cofi-button-text-color);
}

.widget-tab > .p-TabBar .p-TabBar-tab.p-mod-current {
    background: var(--cofi-primary-color);
    color: var(--cofi-button-text-color);
    border-color: var(--cofi-primary-color);
}

.widget-tab > .widget-tab-contents {
    background: var(--cofi-bg-color);
    border: 1px solid var(--cofi-primary-color);
    border-radius: 0 8px 8px 8px;
    padding: 20px;
    /*min-height: 300px;*/
    min-height: auto;
}

.sub-tab-title {
    font-size: 2.0em;
    font-weight: 560;
    margin: 0 0 15px 0;
    font-family: 'Montserrat', sans-serif;
    color: var(--cofi-secondary-color);
    border-bottom: 2px solid var(--cofi-border-color);
    padding-bottom: 8px;
}

.custom-button {
    background-color: var(--cofi-primary-color);
    color: var(--cofi-button-text-color);
    border: none;
    border-radius: 5px;
    padding: none;
    font-family: 'Montserrat', sans-serif;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    width: auto;
    transition: background-color 0.3s ease, transform 0.1s ease;
    /* Flexbox for perfect centering */
    display: flex;
    align-items: center;
    justify-content: center;
}
.custom-button:hover { box-shadow: 0 5px 12px rgba(46, 204, 113, 0.4); 
    background-color: var(--cofi-secondary-color);
    transform: translateY(-2px);
}
.custom-button.run-button { /* For main action buttons */
    font-weight: bold;
    padding: 10px 20px; /* Make run buttons slightly larger */
}
.custom-button.extraction-2d, .custom-button.extraction-1d,
.custom-button.yes, .custom-button.no { /* From processor styling */
      color: white !important; /* Ensure text is white on gradient buttons */
}

/* FIX: This selector now correctly targets the input/select elements
   within any widget that has the '.cofi-input-widget' class applied to it. */
.cofi-input-widget input, .cofi-input-widget select {
    background-color: var(--cofi-bg-color-2); /*--cofi-bg-color-2*/
    border: 4px solid var(--cofi-border-color); /*--cofi-border-color)*/
    border-radius: 5px;
    color: var(--cofi-text-color);
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    /*box-sizing: border-box; Important: includes padding in the total width */
    /*width: 100%;*/
    /*min-width: auto; Ensure a decent default width */
    margin: 3px; /*Add some margin */
    /*Text-align: center;*/
    border-bottom: none;
    /* --- Add these lines for vertical centering --- */
    height: auto;  /* Set a fixed height */
    padding: 0 0px;

}

/* FIX: This selector targets the focus state for the corrected rule above. */
.cofi-input-widget input:focus, .cofi-input-widget select:focus {
    border-color: var(--cofi-primary-color);
    box-shadow: 0 0 5px var(--cofi-accent-color);
    outline: none;
}


/* Ensure labels for ALL ipywidgets are themed and fully visible */
.widget-label, .widget-checkbox > label {
    color: var(--cofi-text-color);
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    margin-right: 8px;
    /* NEW: Force the label to take up as much space as it needs */
    width: max-content !important;
    min-width: max-content !important; /* Be at least as wide as the text */
    flex-shrink: 0;
    white-space: nowrap;
}


.custom-output-area, .interactive-processor-area {
    background-color: var(--cofi-bg-color-2);
    border: 1px solid var(--cofi-border-color);
    border-radius: 8px;
    padding: 15px;
    margin-top: 10px;
    min-height: auto;
    max-height: auto;
    overflow-y: auto;
    color: var(--cofi-text-color);
    font-family: 'Menlo', 'Consolas', 'Courier New', monospace;
    line-height: 1.6;
}
.interactive-processor-area { /* For areas where processor places its UI */
    min-height: auto; /* Ensure space for controls */
    font-family: 'Roboto', sans-serif; /* Match other UI text */
    margin-bottom:10px; /* Space below processor UI areas */
    border-color: var(--cofi-accent-color); /* Highlight these areas */
}


.cofi-guide-container {
    padding: 10px;
    /* This rule ensures text color is correctly inherited in dark mode */
    color: var(--cofi-text-color); 
}
.cofi-guide-container h2 {
    font-size: 1.9em !important;
    color: #00a8ff !important;
    border-bottom: 1px solid #3498db !important;
    padding-bottom: 8px !important;
    text-align: left !important;
}
.cofi-guide-container .widget-checkbox label {
    font-size: 1.3em !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 500 !important;
    /* Use the theme's text color for better dark/light mode compatibility */
    color: var(--cofi-text-color) !important;
    opacity: 0.9;
}
.cofi-guide-container .widget-vbox {
    margin: 8px 0 15px 25px !important;
    padding: 12px 18px !important;
    border-left: 4px solid #00a8ff !important;
    /* Use a semi-transparent version of the theme's secondary background color */
    background-color: rgba(128, 128, 128, 0.1) !important;
    border-radius: 0 8px 8px 0;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}

/* FIX: Increased specificity by prepending .cofi-guide-container */
.cofi-guide-container .help-section-text h4 {
    color: var(--cofi-secondary-color);
    font-family: 'Montserrat', sans-serif;
    margin-top: 12px;
    margin-bottom: 6px;
    font-size: 1.9em;
}

/* FIX: Added missing closing brace and increased specificity */
.cofi-guide-container .help-section-text h5 {
    color: var(--cofi-secondary-color);
    font-family: 'Montserrat', sans-serif;
    margin-top: 12px;
    margin-bottom: 6px;
    font-size: 1.9em;
}

/* FIX: Increased font size and specificity */
.cofi-guide-container .help-section-text p, 
.cofi-guide-container .help-section-text li {
    /* Use the main text color from the theme variables */
    color: var(--cofi-text-color); 
    font-family: 'Roboto', sans-serif;
    line-height: 1.65;
    /* MODIFIED: Increased font size for readability. Adjust as needed. */
    font-size: 20px;
}

/* FIX: Increased specificity */
.cofi-guide-container .help-section-text code {
    padding: 3px 6px;
    border-radius: 5px;
    background-color: var(--cofi-bg-color-2);
    border: 1px solid var(--cofi-border-color);
    color: var(--cofi-accent-color);
    font-family: 'Menlo', 'Consolas', monospace;
    font-size: 0.95em; /* Slightly smaller than parent text for inline code */
}

/* FIX: Increased specificity */
.cofi-guide-container .help-section-text strong {
    color: var(--cofi-primary-color);
    font-weight: bold;
}

/* FIX: Increased specificity */
.cofi-guide-container .help-section-text ul {
    padding-left: 22px;
    list-style-type: disc;
}

/* FIX: Increased specificity */
.cofi-guide-container .help-section-text hr {
    border: 1px solid var(--cofi-border-color);
    margin: 25px 0;
}

</style>
"""
# --------------------------------------------------------------------
# END OF CORRECTED SECTIONcofi-input-widget
# --------------------------------------------------------------------

# Display the CSS style block when the module loads
def load_style():
    display(widgets.HTML(style_html))

custom_input_layout = widgets.Layout(width='auto')

def get_srt_or_list(widget_value):
    cleaned_value = widget_value.strip()
    if cleaned_value.startswith('[') and cleaned_value.endswith(']'):
        try:
            return ast.literal_eval(cleaned_value)
        except (ValueError, SyntaxError):
            return cleaned_value
    else:
        return cleaned_value

class CofiReductionWidget:
    def __init__(self, display_enabled=True):
        load_style()
        self.display_enabled = display_enabled
        self.tv = tv.TV() if self.display_enabled else None
        self.guide_widget = CofiGuideWidget()
        self.processor = CofiProcessor(display_1=self.tv)

        # Internal state attributes
        self.red = None
        self.bias_frame = None
        self.dark_frame = None
        self.flat_frame = None
        self.arcs_frame = None
        self.trace = None
        self.targets = None
        self.reduced_frame = None
        self.spec2d_out = None
        self.spec1d_out = None
        self.arcec = None
        self.full_trace = None
        self.full_targets = None

        self._create_widgets()
        self._setup_ui()
        self.logger = CofiLogger()
        self._attach_handlers()
        self.widget_map = None

    def _create_widgets(self):
        # --- Main Data Input ---
        self.folder_path_input = widgets.Text(placeholder='e.g., UT230909', description='Folder Path:',style={'description_width': 'initial'},
                                                layout= custom_input_layout)
        self.log_file_input = widgets.Text(placeholder='e.g., M5real.0008', description='Log file name:',style={'description_width': 'initial'},
                                                layout= custom_input_layout)
        self.read_folder_button = widgets.Button(description='Read Folder', icon='folder-open',style={'description_width': 'initial'},
                                                layout= custom_input_layout)
        self.folder_path_input.add_class('cofi-input-widget')
        self.log_file_input.add_class('cofi-input-widget')
        self.read_folder_button.add_class('custom-button')

        # --- Log File Loader ---
        self.log_uploader = widgets.FileUpload(
            accept='.txt',
            multiple=False,
            description='Upload Log File',
            style={'description_width': 'initial'},
            layout=custom_input_layout
        )
        self.load_log_button = widgets.Button(
            description='Apply Settings from Log',
            icon='upload',
            style={'description_width': 'initial'},
            layout=custom_input_layout
        )
        self.log_uploader.add_class('cofi-input-widget')
        self.load_log_button.add_class('custom-button')
        

        # --- Calibration: Bias ---
        self.bias_files_input = widgets.Text(placeholder='e.g., 74,75,76', description='Bias Frames:',
                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.bias_type_dropdown = widgets.Dropdown(options=['median', 'mean', 'reject'], value='median', description='Combine Type:',
                                                   style={'description_width': 'initial'},layout= custom_input_layout)
        self.bias_sigreject_input = widgets.FloatText(value=5.0, description='Sigma Reject:',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.bias_display = widgets.Checkbox(value=False, description='Display indivitual bias')
        self.bias_trim_checkbox = widgets.Checkbox(value=False, description='Trim bias')
        self.compute_bias_button = widgets.Button(description='Compute Bias', icon='cogs',style={'description_width': 'initial'},
                                                 layout= custom_input_layout)
        self.bias_files_input.add_class('cofi-input-widget')
        self.bias_type_dropdown.add_class('cofi-input-widget')
        self.bias_sigreject_input.add_class('cofi-input-widget')
        self.bias_display.add_class('cofi-input-widget')
        self.bias_trim_checkbox.add_class('cofi-input-widget')
        self.compute_bias_button.add_class('custom-button')
        self.compute_bias_button.add_class('run-button')

        # --- Calibration: Dark ---
        self.dark_files_input = widgets.Text(placeholder='e.g., 94,95,96', description='Dark Frames:',
                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.dark_type_dropdown = widgets.Dropdown(options=['median', 'mean', 'reject'], value='median', description='Combine Type:',
                                                   style={'description_width': 'initial'},layout= custom_input_layout)
        self.dark_sigreject_input = widgets.FloatText(value=5.0, description='Sigma Reject:',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.dark_display = widgets.Checkbox(value=False, description='Display indivitual dark')
        self.dark_trim_checkbox = widgets.Checkbox(value=False, description='Trim darks')
        self.apply_bias_checkbox = widgets.Checkbox(value=True, description='Apply bias')
        self.dark_clip_input = widgets.FloatText(value=0, description='Clip (x Uncertainty):')
        self.compute_dark_button = widgets.Button(description='Compute Dark', icon='cogs',style={'description_width': 'initial'},
                                                 layout= custom_input_layout)
        self.dark_files_input.add_class('cofi-input-widget')
        self.dark_type_dropdown.add_class('cofi-input-widget')
        self.dark_sigreject_input.add_class('cofi-input-widget')
        self.dark_display.add_class('cofi-input-widget')
        self.dark_trim_checkbox.add_class('cofi-input-widget')
        self.apply_bias_checkbox.add_class('cofi-input-widget')
        self.dark_clip_input.add_class('cofi-input-widget')
        self.compute_dark_button.add_class('custom-button')
        self.compute_dark_button.add_class('run-button')

        # --- Calibration: Flat ---
        self.flat_files_input = widgets.Text(placeholder='e.g., 21,22', description='Flat Frames:',
                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.flat_type_dropdown = widgets.Dropdown(options=['median', 'mean', 'reject'], value='median', description='Combine Type:',
                                                  style={'description_width': 'initial'}, layout= custom_input_layout)
        self.flat_sigreject_input = widgets.FloatText(value=5.0, description='Sigma Reject:',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.flat_spec_checkbox = widgets.Checkbox(value=True, description='Spectral Flat')
        self.apply_dark_bias_checkbox = widgets.Checkbox(value=True, description='Apply bias')
        self.apply_dark_checkbox = widgets.Checkbox(value=True, description='Apply dark')
        self.flat_display = widgets.Checkbox(value=False, description='Display indivitual flats')
        self.flat_littrow_checkbox = widgets.Checkbox(value=False, description='Flat littrow')
        self.flat_trim_checkbox = widgets.Checkbox(value=False, description='Trim flats')
        self.flat_width_input = widgets.IntText(value=101, description='Window Width:',
                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.flat_normalize_checkbox = widgets.Checkbox(value=True, description='Normalize Flat')
        self.flat_snmin_input = widgets.FloatText(value=50.0, description='S/N Min (for Norm):',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.compute_flat_button = widgets.Button(description='Compute Flat', icon='cogs',style={'description_width': 'initial'},
                                                 layout= custom_input_layout)
        self.flat_files_input.add_class('cofi-input-widget')
        self.flat_type_dropdown.add_class('cofi-input-widget')
        self.flat_sigreject_input.add_class('cofi-input-widget')
        self.flat_spec_checkbox.add_class('cofi-input-widget')
        self.apply_dark_bias_checkbox.add_class('cofi-input-widget')
        self.apply_dark_checkbox.add_class('cofi-input-widget')
        self.flat_display.add_class('cofi-input-widget')
        self.flat_littrow_checkbox.add_class('cofi-input-widget')
        self.flat_trim_checkbox.add_class('cofi-input-widget')
        self.flat_width_input.add_class('cofi-input-widget')
        self.flat_normalize_checkbox.add_class('cofi-input-widget')
        self.flat_snmin_input.add_class('cofi-input-widget')
        self.compute_flat_button.add_class('custom-button')
        self.compute_flat_button.add_class('run-button')

        # --- Calibration: Arcs ---
        self.arc_files_input = widgets.Text(placeholder='e.g., 23,24', description='Arc Frames:',
                                           style={'description_width': 'initial'},layout= custom_input_layout)
        self.arc_return_list_checkbox = widgets.Checkbox(value=False, description='Returns a list')
        self.compute_arcs_button = widgets.Button(description='Compute Arcs', icon='cogs',style={'description_width': 'initial'},
                                                 layout= custom_input_layout)
        self.arc_files_input.add_class('cofi-input-widget')
        self.arc_return_list_checkbox.add_class('cofi-input-widget')
        self.compute_arcs_button.add_class('custom-button')
        self.compute_arcs_button.add_class('run-button')

        # --- Slits & Targets: Find Slits ---
        self.slit_flat_file_input = widgets.Text(placeholder='e.g., 21', description='Flat Frame for Slits:',
                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.kms_file_input = widgets.Text(placeholder='path/to/mask.kms', description='KMS File:',
                                          style={'description_width': 'initial'},layout= custom_input_layout)
        self.findslits_smooth_input = widgets.FloatText(value=3.0, description='Smooth Radius (FindSlits):',
                                                       style={'description_width': 'initial'},layout= custom_input_layout)
        self.findslits_thresh_input = widgets.FloatText(value=0.5, description='Edge Threshold (FindSlits):',
                                                       style={'description_width': 'initial'},layout= custom_input_layout)
        self.findslits_degree_input = widgets.IntText(value=2, description='Fit Degree (FindSlits):',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.findslits_cent_input = widgets.Text(value='None', description='spectra center location (if known):',
                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.findslits_sn_checkbox = widgets.Checkbox(value=True, description='Use S/N for Edges (FindSlits)',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.findslits_skip_input = widgets.IntText(value=50, description='Pixels to skip (FindSlits):',
                                                   style={'description_width': 'initial'},layout= custom_input_layout)
        self.find_slits_button = widgets.Button(description='Find Slits', icon='search',style={'description_width': 'initial'},
                                               layout= custom_input_layout)
        self.update_headers_button = widgets.Button(description='Update Arc Headers', icon='tags',style={'description_width': 'initial'},
                                                   layout= custom_input_layout)
        self.slit_flat_file_input.add_class('cofi-input-widget')
        self.kms_file_input.add_class('cofi-input-widget')
        self.findslits_smooth_input.add_class('cofi-input-widget')
        self.findslits_thresh_input.add_class('cofi-input-widget')
        self.findslits_degree_input.add_class('cofi-input-widget')
        self.findslits_cent_input.add_class('cofi-input-widget')
        self.findslits_sn_checkbox.add_class('cofi-input-widget')
        self.findslits_skip_input.add_class('cofi-input-widget')
        self.find_slits_button.add_class('custom-button')
        self.find_slits_button.add_class('run-button')
        self.update_headers_button.add_class('custom-button')

        # --- Slits & Targets: Filter Slits ---
        self.filter_method_dropdown = widgets.Dropdown(options=['Index', 'ID', 'Name'], value='Index', description='Filter By:',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.filter_values_input = widgets.Text(placeholder='e.g., 6,7,9', description='Values:',
                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.filter_slits_button = widgets.Button(description='Filter Slits', icon='filter',style={'description_width': 'initial'},
                                                 layout= custom_input_layout)
        self.reset_filter_button = widgets.Button(description='Reset Filter', icon='refresh',style={'description_width': 'initial'},
                                                 layout= custom_input_layout)
        self.filter_method_dropdown.add_class('cofi-input-widget')
        self.filter_values_input.add_class('cofi-input-widget')
        self.filter_slits_button.add_class('custom-button')
        self.reset_filter_button.add_class('custom-button')

        # --- Science: Reduce ---
        self.science_file_input = widgets.Text(placeholder='e.g., 20', description='Science Frame:',
                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_crbox_input = widgets.Text(value='lacosmic', description='Cosmic Ray Algo:', style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_crsig_input = widgets.FloatText(value=5.0, description='CR Sigma (lacosmic):',
                                                   style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_objlim_input = widgets.FloatText(value=5.0, description='CR Object Limit (lacosmic):',
                                                    style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_channel_input = widgets.Text(value='None',  placeholder='int, default= None', description='Specified channel if multi-channel:',style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_scat_input = widgets.Text(value='None',  placeholder='int, default= None', description='If specified, do scattered light correction:',style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_badpix_input = widgets.Text(value='None',  placeholder='int, default= None', description='if specified, set masked pixels to specified value:',style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_trim_checkbox = widgets.Checkbox(value=True, description='Trim image after calibration')
        self.reduce_utr_checkbox = widgets.Checkbox(value=False, description='utr')
        self.reduce_sigfrac_input = widgets.FloatText(value=0.3, description='sigfrac:',style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_ext_input = widgets.IntText(value=0, description='ext:',style={'description_width': 'initial'},layout= custom_input_layout)
        self.use_calibrations_checkbox = widgets.Checkbox(value=False, description='Apply Calibrations (Bias/Dark/Flat)',style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_appy_bias_checkbox=widgets.Checkbox(value=True, description='Apply bias')
        self.reduce_appy_dark_checkbox=widgets.Checkbox(value=True, description='Apply darks')
        self.reduce_appy_flat_checkbox=widgets.Checkbox(value=False, description='Apply flats')
        
        self.reduce_seeing_input = widgets.FloatText(value=2.0, description='Seeing (for solve):',style={'description_width': 'initial'},layout= custom_input_layout)
        self.reduce_solve_checkbox = widgets.Checkbox(value=False, description='Attempt Plate Solve')
        self.reduce_button = widgets.Button(description='Reduce Science Frame', icon='rocket',style={'description_width': 'initial'},
                                           layout= custom_input_layout)
        self.science_file_input.add_class('cofi-input-widget')
        self.reduce_crbox_input.add_class('cofi-input-widget')
        self.reduce_crsig_input.add_class('cofi-input-widget')
        self.reduce_objlim_input.add_class('cofi-input-widget')
        self.reduce_channel_input.add_class('cofi-input-widget')
        self.reduce_scat_input.add_class('cofi-input-widget')
        self.reduce_badpix_input.add_class('cofi-input-widget')
        self.reduce_trim_checkbox.add_class('cofi-input-widget')
        self.reduce_utr_checkbox.add_class('cofi-input-widget')
        self.reduce_sigfrac_input.add_class('cofi-input-widget')
        self.reduce_ext_input.add_class('cofi-input-widget')
        self.use_calibrations_checkbox.add_class('cofi-input-widget')
        self.reduce_appy_bias_checkbox.add_class('cofi-input-widget')
        self.reduce_appy_dark_checkbox.add_class('cofi-input-widget')
        self.reduce_appy_flat_checkbox.add_class('cofi-input-widget')
        self.reduce_seeing_input.add_class('cofi-input-widget')
        self.reduce_solve_checkbox.add_class('cofi-input-widget')
        self.reduce_button.add_class('custom-button')
        self.reduce_button.add_class('run-button')

        # --- Science: Wave Calibration ---
        self.wavecal_clobber_checkbox = widgets.Checkbox(value=False, description='Recalibrate (Clobber)')
        self.wavecal_lamp_spec_input = widgets.Text(value='KOSMOS/KOSMOS_red_waves.fits', description='Lamp Spec File (ref):',style={'description_width': 'initial'},layout= custom_input_layout)
        # self.wavecal_lamp_lines_input = widgets.Text(value='new_wave_lamp/old_neon_red_center.dat', description='Lamp Line List (ID):',style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_fit_degree_input = widgets.IntText(value=3, description='Initial Fit Degree (ref):',style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_refit_degree_input = widgets.IntText(value=5, description='Refit Degree (Full Slit):',
                                                         style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_shift_multiplier_input = widgets.FloatText(value=-22.5, description='XMM Shift Multiplier:',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_arc_line_input = widgets.IntText(value=19, description='Arc lines position:',
                                                                       style={'description_width': 'initial'},layout= custom_input_layout)
        
        self.wavecal_clobber_checkbox.add_class('cofi-input-widget')
        self.wavecal_lamp_spec_input.add_class('cofi-input-widget')
        # self.wavecal_lamp_lines_input.add_class('cofi-input-widget')
        self.wavecal_fit_degree_input.add_class('cofi-input-widget')
        self.wavecal_refit_degree_input.add_class('cofi-input-widget')
        self.wavecal_shift_multiplier_input.add_class('cofi-input-widget')
        self.wavecal_arc_line_input.add_class('cofi-input-widget')
        # --- Advanced Identify Parameters ---
        self.wavecal_id_thresh_input = widgets.FloatText(value=10.0, description='ID Thresh (peaks):',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_rad_input = widgets.IntText(value=5, description='ID Radius (peaks):')
        self.wavecal_id_maxshift_input = widgets.FloatText(value=1.e10, description='ID Max Shift:',
                                                          style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_sample_input = widgets.IntText(value=10, description='Sampling value:',
                                                          style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_re_sample_input = widgets.IntText(value=2, description='Correcting position:',
                                                          style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_weak_weight_input = widgets.FloatText(value=0.5, description='Weak weght identifier:',
                                                          style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_arc_line_position_input = widgets.IntText(value=2, description='Arc line position:',
                                                          style={'description_width': 'initial'},layout= custom_input_layout)
        
        self.wavecal_id_fit_checkbox = widgets.Checkbox(value=True, description='ID Fit Peaks')
        self.wavecal_id_sky_checkbox = widgets.Checkbox(value=False, description='ID Sky Lines')
        self.wavecal_id_inter_checkbox = widgets.Checkbox(value=False, description='ID Interactive')
        self.wavecal_id_verbose_checkbox = widgets.Checkbox(value=False, description='ID Verbose')
        self.wavecal_id_pixplot_checkbox = widgets.Checkbox(value=False, description='ID Pixel Plot')
        self.wavecal_id_domain_checkbox = widgets.Checkbox(value=False, description='ID Domain Plot')
        self.wavecal_id_plot_checkbox = widgets.Checkbox(value=True, description='ID Enable Plots') 
        self.wavecal_id_plotinter_checkbox = widgets.Checkbox(value=True, description='ID Enable Plotinter')
        self.wavecal_id_file_input = widgets.Text(value='new_wave_lamp/old_neon_red_center.dat', description='Lamp Line List (ID):',
                                                  style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_disp_input = widgets.Text(value='None', description='ID Dispersion :', placeholder='Optional',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_xmin_input = widgets.Text(value='None', description='ID Plot X-Min:', placeholder='Optional',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_xmax_input = widgets.Text(value='None', description='ID Plot X-Max:', placeholder='Optional',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_rows_input = widgets.Text(value='None', description='ID Rows (e.g., 100:200):', placeholder='Optional',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_nskip_input = widgets.Text(value='None', description='ID NSkip:', placeholder='Optional')
        self.wavecal_id_orders_input = widgets.Text(value='None', description='ID Orders (e.g., 1,2):', placeholder='Optional',
                                                   style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_lags_input = widgets.IntText(value=50, description='ID Lags:',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_wav_input = widgets.Text(value='None', description='ID Wavelength array/image:', placeholder='Optional',
                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_wref_input = widgets.Text(value='None', description='ID WRef File:', placeholder='Optional',
                                                 style={'description_width': 'initial'},layout= custom_input_layout)
        self.wavecal_id_file_input.add_class('cofi-input-widget')
        self.wavecal_id_thresh_input.add_class('cofi-input-widget')
        self.wavecal_id_rad_input.add_class('cofi-input-widget')
        self.wavecal_id_maxshift_input.add_class('cofi-input-widget')
        self.wavecal_id_sample_input.add_class('cofi-input-widget')
        self.wavecal_id_re_sample_input.add_class('cofi-input-widget') 
        self.wavecal_id_weak_weight_input.add_class('cofi-input-widget') 
        self.wavecal_id_arc_line_position_input.add_class('cofi-input-widget')      
        self.wavecal_id_fit_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_sky_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_inter_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_verbose_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_pixplot_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_domain_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_plot_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_plotinter_checkbox.add_class('cofi-input-widget')
        self.wavecal_id_disp_input.add_class('cofi-input-widget')
        self.wavecal_id_xmin_input.add_class('cofi-input-widget')
        self.wavecal_id_xmax_input.add_class('cofi-input-widget')
        self.wavecal_id_rows_input.add_class('cofi-input-widget')
        self.wavecal_id_nskip_input.add_class('cofi-input-widget')
        self.wavecal_id_orders_input.add_class('cofi-input-widget')
        self.wavecal_id_lags_input.add_class('cofi-input-widget')
        self.wavecal_id_wav_input.add_class('cofi-input-widget')
        self.wavecal_id_wref_input.add_class('cofi-input-widget')

        # --- Action Buttons ---
        self.run_wave_cal_button = widgets.Button(description='Run Wavelength Calibration', icon='wave-square',style={'description_width': 'initial'},layout= custom_input_layout)
        self.run_shift_check_button = widgets.Button(description='Check Shift', icon='search-plus',style={'description_width': 'initial'},
                                                    layout= custom_input_layout)
        self.run_wave_cal_button.add_class('custom-button')
        self.run_wave_cal_button.add_class('run-button')
        self.run_shift_check_button.add_class('custom-button')
        
        # --- Science: 2D Extraction ---
        self.start_extract2d_button = widgets.Button(description='Setup & Run 2D Extraction', icon='layer-group',style={'description_width': 'initial'},layout= custom_input_layout)
        self.start_extract2d_button.add_class('custom-button')
        self.start_extract2d_button.add_class('run-button')
        
        # -- Trace Parameters --
        self.extract2d_trace_degree_input = widgets.IntText(value=3, description='Trace Degree:',
                                                           style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_sigdegree_input = widgets.IntText(value=3, description='Trace Sigma Degree:',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_type_input = widgets.Text(value='Polynomial1D', description='Trace Type:',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_rad_input = widgets.IntText(value=5, description='Trace Radius:',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_lags_input = widgets.Text(value='-39,39', description='Trace Lags:',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_transpose_checkbox = widgets.Checkbox(value=False, description='Trace Transpose')
        self.extract2d_trace_pix0_input = widgets.IntText(value=0, description='Trace Pix0:',
                                                         style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_sc0_input = widgets.Text(value='None', description='Trace sc0:', placeholder='Optional',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_rows_input = widgets.Text(value='None', description='Trace Rows:', placeholder='Optional',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_channel_input = widgets.Text(value='None', description='Trace Channel:', placeholder='Optional',
                                                         style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_inst_input = widgets.Text(value='None', description='Trace Instrument:', placeholder='Optional',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_file_input = widgets.Text(value='None', description='Trace File:', placeholder='Optional',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_spectrum_input = widgets.Text(value='None', description='Trace Spectrum:', placeholder='Optional',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_model_input = widgets.Text(value='None', description='Trace Model:', placeholder='Optional',
                                                       style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_trace_hdu_input = widgets.IntText(value=1, description='Trace HDU:')
        self.extract2d_trace_degree_input.add_class('cofi-input-widget')
        self.extract2d_trace_sigdegree_input.add_class('cofi-input-widget')
        self.extract2d_trace_type_input.add_class('cofi-input-widget')
        self.extract2d_trace_rad_input.add_class('cofi-input-widget')
        self.extract2d_trace_lags_input.add_class('cofi-input-widget')
        self.extract2d_trace_transpose_checkbox.add_class('cofi-input-widget')
        self.extract2d_trace_pix0_input.add_class('cofi-input-widget')
        self.extract2d_trace_sc0_input.add_class('cofi-input-widget')
        self.extract2d_trace_rows_input.add_class('cofi-input-widget')
        self.extract2d_trace_channel_input.add_class('cofi-input-widget')
        self.extract2d_trace_inst_input.add_class('cofi-input-widget')
        self.extract2d_trace_file_input.add_class('cofi-input-widget')
        self.extract2d_spectrum_input.add_class('cofi-input-widget')
        self.extract2d_trace_model_input.add_class('cofi-input-widget')
        self.extract2d_trace_hdu_input.add_class('cofi-input-widget')

        # -- FindPeak Parameters --
        self.extract2d_findpeak_thresh_input = widgets.FloatText(value=10.0, description='FindPeak Thresh:',
                                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_backperc_input = widgets.IntText(value=10, description='FindPeak Back %:',
                                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_width_input = widgets.Text(value='None', description='FindPeak Width:',
                                                             style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_smooth_input = widgets.FloatText(value=5.0, description='FindPeak Smooth:',
                                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_sc0_input = widgets.Text(value='None', description='FindPeak sc0:', placeholder='Optional',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_method_input = widgets.Text(value='linear', description='FindPeak Method:',
                                                           style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_diff_input = widgets.IntText(value=10000, description='FindPeak Diff:',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_bundle_input = widgets.IntText(value=10000, description='FindPeak Bundle:',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_findpeak_sort_checkbox = widgets.Checkbox(value=True, description='FindPeak Sort')
        self.extract2d_findpeak_plot_checkbox = widgets.Checkbox(value=False, description='FindPeak Plot')
        self.extract2d_findpeak_verbose_checkbox = widgets.Checkbox(value=False, description='FindPeak Verbose')
        self.extract2d_findpeak_thresh_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_backperc_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_width_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_smooth_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_sc0_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_method_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_diff_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_bundle_input.add_class('cofi-input-widget')
        self.extract2d_findpeak_sort_checkbox.add_class('cofi-input-widget')
        self.extract2d_findpeak_verbose_checkbox.add_class('cofi-input-widget')
        self.extract2d_findpeak_plot_checkbox.add_class('cofi-input-widget')

        # -- Skyline Parameters --
        self.extract2d_skyline_thresh_input = widgets.FloatText(value=10.0, description='Skyline Thresh:',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_skyline_obj_rad_input = widgets.IntText(value=5, description='Skyline rad for rows',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_correcting_value_input = widgets.IntText(value=2, description='Correcting position',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        
        self.extract2d_skyline_file_input = widgets.Text(value='skyline.dat', description='Skyline File:',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_skyline_rows_input = widgets.Text(value='None', description='Skyline Rows:', placeholder='Optional',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_skyline_linear_checkbox = widgets.Checkbox(value=False, description='Skyline Linear Fit')
        self.extract2d_skyline_inter_checkbox = widgets.Checkbox(value=True, description='Skyline Interactive')
        self.extract2d_skyline_thresh_input.add_class('cofi-input-widget')
        self.extract2d_skyline_obj_rad_input.add_class('cofi-input-widget')
        self.extract2d_correcting_value_input.add_class('cofi-input-widget')
        self.extract2d_skyline_file_input.add_class('cofi-input-widget')
        self.extract2d_skyline_rows_input.add_class('cofi-input-widget')
        self.extract2d_skyline_linear_checkbox.add_class('cofi-input-widget')
        self.extract2d_skyline_inter_checkbox.add_class('cofi-input-widget')

        # -- extract2d() Parameters --
        self.extract2d_rows_input = widgets.Text(value='None',description='Extract Rows:', placeholder='Optional',
                                                style={'description_width': 'initial'},layout= custom_input_layout) 
        self.extract2d_buffer_input = widgets.IntText(value=0, description='Extract Buffer:',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self._2d_flat_field_checkbox = widgets.Checkbox(value=True, description='Apply flat:',
                                                     style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract2d_rows_input.add_class('cofi-input-widget')
        self.extract2d_buffer_input.add_class('cofi-input-widget')
        self._2d_flat_field_checkbox.add_class('cofi-input-widget')

        # --- Science: 1D Extraction ---
        self.start_extract1d_button = widgets.Button(description='Setup & Run 1D Extraction', icon='chart-bar',style={'description_width': 'initial'},layout= custom_input_layout)
        self.start_extract1d_button.add_class('custom-button')
        self.start_extract1d_button.add_class('run-button')
        
        # -- Main 1D Parameters --
        # self.extract1d_plot_spectra_checkbox = widgets.Checkbox(value=True, description='Plot Final 1D Spectra')
        self.extract1d_back_input = widgets.IntText(value=10, description='Bkg. Regions:', placeholder='e.g., [[-15,-7],[7,15]]',
                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_fit_checkbox = widgets.Checkbox(value=False, description='Fit Profile')
        self.extract1d_old_checkbox = widgets.Checkbox(value=False, description='Use Old Extraction')
        self.extract1d_medfilt_input = widgets.Text(value='None', description='Median Filter:', placeholder='0 to disable',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_nout_input = widgets.Text(value='None', description='N-out:', placeholder='Optional',
                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_threads_input = widgets.IntText(value=0, description='Threads:', placeholder='0 for auto',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_sky_width_input = widgets.IntText(value=10, description='Sky width:',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)

        # self.extract1d_plot_spectra_checkbox.add_class('cofi-input-widget')
        self.extract1d_back_input.add_class('cofi-input-widget')
        self.extract1d_fit_checkbox.add_class('cofi-input-widget')
        self.extract1d_old_checkbox.add_class('cofi-input-widget')
        self.extract1d_medfilt_input.add_class('cofi-input-widget')
        self.extract1d_nout_input.add_class('cofi-input-widget')
        self.extract1d_threads_input.add_class('cofi-input-widget')
        self.extract1d_sky_width_input.add_class('cofi-input-widget')

        # -- Trace Class Constructor Parameters (1D) --
        self.extract1d_trace_degree_input = widgets.IntText(value=3, description='Trace Degree:',
                                                           style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_sigdegree_input = widgets.IntText(value=3, description='Trace Sigma Degree:',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_file_input = widgets.Text(value='None', description='Trace File:', placeholder='Optional',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_inst_input = widgets.Text(description='Trace Instrument:', placeholder='Optional',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_type_input = widgets.Text(value='Polynomial1D', description='Trace Model Type:',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_pix0_input = widgets.IntText(value=0, description='Trace Pix0:',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_rad_input = widgets.IntText(value=5, description='Trace Radius:',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_sc0_input = widgets.Text(value='None', description='Trace sc0:', placeholder='Optional',
                                                           style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_rows_input = widgets.Text(value='None',description='Trace Rows:', placeholder='Optional',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_transpose_checkbox = widgets.Checkbox(value=False, description='Trace Transpose')
        self.extract1d_trace_class_lags_input = widgets.Text(value='-39,39', description='Trace Lags:',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_channel_input = widgets.Text(value='None', description='Trace Channel:', placeholder='Optional',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_hdu_input = widgets.IntText(value=1, description='Trace HDU:',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_model_input = widgets.Text(value='None', description='Trace Model:', placeholder='Optional',
                                                       style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_class_spectrum_input = widgets.Text(value='None', description='Trace Spectrum:', placeholder='Optional',
                                                      style={'description_width': 'initial'},layout= custom_input_layout)
        
        self.extract1d_trace_degree_input.add_class('cofi-input-widget')
        self.extract1d_trace_sigdegree_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_file_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_inst_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_type_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_pix0_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_rad_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_sc0_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_rows_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_transpose_checkbox.add_class('cofi-input-widget')
        self.extract1d_trace_class_lags_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_channel_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_hdu_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_model_input.add_class('cofi-input-widget')
        self.extract1d_trace_class_spectrum_input.add_class('cofi-input-widget')

        # -- FindPeak Method Parameters (1D) --
        self.extract1d_findpeak_thresh_input = widgets.FloatText(value=50.0, description='FindPeak Thresh:',
                                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_backperc_input = widgets.IntText(value=10, description='FindPeak Back %:',
                                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_width_input = widgets.Text(value='None', description='FindPeak Width:',placeholder='Optional',
                                                          style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_method_input = widgets.Text(value='linear', description='FindPeak Method:',
                                                           style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_smooth_input = widgets.FloatText(value=5.0, description='FindPeak Smooth:',
                                                                style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_sc0_input = widgets.Text(value='None', description='FindPeak sc0:', placeholder='Optional',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_sort_checkbox = widgets.Checkbox(value=True, description='Sort Peaks')
        self.extract1d_findpeak_diff_input = widgets.IntText(value=10000, description='FindPeak Diff:',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_bundle_input = widgets.IntText(value=10000, description='FindPeak Bundle:',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_findpeak_verbose_checkbox = widgets.Checkbox(value=False, description='FindPeak Verbose')
        self.extract1d_findpeak_plot_checkbox = widgets.Checkbox(value=False, description='FindPeak Plot')
        self.extract1d_findpeak_thresh_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_backperc_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_width_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_method_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_smooth_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_sc0_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_sort_checkbox.add_class('cofi-input-widget')
        self.extract1d_findpeak_diff_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_bundle_input.add_class('cofi-input-widget')
        self.extract1d_findpeak_verbose_checkbox.add_class('cofi-input-widget')
        self.extract1d_findpeak_plot_checkbox.add_class('cofi-input-widget')
        
        # -- Trace Method Parameters (1D) --
        self.extract1d_trace_skip_input = widgets.IntText(value=20, description='Trace Skip:',
                                                         style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_method_rad_input = widgets.IntText(value=5, description='Trace Method Radius:',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_method_thresh_input = widgets.FloatText(value=20.0, description='Trace Method Thresh:',
                                                                    style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_method_sc0_input = widgets.Text(value='None', description='Trace Method sc0:', placeholder='Optional',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_method_srows_input = widgets.Text(value='None', description='Trace Method srows:', placeholder='Optional',
                                                            style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_method_index_input = widgets.Text(value='None', description='Trace Method Index:', placeholder='Optional',
                                                              style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_trace_method_gaussian_checkbox = widgets.Checkbox(value=True, description='Use Gaussian Fit')
        self.extract1d_trace_method_verbose_checkbox = widgets.Checkbox(value=False, description='Trace Method Verbose')
        self.extract1d_trace_method_plot_checkbox = widgets.Checkbox(value=True, description='Use Gaussian Fit')
        self.extract1d_trace_skip_input.add_class('cofi-input-widget')
        self.extract1d_trace_method_rad_input.add_class('cofi-input-widget')
        self.extract1d_trace_method_thresh_input.add_class('cofi-input-widget')
        self.extract1d_trace_method_sc0_input.add_class('cofi-input-widget')
        self.extract1d_trace_method_srows_input.add_class('cofi-input-widget')
        self.extract1d_trace_method_index_input.add_class('cofi-input-widget')
        self.extract1d_trace_method_gaussian_checkbox.add_class('cofi-input-widget')
        self.extract1d_trace_method_verbose_checkbox.add_class('cofi-input-widget')
        
        # -- Skyline Parameters (1D) --
        self.extract1d_skyline_thresh_input = widgets.FloatText(value=12.0, description='Skyline Thresh:',
                                                               style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_skyline_file_input = widgets.Text(value='new_wave_lamp/skyline.dat', description='Skyline File:',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_skyline_rows_input = widgets.Text(value='None', description='Skyline Rows:', placeholder='Optional',
                                                        style={'description_width': 'initial'},layout= custom_input_layout)
        self.extract1d_skyline_linear_checkbox = widgets.Checkbox(value=False, description='Skyline Linear Fit')
        self.extract1d_skyline_inter_checkbox = widgets.Checkbox(value=True, description='Skyline Interactive')
        self.extract1d_skyline_plot_checkbox = widgets.Checkbox(value=True, description='Skyline plot')
        self.extract1d_skyline_thresh_input.add_class('cofi-input-widget')
        self.extract1d_skyline_file_input.add_class('cofi-input-widget')
        self.extract1d_skyline_rows_input.add_class('cofi-input-widget')
        self.extract1d_skyline_linear_checkbox.add_class('cofi-input-widget')
        self.extract1d_skyline_inter_checkbox.add_class('cofi-input-widget')
        self.extract1d_skyline_plot_checkbox.add_class('cofi-input-widget')

        # --- Output & Interactive Areas ---
        self.output_area = widgets.Output(layout={'border': '1px solid #ccc', 'padding': '10px', 'min_height': 'auto'})
        self.output_area.add_class('custom-output-area')
        
        self.processor_2d_control_area = widgets.VBox([], layout={'padding': '5px'})
        self.processor_2d_feedback_area = widgets.VBox([], layout=widgets.Layout(padding='5px', align_items='center'))
        self.processor_2d_output_area = widgets.Output(layout={'border': '1px solid #ace', 'padding': '10px', 'min_height':'auto'})
        self.processor_2d_output_area.add_class('interactive-processor-area')
        
        self.processor_1d_control_area = widgets.VBox([], layout=widgets.Layout(padding='5px', align_items='center'))
        self.processor_1d_feedback_area = widgets.VBox([], layout=widgets.Layout(padding='5px', align_items='center'))
        self.processor_1d_log_area = widgets.Output(layout={'border': '1px solid #aec', 'padding': '10px', 'min_height':'auto'})
        self.processor_1d_log_area.add_class('interactive-processor-area')
    
    def _setup_ui(self):
        # --- Calibration Sub-tabs with Advanced Accordions ---

        # 1. Bias Tab
        bias_advanced_box = widgets.VBox([
            self.bias_type_dropdown, self.bias_sigreject_input,
            self.bias_display, self.bias_trim_checkbox
        ])
        bias_accordion = widgets.Accordion(children=[bias_advanced_box])
        bias_accordion.set_title(0, 'Advanced Parameters')
        bias_accordion.selected_index = None # Collapsed by default
        bias_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Compute Master Bias</h3>"),
            self.bias_files_input,
            bias_accordion,
            self.compute_bias_button
        ])

        # 2. Dark Tab
        dark_advanced_box = widgets.VBox([
            self.dark_type_dropdown, self.dark_sigreject_input, self.dark_clip_input,
            self.apply_dark_bias_checkbox, self.dark_display, self.dark_trim_checkbox
        ])
        dark_accordion = widgets.Accordion(children=[dark_advanced_box])
        dark_accordion.set_title(0, 'Advanced Parameters')
        dark_accordion.selected_index = None
        dark_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Compute Master Dark</h3>"),
            self.dark_files_input,
            dark_accordion,
            self.compute_dark_button
        ])

        # 3. Flat Tab
        flat_advanced_box = widgets.VBox([
            self.flat_type_dropdown, self.flat_sigreject_input, self.flat_spec_checkbox,
            self.flat_width_input, self.flat_normalize_checkbox, self.flat_snmin_input,
            self.apply_bias_checkbox , self.apply_dark_checkbox, self.flat_display,
            self.flat_littrow_checkbox, self.flat_trim_checkbox
        ])
        flat_accordion = widgets.Accordion(children=[flat_advanced_box])
        flat_accordion.set_title(0, 'Advanced Parameters')
        flat_accordion.selected_index = None
        flat_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Compute Master Flat</h3>"),
            self.flat_files_input,
            flat_accordion,
            self.compute_flat_button
        ])

        # 4. Arcs Tab (No changes needed here)
        arcs_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Compute Master Arcs</h3>"),
            self.arc_files_input,
            self.compute_arcs_button
        ])
        
        calibration_sub_tabs = widgets.Tab(children=[bias_tab_content, dark_tab_content, flat_tab_content, arcs_tab_content])
        calibration_sub_tabs.set_title(0, 'Bias'); calibration_sub_tabs.set_title(1, 'Dark'); calibration_sub_tabs.set_title(2, 'Flat'); calibration_sub_tabs.set_title(3, 'Arcs')

        # --- Slits & Targets Sub-tabs with Advanced Accordions ---
        
        # 5. Find Slits Tab
        find_slits_advanced_box = widgets.VBox([
            self.findslits_smooth_input, self.findslits_degree_input,
            self.findslits_skip_input, self.findslits_cent_input
        ])
        find_slits_accordion = widgets.Accordion(children=[find_slits_advanced_box])
        find_slits_accordion.set_title(0, 'Advanced Parameters')
        find_slits_accordion.selected_index = None
        find_slits_box = widgets.VBox([
            self.slit_flat_file_input, self.kms_file_input,
            self.findslits_thresh_input, self.findslits_sn_checkbox,
            find_slits_accordion, self.find_slits_button
        ])

        filter_slits_box = widgets.VBox([
            self.filter_method_dropdown, self.filter_values_input,
            widgets.HBox([self.filter_slits_button, self.update_headers_button, self.reset_filter_button])
        ])
        
        slits_targets_sub_tabs = widgets.Tab(children=[
            widgets.VBox([widgets.HTML("<h3 class='sub-tab-title'>Find Slits/Targets</h3>"), find_slits_box]),
            widgets.VBox([widgets.HTML("<h3 class='sub-tab-title'>Filter Slits & Update Headers</h3>"), filter_slits_box])
        ])
        slits_targets_sub_tabs.set_title(0, 'Find Slits'); slits_targets_sub_tabs.set_title(1, 'Filter Targets')

        # --- Science & Extraction Sub-tabs with Advanced Accordions ---

        # 6. Reduce Tab
        reduce_advanced_box = widgets.VBox([
            #self.use_calibrations_checkbox
            self.reduce_appy_bias_checkbox,self.reduce_appy_dark_checkbox,self.reduce_appy_flat_checkbox, 
            self.reduce_seeing_input, self.reduce_solve_checkbox,
            self.reduce_channel_input, self.reduce_scat_input, self.reduce_badpix_input,
            self.reduce_trim_checkbox, self.reduce_sigfrac_input, self.reduce_ext_input,
            self.reduce_utr_checkbox
        ])
        reduce_accordion = widgets.Accordion(children=[reduce_advanced_box])
        reduce_accordion.set_title(0, 'Advanced Parameters')
        reduce_accordion.selected_index = None
        reduce_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Reduce Science Frame</h3>"),
            self.science_file_input, self.reduce_crbox_input,
            self.reduce_crsig_input, self.reduce_objlim_input,
            reduce_accordion,
            self.reduce_button
        ])

        # --- The rest of the UI setup remains the same ---

        # Group the main, frequently used wavelength calibration widgets
        main_wave_cal_box = widgets.VBox([
            self.wavecal_clobber_checkbox,
            self.wavecal_lamp_spec_input,
            # self.wavecal_lamp_lines_input,
            self.wavecal_id_file_input,
            self.wavecal_fit_degree_input,
            self.wavecal_refit_degree_input,
            self.wavecal_shift_multiplier_input,
            self.wavecal_arc_line_input,
            self.wavecal_id_lags_input,
            self.wavecal_id_thresh_input,
            self.wavecal_id_rad_input
        ])
        
        # Group the advanced/optional identify() parameters in a separate box
        advanced_id_params_box = widgets.VBox([
            self.wavecal_id_maxshift_input,
            self.wavecal_id_disp_input,
            self.wavecal_id_sample_input,
            self.wavecal_id_re_sample_input,
            self.wavecal_id_weak_weight_input,
            self.wavecal_id_arc_line_position_input,
            # self.wavecal_id_lags_input,
            # Group related checkboxes for a cleaner layout
            widgets.HBox([
                self.wavecal_id_fit_checkbox, 
                self.wavecal_id_sky_checkbox, 
                self.wavecal_id_inter_checkbox
            ]),
            widgets.HBox([
                self.wavecal_id_verbose_checkbox, 
                self.wavecal_id_pixplot_checkbox, 
                self.wavecal_id_domain_checkbox
            ]),
            widgets.HBox([
                self.wavecal_id_plot_checkbox,
                self.wavecal_id_plotinter_checkbox,
            ]),
            # Group related inputs
            widgets.HBox([self.wavecal_id_xmin_input, self.wavecal_id_xmax_input]),
            self.wavecal_id_rows_input,
            self.wavecal_id_nskip_input,
            self.wavecal_id_orders_input,
            self.wavecal_id_wav_input,
            self.wavecal_id_wref_input
        ])
        
        # Use an accordion to make the advanced options collapsible
        advanced_options_accordion = widgets.Accordion(children=[advanced_id_params_box])
        advanced_options_accordion.set_title(0, 'Advanced Identify Parameters')
        advanced_options_accordion.selected_index = None # Start with it collapsed
        
        # Combine all components into the final tab layout
        wave_cal_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Wavelength Calibration</h3>"),
            main_wave_cal_box,
            advanced_options_accordion, # Add the collapsible section
            widgets.HBox([self.run_shift_check_button,self.run_wave_cal_button])
        ])
        
        # --- Create VBoxes for each parameter group for the Accordion ---
        trace_params_vbox = widgets.VBox([
            self.extract2d_trace_degree_input, self.extract2d_trace_sigdegree_input,
            self.extract2d_trace_type_input, self.extract2d_trace_rad_input,
            self.extract2d_trace_lags_input, self.extract2d_trace_pix0_input,
            self.extract2d_trace_sc0_input, self.extract2d_trace_rows_input,
            self.extract2d_trace_channel_input, self.extract2d_trace_inst_input,
            self.extract2d_trace_file_input,self.extract2d_spectrum_input,
            self.extract2d_trace_model_input,
            self.extract2d_trace_hdu_input, self.extract2d_trace_transpose_checkbox
        ])
        findpeak_params_vbox = widgets.VBox([
            self.extract2d_findpeak_thresh_input, self.extract2d_findpeak_backperc_input,
            self.extract2d_findpeak_width_input, self.extract2d_findpeak_smooth_input,
            self.extract2d_findpeak_sc0_input, self.extract2d_findpeak_method_input,
            self.extract2d_findpeak_diff_input, self.extract2d_findpeak_bundle_input,
            self.extract2d_findpeak_sort_checkbox, self.extract2d_findpeak_verbose_checkbox,
            self.extract2d_findpeak_plot_checkbox,
        ])
        skyline_params_vbox = widgets.VBox([
            self.extract2d_skyline_thresh_input,
            self.extract2d_skyline_file_input, self.extract2d_skyline_rows_input,
            self.extract2d_skyline_linear_checkbox, self.extract2d_skyline_inter_checkbox,
            self.extract2d_skyline_obj_rad_input,self.extract2d_correcting_value_input,
        ])
        extract_params_vbox = widgets.VBox([
            self.extract2d_rows_input, self.extract2d_buffer_input,self._2d_flat_field_checkbox
        ])
        
        # --- Create the Accordion to hold the parameter groups ---
        params_accordion = widgets.Accordion(children=[
            trace_params_vbox, findpeak_params_vbox, skyline_params_vbox, extract_params_vbox
        ])
        params_accordion.set_title(0, 'Trace Parameters')
        params_accordion.set_title(1, 'FindPeak Parameters')
        params_accordion.set_title(2, 'Skyline Parameters')
        params_accordion.set_title(3, 'Extraction Parameters')
        params_accordion.selected_index = None # Start collapsed
        
        # --- Define the main box for default parameters ---
        extract2d_params_box = widgets.VBox([
            widgets.HTML("<h4>Default Parameters for 2D Extraction:</h4>"),
            params_accordion
        ])
        
        # --- Define the final layout for the 2D extraction tab ---
        extract2d_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>2D Spectral Extraction</h3>"),
            extract2d_params_box,
            self.start_extract2d_button,
            widgets.HTML("<h4>Interactive Controls (from processor):</h4>"), self.processor_2d_control_area,
            widgets.HTML("<h4>Feedback Prompt (from processor):</h4>"), self.processor_2d_feedback_area,
            widgets.HTML("<h4>Log / Output (from processor):</h4>"), self.processor_2d_output_area
        ])

        # --- Create VBoxes for each parameter group for the 1D Accordion ---
        extract1d_main_vbox = widgets.VBox([
            # self.extract1d_plot_spectra_checkbox, 
            # self.extract1d_back_input,
            self.extract1d_fit_checkbox,
            self.extract1d_old_checkbox, self.extract1d_medfilt_input,
            self.extract1d_nout_input, self.extract1d_threads_input,
            # self.extract1d_sky_width_input,
        ])
        trace_class_vbox = widgets.VBox([
            self.extract1d_trace_degree_input, self.extract1d_trace_sigdegree_input,
            self.extract1d_trace_class_lags_input, self.extract1d_trace_class_type_input,
            self.extract1d_trace_class_rad_input, self.extract1d_trace_class_pix0_input,
            self.extract1d_trace_class_sc0_input, self.extract1d_trace_class_rows_input,
            self.extract1d_trace_class_channel_input, self.extract1d_trace_class_inst_input,
            self.extract1d_trace_class_file_input, self.extract1d_trace_class_hdu_input,
            self.extract1d_trace_class_model_input,self.extract1d_trace_class_spectrum_input,
            self.extract1d_trace_class_transpose_checkbox
        ])
        findpeak1d_vbox = widgets.VBox([
            self.extract1d_findpeak_thresh_input, self.extract1d_findpeak_backperc_input,
            self.extract1d_findpeak_width_input, self.extract1d_findpeak_method_input,
            self.extract1d_findpeak_smooth_input, self.extract1d_findpeak_sc0_input,
            self.extract1d_findpeak_diff_input, self.extract1d_findpeak_bundle_input,
            self.extract1d_findpeak_sort_checkbox, self.extract1d_findpeak_verbose_checkbox,
            self.extract1d_findpeak_plot_checkbox
        ])
        trace_method_vbox = widgets.VBox([
            self.extract1d_trace_skip_input, self.extract1d_trace_method_rad_input,
            self.extract1d_trace_method_thresh_input, self.extract1d_trace_method_sc0_input,
            self.extract1d_trace_method_srows_input, self.extract1d_trace_method_index_input, 
            self.extract1d_trace_method_gaussian_checkbox, self.extract1d_trace_method_verbose_checkbox
        ])
        skyline1d_vbox = widgets.VBox([
            self.extract1d_skyline_thresh_input, self.extract1d_skyline_file_input,
            self.extract1d_skyline_rows_input, self.extract1d_skyline_linear_checkbox,
            self.extract1d_skyline_inter_checkbox,self.extract1d_skyline_plot_checkbox
        ])
        
        # --- Create the Accordion to hold the parameter groups ---
        params1d_accordion = widgets.Accordion(children=[
            extract1d_main_vbox, trace_class_vbox, findpeak1d_vbox, trace_method_vbox, skyline1d_vbox
        ])
        params1d_accordion.set_title(0, 'Extraction & Plotting')
        params1d_accordion.set_title(1, 'Trace Class Parameters')
        params1d_accordion.set_title(2, 'FindPeak Parameters')
        params1d_accordion.set_title(3, 'Trace Method Parameters')
        params1d_accordion.set_title(4, 'Skyline Parameters')
        params1d_accordion.selected_index = None # Start collapsed
        
        # --- Define the main box for default parameters ---
        extract1d_params_box = widgets.VBox([
            widgets.HTML("<h4>Default Parameters for 1D Extraction:</h4>"),
            params1d_accordion
        ])
        
        # --- Define the final layout for the 1D extraction tab ---
        extract1d_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>1D Spectral Extraction</h3>"),
            extract1d_params_box,
            self.start_extract1d_button,
            widgets.HTML("<h4>Interactive Controls (from processor):</h4>"), self.processor_1d_control_area,
            widgets.HTML("<h4>Feedback Prompt (from processor):</h4>"), self.processor_1d_feedback_area,
            widgets.HTML("<h4>Log / Output (from processor):</h4>"), self.processor_1d_log_area
        ])
        
        science_sub_tabs = widgets.Tab(children=[ wave_cal_tab_content, reduce_tab_content, extract2d_tab_content, extract1d_tab_content])
        science_sub_tabs.set_title(0, 'Wave Cal'); science_sub_tabs.set_title(1, 'Reduce'); science_sub_tabs.set_title(2, '2D Extract'); science_sub_tabs.set_title(3, '1D Extract')

        # --- Main Tabs ---
        tab6_content = self.guide_widget.display()
        tab6_content.add_class('cofi-guide-container')
        # data_input_tab_content = widgets.VBox([self.folder_path_input, self.log_file_input, self.read_folder_button])

        data_input_tab_content = widgets.VBox([
            widgets.HTML("<h3 class='sub-tab-title'>Load Observation Data</h3>"),
            self.folder_path_input, 
            self.log_file_input,
            self.read_folder_button,
            widgets.HTML("<hr>"), # Visual separator
            widgets.HTML("<h3 class='sub-tab-title'>Load Settings from Log</h3>"),
            self.log_uploader,
            self.load_log_button
        ])
        
        main_tabs = widgets.Tab(children=[tab6_content, data_input_tab_content, calibration_sub_tabs, slits_targets_sub_tabs, science_sub_tabs])
        main_tabs.set_title(0,  "📖 User Guide"); main_tabs.set_title(1, "📁 Data Input"); main_tabs.set_title(2, "⚙️ Calibration"); main_tabs.set_title(3, "🔎 Slits & Targets"); main_tabs.set_title(4, "🔬 Science & Extract")

        self.full_ui = widgets.VBox([widgets.HTML("<h1 class='cofi-main-title'>CofI Reduction Interface</h1>"), main_tabs, self.output_area])

    def _attach_handlers(self):
        self.read_folder_button.on_click(self._read_folder_handler)
        self.compute_bias_button.on_click(self._compute_bias_handler)
        self.compute_dark_button.on_click(self._compute_dark_handler)
        self.compute_flat_button.on_click(self._compute_flat_handler)
        self.compute_arcs_button.on_click(self._compute_arcs_handler)
        self.find_slits_button.on_click(self._find_slits_handler)
        self.update_headers_button.on_click(self._update_headers_handler)
        self.filter_slits_button.on_click(self._filter_slits_handler)
        self.reset_filter_button.on_click(self._reset_filter_handler) # Attach reset handler
        self.reduce_button.on_click(self._reduce_science_handler)
        self.run_wave_cal_button.on_click(self._run_wave_cal_handler)
        self.run_shift_check_button.on_click(self._run_shift_check_handler)
        self.start_extract2d_button.on_click(self._start_extract2d_handler) # New handler
        self.start_extract1d_button.on_click(self._start_extract1d_handler) # New handler
        # In CofiReductionWidget1._attach_handlers
        self.load_log_button.on_click(self._load_log_handler)

    def show(self):
        display(self.full_ui)

    def _parse_input(self, input_str):
        if not input_str.strip(): return []
        items = [x.strip() for x in input_str.split(',') if x.strip()]
        try:
            return [int(item) for item in items]
        except ValueError: # If not all are ints, treat all as strings (filenames)
            return items 
            
    # --- Handler Methods ---
    def _read_folder_handler(self, b):
        with self.output_area:
            clear_output(wait=True)
            indir = self.folder_path_input.value
            if not os.path.isdir(indir):
                print(f"❌ Error: Folder not found at '{indir}'")
                return
            # Set the star/target name for the logger from the folder name
            star_name = os.path.basename(os.path.normpath(self.log_file_input.value)) or "reduction_session"
            self.logger.set_log_file(star_name)
            
            # Log this action
            params = {'folder_path': indir}
            self.logger.log_action("Data Input", "Read Folder", params)
            try:
                self.red = imred.Reducer('KOSMOS', dir=indir) # KOSMOS is instrument default
                print(f"✅ Reducer initialized for folder: {indir}")
                display(self.red.log().show_in_notebook(display_length=len(self.red.log()))) # Show full log
            except Exception as e:
                print(f"❌ Error initializing Reducer: {e}")

    def _compute_bias_handler(self, b):
        # 1. Gather all parameters for logging
        params = {
            'Bias Frames': self.bias_files_input.value,
            'Combine Type': self.bias_type_dropdown.value,
            'Sigma Reject': self.bias_sigreject_input.value,
            'display individual': self.bias_display.value,
            'Trim Bias': self.bias_trim_checkbox.value
        }
        # 2. Log the action before executing it
        self.logger.log_action("Calibration - Bias", "Compute Bias", params)
        
        with self.output_area:
            clear_output(wait=True)
            if not self.red: print("❌ Reducer not set. Read folder first."); return
            files = self._parse_input(self.bias_files_input.value)
            if not files: print("❌ Bias frames input is empty."); return          
            if self.bias_display.value:
                bias_display = self.tv
            else:
                bias_display = None
            try:
                self.bias_frame = self.red.mkbias(files, display=bias_display, # display handled by self.tv
                                                    type=self.bias_type_dropdown.value,
                                                    sigreject=self.bias_sigreject_input.value,
                                                   trim = self.bias_trim_checkbox.value)
                print(f"✅ Master Bias created from frames: {files}")
                if self.tv and self.bias_frame is not None : self.tv.tv(self.bias_frame)
            except Exception as e:
                print(f"❌ Error computing bias: {e}")

    def _compute_dark_handler(self, b):
        # 1. Gather all parameters for logging
        params = {
            'Dark Frames': self.dark_files_input.value,
            'Combine Type': self.dark_type_dropdown.value,
            'Sigma Reject': self.dark_sigreject_input.value,
            'Clip (x Uncertainty)': self.dark_clip_input.value,
            'Display Individual': self.dark_display.value,
            'Apply dark Bias': self.apply_dark_bias_checkbox.value,
            'Trim Dark': self.dark_trim_checkbox.value
        }
        # 2. Log the action before executing it
        self.logger.log_action("Calibration - Dark", "Compute Dark", params)
        with self.output_area:
            clear_output(wait=True)
            if not self.red: print("❌ Reducer not set. Read folder first."); return
            files = self._parse_input(self.dark_files_input.value)
            if not files: print("❌ Dark frames input is empty."); return
                
            if self.apply_dark_bias_checkbox.value:
                dark_biases = self.bias_frame
            else:
                dark_biases = None

            if self.dark_display.value:
                dark_display = self.tv
            else:
                dark_display = None
            if self.dark_clip_input.value == 0:
                dark_clip = None
            else:
                dark_clip = self.dark_clip_input.value
            try:

                self.dark_frame = self.red.mkdark(files, bias=dark_biases, display=dark_display,
                                                    type=self.dark_type_dropdown.value,
                                                    sigreject=self.dark_sigreject_input.value,
                                                    clip=dark_clip,
                                                   trim= self.dark_trim_checkbox.value)
                print(f"✅ Master Dark created from frames: {files}")
                if self.tv and self.dark_frame is not None: self.tv.tv(self.dark_frame)
            except Exception as e:
                print(f"❌ Error computing dark: {e}")

    def _compute_flat_handler(self, b):
        # 1. Gather all parameters for logging
        params = {
            'Flat Frames': self.flat_files_input.value,
            'Combine Type': self.flat_type_dropdown.value,
            'Sigma Reject': self.flat_sigreject_input.value,
            'Spectral Flat': self.flat_spec_checkbox.value,
            'Window Width': self.flat_width_input.value,
            'Normalize Flat': self.flat_normalize_checkbox.value,
            'S/N Min (for Norm)': self.flat_snmin_input.value,
            'Apply Bias': self.apply_bias_checkbox.value,
            'Apply Dark': self.apply_dark_checkbox.value,
            'Display Individual flats': self.flat_display.value,
            'Flat littrow ': self.flat_littrow_checkbox.value,
            'Trim Flats': self.flat_trim_checkbox.value
            
        }
        # 2. Log the action before executing it
        self.logger.log_action("Calibration - Flat", "Compute Flat", params)
        with self.output_area:
            clear_output(wait=True)
            if not self.red: print("❌ Reducer not set. Read folder first."); return
            files = self._parse_input(self.flat_files_input.value)
            if not files: print("❌ Flat frames input is empty."); return
            
            if self.apply_bias_checkbox.value:
                flat_biases = self.bias_frame
            else:
                flat_biases = None
                
            if self.apply_dark_checkbox.value:
                flat_darks = self.dark_frame
            else:
                flat_darks = None
                
            if self.flat_display.value:
                flat_display = self.tv
            else:
                flat_display = None
            try:
                self.flat_frame = self.red.mkflat(files, bias=flat_biases, dark=flat_darks, display=flat_display,
                                                    type=self.flat_type_dropdown.value,
                                                    sigreject=self.flat_sigreject_input.value,
                                                    spec=self.flat_spec_checkbox.value,
                                                    width=self.flat_width_input.value,
                                                    normalize=self.flat_normalize_checkbox.value,
                                                    snmin=self.flat_snmin_input.value,
                                                    trim= self.flat_trim_checkbox.value,
                                                   littrow = self.flat_littrow_checkbox.value)
                print(f"✅ Master Flat created from frames: {files}")
                if self.tv and self.flat_frame is not None: self.tv.tv(self.flat_frame)
            except Exception as e:
                print(f"❌ Error computing flat: {e}")

    def _compute_arcs_handler(self, b):
        # 1. Gather all parameters for logging
        params = {
            'Arc Frames': self.arc_files_input.value
            
        }
        # 2. Log the action before executing it
        self.logger.log_action("Calibration - Arcs", "Compute Arc", params)
        
        with self.output_area:
            clear_output(wait=True)
            if not self.red: print("❌ Reducer not set. Read folder first."); return
            files = self._parse_input(self.arc_files_input.value)
            if not files: print("❌ Arc frames input is empty."); return
            try:
                self.arcs_frame = self.red.sum(files) # sum doesn't take display
                print(f"✅ Master Arc(s) created from frames: {files}")
                if self.tv and self.arcs_frame is not None: self.tv.tv(self.arcs_frame)
            except Exception as e:
                print(f"❌ Error computing arcs: {e}")

    def _find_slits_handler(self, b):
        # 1. Gather all parameters for logging
        params = {
            'Flat Frame for Slits': self.slit_flat_file_input.value,
            'KMS File': self.kms_file_input.value,
            'Edge Threshold (FindSlits)': self.findslits_thresh_input.value,
            'Use S/N for Edges (FindSlits)': self.findslits_sn_checkbox.value,
            'Smooth Radius (FindSlits)': self.findslits_smooth_input.value,
            'Fit Degree (FindSlits)': self.findslits_degree_input.value,
            'Pixels to skip (FindSlits)': self.findslits_skip_input.value,
            'spectra center location (if known)': self.findslits_cent_input.value
        }
        # 2. Log the action before executing it
        self.logger.log_action("Slits & Targets - Find Slits", "Find Slits", params)
        self.tv.tvclear()
        self.tv.clear()
        with self.output_area:
            clear_output(wait=True)
            if not self.red: print("❌ Reducer not set."); return
            flat_file_id = self._parse_input(self.slit_flat_file_input.value)
            if not flat_file_id or not isinstance(flat_file_id[0], (int, str)): # Ensure it's a single identifier
                print("❌ Slit finding flat input is empty or invalid (must be a single frame ID/name)."); return
            
            kms_file = self.kms_file_input.value
            if not os.path.isfile(kms_file): print(f"❌ KMS file not found: {kms_file}"); return
            
            try:
                # Reduce the single flat frame specified for slit finding
                flat_image_data = self.red.reduce(flat_file_id[0], display=None) # Reduce returns image data
                if flat_image_data is None:
                    print(f"❌ Failed to reduce flat frame {flat_file_id[0]}.")
                    return
                if self.findslits_cent_input.value == 'None':
                    cent_value = None
                else:
                    cent_value = int(self.findslits_cent_input.value)
                    
                self.trace = spectra.Trace(transpose=True) # KOSMOS specific
                bottom, top = self.trace.findslits(flat_image_data, display=self.tv, # Pass image data
                                                   smooth=self.findslits_smooth_input.value,
                                                   thresh=self.findslits_thresh_input.value,
                                                   degree=self.findslits_degree_input.value,
                                                   skip = self.findslits_skip_input.value,
                                                   sn=self.findslits_sn_checkbox.value,
                                                   cent = cent_value)
                self.targets = slitmask.read_kms(kms_file, sort='YMM') # YMM sort is KOSMOS typical
                
                # Store the original full list for potential reset
                self.full_trace = copy.deepcopy(self.trace)
                self.full_targets = self.targets.copy() # Use .copy() for astropy Table

                print(f"✅ Found {len(bottom)} slits.")
                if len(self.targets) != len(bottom) or len(self.targets) != len(top):
                    print(f"⚠️ Warning: Found bottom = {len(bottom)} and found top = {len(top)} the slits are not properly found")
                    if len(bottom) > len(top):
                        slit_size = len(top)
                    else:
                        slit_size = len(bottom)
                    print(f"⚠️ Warning: Found {slit_size} slits but KMS file has {len(self.targets)} targets.")
                display(self.targets.to_pandas())
            except Exception as e:
                print(f"❌ Error finding slits: {e}")
                import traceback
                traceback.print_exc()


    def _update_headers_handler(self, b):
        self.tv.tvclear()
        self.tv.clear()
        with self.output_area:
            clear_output(wait=True)
            if not self.trace or self.arcs_frame is None or self.targets is None:
                print("❌ Trace, Arcs, or Targets not available. Run previous steps."); return
            try:
                self.arcec = self.trace.extract2d(self.arcs_frame, display=self.tv)
                for arc, target in zip(self.arcec, self.targets):
                    arc.header['XMM'] = target['XMM']
                    arc.header['YMM'] = target['YMM']
                print("✅ Arc headers updated with XMM and YMM for currently selected targets.")
            except Exception as e:
                print(f"❌ Error updating arc headers: {e}")

    def _filter_slits_handler(self, b):
        # 1. Gather all parameters for logging
        params = {
            'Filter By': self.filter_method_dropdown.value,
            'Values': self.filter_values_input.value
        }
        # 2. Log the action before executing it
        self.logger.log_action("Slits & Targets - Filter Targets", "Filter Slits", params)
        
        with self.output_area:
            clear_output(wait=True)
            if self.full_targets is None or self.full_trace is None:
                print("❌ Run 'Find Slits' first to generate the initial target list and trace.")
                return

            value_str = self.filter_values_input.value
            if not value_str.strip():
                print("❌ Filter values are empty.")
                # Optionally, reset to full list if filter is empty
                # self._reset_filter_handler(None) 
                return

            data = self.full_targets.to_pandas() # Filter from the original full list
            method = self.filter_method_dropdown.value
            selected_indices = [] # Store indices relative to self.full_targets

            try:
                if method == 'Index':
                    raw_indices = [idx.strip() for idx in value_str.split(',') if idx.strip()]
                    for idx_str in raw_indices:
                        if idx_str.isdigit():
                            idx = int(idx_str)
                            if 0 <= idx < len(self.full_targets):
                                selected_indices.append(idx)
                            else:
                                print(f"⚠️ Index {idx} out of range (0-{len(self.full_targets)-1}).")
                        else:
                            print(f"⚠️ Invalid index '{idx_str}'.")
                
                elif method == 'ID':
                    ids_to_find = [val.strip().strip("'\"") for val in value_str.split(',')]
                    # Ensure 'ID' column exists and is string type for comparison
                    if 'ID' in data.columns:
                        data['ID_str'] = data['ID'].astype(str).str.strip()
                        mask = data['ID_str'].isin(ids_to_find)
                        selected_indices = data.index[mask].tolist()
                    else:
                        print("⚠️ 'ID' column not found in targets table.")
                
                elif method == 'Name':
                    names_to_find = [val.strip().strip("'\"") for val in value_str.split(',')]
                    if 'NAME' in data.columns:
                        data['NAME_str'] = data['NAME'].astype(str).str.strip()
                        mask = data['NAME_str'].isin(names_to_find)
                        selected_indices = data.index[mask].tolist()
                    else:
                        print("⚠️ 'NAME' column not found in targets table.")

                if not selected_indices:
                    print("⚠️ No targets found matching the filter criteria. Current selection remains unchanged.")
                    # Display current targets again so user isn't confused
                    if self.targets is not None: display(self.targets.to_pandas())
                    else: print(" (No targets currently selected)")
                    return

                # Filter the trace object based on selected_indices from full_trace
                gdtrace = copy.deepcopy(self.full_trace) # Start from original trace
                gdtrace.model = [self.full_trace.model[i] for i in selected_indices if i < len(self.full_trace.model)]
                gdtrace.rows = [self.full_trace.rows[i] for i in selected_indices if i < len(self.full_trace.rows)]
                
                # Update the main trace and targets attributes
                self.trace = gdtrace
                self.targets = self.full_targets[selected_indices] # Filter original table by indices
                
                print(f"✅ Filter applied. Selected {len(self.targets)} targets:")
                display(self.targets.to_pandas())

            except Exception as e:
                print(f"❌ An error occurred during filtering: {e}")
                import traceback
                traceback.print_exc()
    
    def _reset_filter_handler(self, b):
        with self.output_area:
            clear_output(wait=True)
            if self.full_targets is None or self.full_trace is None:
                print("❌ No original target list to reset to. Run 'Find Slits' first.")
                return
            
            self.trace = copy.deepcopy(self.full_trace)
            self.targets = self.full_targets.copy() # Use .copy() for astropy Table
            self.filter_values_input.value = '' # Clear filter input
            print("✅ Filter has been reset. Showing all original targets.")
            display(self.targets.to_pandas())

    def _reduce_science_handler(self, b):
        self.tv.tvclear()
        self.tv.clear()
        with self.output_area:
            clear_output(wait=True)
            if not self.red: print("❌ Reducer not set."); return
            science_file_id = self._parse_input(self.science_file_input.value)
            if not science_file_id or not isinstance(science_file_id[0], (int, str)):
                    print("❌ Science frame input is empty or invalid (must be a single frame ID/name)."); return

            crbox_value = get_srt_or_list(self.reduce_crbox_input.value)
            try:
                kwargs = {
                    'num': science_file_id[0],
                    'bias': self.bias_frame if self.reduce_appy_bias_checkbox.value else None,
                    'dark': self.dark_frame if self.reduce_appy_dark_checkbox.value else None,
                    'flat': self.flat_frame if self.reduce_appy_flat_checkbox.value else None,
                    'display': self.tv if self.display_enabled and self.tv is not None else None,
                    'crbox': crbox_value if self.reduce_crbox_input.value != 'none' else None,
                    'crsig': self.reduce_crsig_input.value,
                    'objlim': self.reduce_objlim_input.value,
                    #'display': None, # self.tv, # Handled by tv call below
                    'channel':None if self.reduce_channel_input.value == "None" else
                    int(self.reduce_channel_input.value),
                    'scat': None if self.reduce_scat_input.value =='None' else 
                    int(self.reduce_scat_input.value),
                    'badpix': None if self.reduce_badpix_input.value =='None'
                    else int(self.reduce_badpix_input.value),
                    'trim': self.reduce_trim_checkbox.value,
                    'utr': self.reduce_utr_checkbox.value,
                    #'return_list': self.reduce_return_list_checkbox.value,
                    'ext': self.reduce_ext_input.value,
                    'solve': self.reduce_solve_checkbox.value,
                    'seeing': self.reduce_seeing_input.value,
                    'sigfrac': self.reduce_sigfrac_input.value,
                }


                # Create a separate dictionary for logging
                log_kwargs = kwargs.copy()
    
                # Remove non-serializable objects and the old keys
                del log_kwargs['display']
                del log_kwargs['bias']
                del log_kwargs['dark']
                del log_kwargs['flat']
    
                # Add the new keys with descriptive names and their boolean values
                log_kwargs['Apply bias'] = self.reduce_appy_bias_checkbox.value
                log_kwargs['Apply dark'] = self.reduce_appy_dark_checkbox.value
                log_kwargs['Apply flat'] = self.reduce_appy_flat_checkbox.value
                
                # # Add the science file number for completeness
                # log_kwargs['science_file_num'] = science_file_id[0]
    
                # # Log the user's settings before executing
                # # self.logger.log_action("Science & Extract - Reduce", "Reduce Science Frame", log_kwargs)
    
                # # Execute the reduction with the original kwargs containing the frame objects
                # self.reduced_frame = self.red.reduce(science_file_id[0], **kwargs)

                
                # 2. Log the action before executing it
                # Create a new dictionary for logging that excludes the 'display' key
                # log_kwargs = {key: (True if key == 'display' else value) for key, value in kwargs.items()}
                #{key: value for key, value in kwargs.items() if key != 'display'}
                self.logger.log_action("Science & Extraction - Reduce", "Reduce Science Frame", log_kwargs)
        
                self.reduced_frame = self.red.reduce( **kwargs)
                print(f"✅ Science frame {science_file_id[0]} reduced.")
                #if self.tv and self.reduced_frame is not None : self.tv.tv(self.reduced_frame)
            except Exception as e:
                print(f"❌ Error reducing science frame: {e}")
                import traceback
                traceback.print_exc()


    def _run_wave_cal_handler(self, b):
        with self.output_area:
            clear_output(wait=True)
            if self.arcec is None or self.targets is None:
                print("❌ Run 'Update Arc Headers' first for current targets.")
                return
            print("🚀 Starting Wavelength Calibration...")

            
            variable = get_srt_or_list(self.wavecal_id_wav_input.value)
            if isinstance(variable,str):
                wav_value = variable
            else:
                wav_value = np.array(variable)
                
            wref_value = get_srt_or_list(self.wavecal_id_wref_input.value)
            orders_value = get_srt_or_list(self.wavecal_id_orders_input.value)
            disp_value = get_srt_or_list(self.wavecal_id_disp_input.value)
            rows_value = get_srt_or_list(self.wavecal_id_rows_input.value)
            try:
                params = {
                    'clobber': self.wavecal_clobber_checkbox.value,
                    'lamp_spec_file': self.wavecal_lamp_spec_input.value,
                    'fit_degree': self.wavecal_fit_degree_input.value,
                    'shift_multiplier': self.wavecal_shift_multiplier_input.value,
                    # 'lamp_file_for_identify': self.wavecal_lamp_lines_input.value,
                    'file': self.wavecal_id_file_input.value,
                    'wave_fit_degree_after_identify': self.wavecal_refit_degree_input.value,
                    
                    # Parameters from identify()
                    'identify_thresh': self.wavecal_id_thresh_input.value, # Mapped from 'thresh'
                    'sky': self.wavecal_id_sky_checkbox.value,
                    # 'wav': wav_value if self.wavecal_id_wav_input.value != 'None' else None,
                    'wref': wref_value if self.wavecal_id_wref_input.value != 'None' else None,
                    'inter': self.wavecal_id_inter_checkbox.value,
                    'orders': orders_value if self.wavecal_id_orders_input.value != 'None' else None,
                    'verbose': self.wavecal_id_verbose_checkbox.value,
                    'rad': self.wavecal_id_rad_input.value,
                    'fit': self.wavecal_id_fit_checkbox.value,
                    'maxshift': self.wavecal_id_maxshift_input.value,
                    'sampling_value': 1 if self.wavecal_id_sample_input.value == 0 
                    else self.wavecal_id_sample_input.value,
                    'correcting_value': self.wavecal_id_re_sample_input.value,
                    'weight_thresh': self.wavecal_id_weak_weight_input.value,
                    'arc_line_position': self.wavecal_id_arc_line_position_input.value,
                    'disp': disp_value if self.wavecal_id_disp_input.value != 'None' else None,
                    'plot': self.wavecal_id_plot_checkbox.value,
                    'pixplot': self.wavecal_id_pixplot_checkbox.value,
                    'domain': self.wavecal_id_domain_checkbox.value,
                    # 'plot_first_identify': True, # Mapped from 'plot' for the first run
                    'plotinter': self.wavecal_id_plotinter_checkbox.value, # Mapped from 'plotinter'
                    'xmin': None if self.wavecal_id_xmin_input.value == 'None' 
                    else float(self.wavecal_id_xmin_input.value),
                    'xmax': None if self.wavecal_id_xmax_input.value == 'None'
                    else float(self.wavecal_id_xmax_input.value),
                    'lags_offset': self.wavecal_id_lags_input.value,
                    'nskip': None if self.wavecal_id_nskip_input.value == 'None'
                    else int(self.wavecal_id_nskip_input.value),
                    'rows': rows_value if self.wavecal_id_rows_input.value != 'None' else None
                }
                self.logger.log_action("Science & Extraction - Wave Cal", "Reduce Run Wavelength Calibration", params)
                self.processor.calibrate_wavelength(self.arcec, self.targets, **params)
                print("✅ Wavelength Calibration process complete.")
            except Exception as e:
                print(f"❌ Error during wavelength calibration: {e}")
                import traceback
                traceback.print_exc()


    def _run_shift_check_handler(self, b):
        with self.output_area: # Shift check primarily prints to console/shows plot
            clear_output(wait=True) # Clear previous messages in main output
            if self.arcec is None: print("❌ ArcEC (extracted 2D arcs) not available. Run 'Update Arc Headers' first."); return
            print("🚀 Checking wavelength shift (plot will appear in a new window or inline depending on Matplotlib backend)...")
            try:
                params = {
                    'lamp_spec_file': self.wavecal_lamp_spec_input.value,
                    'shift_multiplier': self.wavecal_shift_multiplier_input.value,
                    'arc_line': self.wavecal_arc_line_input.value,
                }
                # This method directly calls plt.show()
                self.logger.log_action("Science & Extraction - Wave Cal", "Check Shift", params)
                self.processor.checking_shift_value(self.arcec, **params) 
            except Exception as e:
                print(f"❌ Error during shift check: {e}")
                import traceback
                traceback.print_exc()

    # --- Callbacks and Handlers for Interactive Extraction ---
    def _update_spec2d_out_callback(self, result_list):
        self.spec2d_out = result_list
        with self.processor_2d_output_area: # self.output_area: # Use main output area for final confirmation
            # Don't clear here, processor_2d_output_area has detailed logs
            if result_list is not None:
                print(f"✅✅✅ Final 2D Extraction Callback: Results received for {len(result_list)} spectra. Stored in widget.")
            else:
                print("⚠️ 2D Extraction Callback: Received no results (None).")

    def _start_extract2d_handler(self, b):
        self.tv.tvclear()
        self.tv.clear()
        # This handler initiates the interactive 2D extraction process.
        # It passes necessary output areas to the processor method.
        with self.processor_2d_output_area: # self.output_area: # Main output area for initial status
            clear_output(wait=True)
            if self.reduced_frame is None or self.trace is None or self.targets is None:
                print("❌ Reduced science frame, trace, or targets not available. Ensure previous steps are complete."); return
            if not self.red:
                print("❌ Reducer object not initialized. Please read folder first."); return
            print("🚀 Initializing interactive 2D spectrum extraction UI in the '2D Extract' sub-tab...")
        
        # Clear processor-specific areas before new UI is injected
        self.processor_2d_control_area.children = []
        self.processor_2d_output_area.clear_output(wait=True)
    
        # Collect parameters from the main widget to pass as defaults/config to the processor
        lag1,lag2 = self.extract2d_trace_lags_input.value.split(',')
        lag_range = range(int(lag1),int(lag2))
        
        variable_2d = get_srt_or_list(self.extract2d_spectrum_input.value)
        if isinstance(variable_2d,str):
            spectrum_2d = variable_2d
        else:
            spectrum_2d = np.array(variable_2d)

        trace_model_value_2d = get_srt_or_list(self.extract2d_trace_model_input.value)
        trace_rows_value = get_srt_or_list(self.extract2d_trace_rows_input.value)
        skyline_rows_value = get_srt_or_list(self.extract2d_skyline_rows_input.value)
        extract2d_rows_value = get_srt_or_list(self.extract2d_rows_input.value)
        
        extract_2d_params = {
            # --- Trace() parameters ---
            'trace_file': None if self.extract2d_trace_file_input.value == 'None' 
            else self.extract2d_trace_file_input.value,
            'trace_spectrum': spectrum_2d if self.extract2d_spectrum_input.value != 'None'
            else None,
            'trace_inst': None if self.extract2d_trace_inst_input.value == 'None'
            else self.extract2d_trace_inst_input.value,
            'trace_type': self.extract2d_trace_type_input.value,
            'trace_degree': self.extract2d_trace_degree_input.value,
            'trace_sigdegree': self.extract2d_trace_sigdegree_input.value,
            'trace_pix0': self.extract2d_trace_pix0_input.value,
            'trace_rad': self.extract2d_trace_rad_input.value,
            'trace_model': trace_model_value_2d if self.extract2d_trace_model_input.value !='None'
            else None,
            'trace_sc0': None if self.extract2d_trace_sc0_input.value == 'None'
            else int(self.extract2d_trace_sc0_input.value),
            'trace_rows': trace_rows_value if self.extract2d_trace_rows_input.value !="None"
            else None,
            'trace_transpose': self.extract2d_trace_transpose_checkbox.value,
            'trace_lags': None if self.extract2d_trace_lags_input.value == 'None'
            else lag_range,
            'trace_channel': None if self.extract2d_trace_channel_input.value == 'None'
            else int(self.extract2d_trace_channel_input.value),
            'trace_hdu': self.extract2d_trace_hdu_input.value,
            
            # --- extract2d() parameters ---
            'extract2d_rows': extract2d_rows_value if self.extract2d_rows_input.value !='None'
            else None,
            'extract2d_buffer': self.extract2d_buffer_input.value,
    
            # --- findpeak() parameters ---
            'findpeak_sc0': None if self.extract2d_findpeak_sc0_input.value == 'None' 
            else int(self.extract2d_findpeak_sc0_input.value),
            'findpeak_width': None if self.extract2d_findpeak_width_input.value == 'None'
            else int(self.extract2d_findpeak_width_input.value),
            'findpeak_thresh': self.extract2d_findpeak_thresh_input.value,
            'findpeak_sort': self.extract2d_findpeak_sort_checkbox.value,
            'findpeak_back_percentile': self.extract2d_findpeak_backperc_input.value,
            'findpeak_method': self.extract2d_findpeak_method_input.value,
            'findpeak_smooth': self.extract2d_findpeak_smooth_input.value,
            'findpeak_diff': self.extract2d_findpeak_diff_input.value,
            'findpeak_bundle': self.extract2d_findpeak_bundle_input.value,
            'findpeak_verbose': self.extract2d_findpeak_verbose_checkbox.value,
            'findpeak_plot': self.extract2d_findpeak_plot_checkbox.value,
    
            # --- skyline() parameters ---
            'skyline_thresh': self.extract2d_skyline_thresh_input.value,
            'skyline_inter': self.extract2d_skyline_inter_checkbox.value,
            'skyline_linear': self.extract2d_skyline_linear_checkbox.value,
            'skyline_file': self.extract2d_skyline_file_input.value,
            'skyline_rows': skyline_rows_value if self.extract2d_skyline_rows_input.value != 'None'  
            else None,
            'skyline_obj_rad': self.extract2d_skyline_obj_rad_input.value,
            'correcting_value': self.extract2d_correcting_value_input.value,
        }
        log_params = {
                key: f"{value.start},{value.stop}" if isinstance(value, range) else value
                for key, value in extract_2d_params.items()
            }
        self.logger.log_action("Science & Extraction - 2D Extract", " Setup & Run 2D Extrction", log_params)
        if self._2d_flat_field_checkbox.value:
            flat_im = self.flat_frame
        else:
            flat_im = None

        self.processor.multi_extract2d(
            self.red, # Reducer instance
            self.trace, # Current trace
            self.targets, # Current targets
            self.reduced_frame, # Reduced science image
            flat_im,folder = self.log_file_input.value,
            **extract_2d_params, # Pass collected parameters
            param_area=self.processor_2d_control_area,
            output=self.processor_2d_output_area,
            output_2=self.output_area,
            param_area_feedback=self.processor_2d_feedback_area,
            update_callback=self._update_spec2d_out_callback,
            logger=self.logger
        )
    
    def _start_extract1d_handler(self, b):
        self.tv.tvclear()
        self.tv.clear()
        with self.output_area:
            clear_output(wait=True)
            if not self.spec2d_out:
                print("❌ 2D extracted spectra (spec2d_out) not available. Run 2D extraction first."); return
            if not self.targets: # Need targets to associate with spec2d_out
                print("❌ Targets list not available. Ensure slit finding and filtering is complete."); return
            if len(self.spec2d_out) != len(self.targets):
                print(f"⚠️ Warning: Mismatch between number of 2D spectra ({len(self.spec2d_out)}) and targets ({len(self.targets)}). Results may be inconsistent.")
    
            print("🚀 Initializing interactive 1D spectrum extraction UI in the '1D Extract' sub-tab...")
    
        # Clear processor-specific areas
        self.processor_1d_control_area.children = []
        self.processor_1d_feedback_area.children = []
        self.processor_1d_log_area.clear_output(wait=True)

        # lag1,lag2 = self.extract1d_trace_class_lags_input.value.split(',')
        # lag_range = range (int(lag1),int(lag2))
        # Collect parameters from the main widget
        lag1,lag2 = self.extract1d_trace_class_lags_input.value.split(',')
        lag_range_1d = range (int(lag1),int(lag2))
        
        variable_1d = get_srt_or_list(self.extract1d_trace_class_spectrum_input.value)
        if isinstance(variable_1d,str):
            spectrum_1d = variable_1d
        else:
            spectrum_1d = np.array(variable_1d)

        trace_model_value_1d = get_srt_or_list(self.extract1d_trace_class_model_input.value)
        trace_rows_value_1d = get_srt_or_list(self.extract1d_trace_class_rows_input.value)
        skyline_rows_value_1d = get_srt_or_list(self.extract1d_skyline_rows_input.value)
        extract1d_rows_value = get_srt_or_list(self.extract1d_trace_class_rows_input.value)
        trace_method_srows_value = get_srt_or_list(self.extract1d_trace_method_srows_input.value)
        # extract1d_back_value = get_srt_or_list(self.extract1d_back_input.value)
        
        extract_1d_params = {

            # --- Trace() parameters ---
            #'plot_spectra': self.extract1d_plot_spectra_checkbox.value,
            'trace_class_file': None if self.extract1d_trace_class_file_input.value == 'None'
            else self.extract1d_trace_class_file_input.value,
            'trace_class_spectrum': spectrum_1d if self.extract1d_trace_class_spectrum_input.value != 'None'
            else None,
            'trace_class_inst': None if self.extract1d_trace_class_inst_input.value == 'None'
            else self.extract1d_trace_class_inst_input.value,
            'trace_class_type': self.extract1d_trace_class_type_input.value,
            'trace_class_degree': self.extract1d_trace_degree_input.value,
            'trace_class_sigdegree': self.extract1d_trace_sigdegree_input.value,
            'trace_class_pix0': self.extract1d_trace_class_pix0_input.value,
            'trace_class_rad': self.extract1d_trace_class_rad_input.value,
            'trace_class_model': trace_model_value_1d if self.extract1d_trace_class_model_input.value !='None'
            else None,
            'trace_class_sc0': None if self.extract1d_trace_class_sc0_input.value == 'None' 
            else int(self.extract1d_trace_class_sc0_input.value),
            'trace_class_rows': trace_rows_value_1d if self.extract1d_trace_class_rows_input.value !="None"
            else None,
            'trace_class_transpose': self.extract1d_trace_class_transpose_checkbox.value,
            'trace_class_lags': None if len(self.extract1d_trace_class_lags_input.value) == 'None'
            else lag_range_1d,
            'trace_class_channel': None if self.extract1d_trace_class_channel_input.value == 'None'
            else int(self.extract1d_trace_class_channel_input.value),
            'trace_class_hdu': self.extract1d_trace_class_hdu_input.value,


            # --- findpeak() parameters ---
            'findpeak_sc0':None if self.extract1d_findpeak_sc0_input.value == 'None' 
            else int(self.extract1d_findpeak_sc0_input.value),
            'findpeak_width': None if self.extract1d_findpeak_width_input.value == 'None'
            else int(self.extract1d_findpeak_width_input.value),
            'findpeak_thresh': self.extract1d_findpeak_thresh_input.value,
            'findpeak_sort': self.extract1d_findpeak_sort_checkbox.value,
            'findpeak_back_percentile': self.extract2d_findpeak_backperc_input.value,
            'findpeak_method': self.extract1d_findpeak_method_input.value,
            'findpeak_smooth': self.extract1d_findpeak_smooth_input.value,
            'findpeak_diff': self.extract1d_findpeak_diff_input.value,
            'findpeak_bundle': self.extract1d_findpeak_bundle_input.value,
            'findpeak_verbose': self.extract1d_findpeak_verbose_checkbox.value,
            'findpeak_plot': self.extract1d_findpeak_plot_checkbox.value,
            
            # trace() method parameters
            'trace_method_srows': trace_method_srows_value if self.extract1d_trace_method_srows_input.value !='None'
            else None,
            'trace_method_sc0': None if self.extract1d_trace_method_sc0_input.value =='None' 
            else int(self.extract1d_trace_method_sc0_input.value),
            'trace_method_rad': None if self.extract1d_trace_method_rad_input.value == 0
            else self.extract1d_trace_method_rad_input.value,
            'trace_method_thresh': self.extract1d_trace_method_thresh_input.value,
            'trace_method_index': None if self.extract1d_trace_method_index_input.value =='None' 
            else int(self.extract1d_trace_method_index_input.value),
            'trace_method_skip': self.extract1d_trace_skip_input.value,
            'trace_method_gaussian': self.extract1d_trace_method_gaussian_checkbox.value,
            'trace_method_verbose': self.extract1d_trace_method_verbose_checkbox.value,

            
            # extract() parameters
            'extract_medfilt': None if self.extract1d_medfilt_input.value == 'None' 
            else int(self.extract1d_medfilt_input.value), # Main extraction radius
            # 'extract_back': extract1d_back_value if self.extract1d_back_input.value != 'None'
            # else None, # e.g., [[-10,-5],[5,10]]
            # 'extract_back': self.extract1d_back_input.value,
            'extract_fit': self.extract1d_fit_checkbox.value,
            'extract_old': self.extract1d_old_checkbox.value,
            'extract_nout': None if self.extract1d_nout_input.value == 'None'
            else int(self.extract1d_nout_input.value),
            'extract_threads': self.extract1d_threads_input.value,
            # 'sky_width_back': self.extract1d_sky_width_input.value,
            
            # --- skyline() parameters ---
            'skyline_thresh': self.extract1d_skyline_thresh_input.value,
            'skyline_inter': self.extract1d_skyline_inter_checkbox.value,
            'skyline_plot': self.extract1d_skyline_plot_checkbox.value,
            'skyline_linear': self.extract1d_skyline_linear_checkbox.value,
            'skyline_file': self.extract1d_skyline_file_input.value,
            'skyline_rows': skyline_rows_value_1d if self.extract1d_skyline_rows_input.value != 'None' 
            else None,
        }
        
        log_params = {
        key: f"{value.start},{value.stop}" if isinstance(value, range) else value
        for key, value in extract_1d_params.items()
        }
        self.logger.log_action("Science & Extraction - 1D Extract", "Setup & Run 1D Extraction", log_params)
        
        self.processor.multi_extract1d(
            self.spec2d_out,
            self.targets,
            **extract_1d_params,
            folder = self.log_file_input.value,
            param_area=self.processor_1d_control_area,
            param_area_1=self.processor_1d_feedback_area,
            param_area_2=self.processor_1d_log_area,
            output=self.output_area,
            logger=self.logger
            #widget_map=self.widget_map
            #update_callback=self._update_spec1d_out_callback
        )

    def _load_log_handler(self, b):
        """Handles the log file upload and initiates parsing."""
        if not self.log_uploader.value:
            with self.output_area:
                clear_output(wait=True)
                print("❌ No log file uploaded. Please select a .txt log file.")
            return
    
        # The FileUpload widget's 'value' is a tuple of dictionaries.
        # Since multiple=False, we take the first element of the tuple.
        uploaded_file_info = self.log_uploader.value[0]
        
        # FIX: The 'content' is a memoryview object. It must be converted to
        # bytes using .tobytes() before it can be decoded.
        content_bytes = uploaded_file_info['content']
        content_str = content_bytes.tobytes().decode('utf-8')
    
        with self.output_area:
            clear_output(wait=True)
            # Get the filename from the 'name' key in the dictionary.
            print(f"⚙️ Applying settings from log file: {uploaded_file_info['name']}")
            try:
                self._parse_and_apply_log(content_str)
                print("✅ Settings successfully applied from log file.")
                print("ℹ️ Note: You may need to re-run steps like 'Read Folder' and 'Find Slits' manually.")
            except Exception as e:
                print(f"❌ Error parsing or applying log file: {e}")
                import traceback
                traceback.print_exc()
    
        # Clear the uploader widget's value by assigning an empty tuple.
        self.log_uploader.value = ()
        self.log_uploader._counter = 0 # Reset internal counter for re-uploads
    
    def _parse_and_apply_log(self, log_content):
        """Parses all parameter blocks in a log file and updates widget values."""
        # This map is critical. It links keys in the log file's JSON to the widget objects.
        # YOU MUST EXPAND THIS MAP to include a key for every single widget parameter you log.
        self.widget_map = {
            'folder_path': self.folder_path_input,
            'Bias Frames': self.bias_files_input,
            'Combine Type': self.bias_type_dropdown,
            'Sigma Reject': self.bias_sigreject_input,
            'display individual': self.bias_display,
            'Trim Bias': self.bias_trim_checkbox,
            'Dark Frames': self.dark_files_input,
            'Combine Type': self.dark_type_dropdown,
            'Sigma Reject': self.dark_sigreject_input,
            'Clip (x Uncertainty)': self.dark_clip_input,
            'Display Individual': self.dark_display,
            'Apply dark Bias': self.apply_dark_bias_checkbox,
            'Trim Dark': self.dark_trim_checkbox,
            'Flat Frames': self.flat_files_input,
            'Combine Type': self.flat_type_dropdown,
            'Sigma Reject': self.flat_sigreject_input,
            'Spectral Flat': self.flat_spec_checkbox,
            'Window Width': self.flat_width_input,
            'Normalize Flat': self.flat_normalize_checkbox,
            'S/N Min (for Norm)': self.flat_snmin_input,
            'Apply Bias': self.apply_bias_checkbox,
            'Apply Dark': self.apply_dark_checkbox,
            'Display Individual flats': self.flat_display,
            'Flat littrow ': self.flat_littrow_checkbox,
            'Trim Flats': self.flat_trim_checkbox,
            'Arc Frames': self.arc_files_input,
            'Flat Frame for Slits': self.slit_flat_file_input,
            'KMS File': self.kms_file_input,
            'Edge Threshold (FindSlits)': self.findslits_thresh_input,
            'Use S/N for Edges (FindSlits)': self.findslits_sn_checkbox,
            'Smooth Radius (FindSlits)': self.findslits_smooth_input,
            'Fit Degree (FindSlits)': self.findslits_degree_input,
            'Pixels to skip (FindSlits)': self.findslits_skip_input,
            'spectra center location (if known)': self.findslits_cent_input,
            'Filter By': self.filter_method_dropdown,
            'Values': self.filter_values_input,
            # ---Reduce----
            'num': self.science_file_input,
            'Apply bias': self.reduce_appy_bias_checkbox,
            'Apply dark': self.reduce_appy_dark_checkbox,
            'Apply flat': self.reduce_appy_flat_checkbox,
            #'display': self.tv if self.display_enabled and self.tv ,
            'crbox': self.reduce_crbox_input,
            'crsig': self.reduce_crsig_input,
            'objlim': self.reduce_objlim_input,
            #'display': None, # self.tv, # Handled by tv call below
            'channel': self.reduce_channel_input,
            'scat': self.reduce_scat_input,
            'badpix': self.reduce_badpix_input,
            'trim': self.reduce_trim_checkbox,
            'utr': self.reduce_utr_checkbox,
            #'return_list': self.reduce_return_list_checkbox.value,
            'ext': self.reduce_ext_input,
            'solve': self.reduce_solve_checkbox,
            'seeing': self.reduce_seeing_input,
            'sigfrac': self.reduce_sigfrac_input,
            'lamp_spec_file': self.wavecal_lamp_spec_input,
            'shift_multiplier': self.wavecal_shift_multiplier_input,
            'arc_line': self.wavecal_arc_line_input,
            'clobber': self.wavecal_clobber_checkbox,
            'lamp_spec_file': self.wavecal_lamp_spec_input,
            'fit_degree': self.wavecal_fit_degree_input,
            'shift_multiplier': self.wavecal_shift_multiplier_input,
            # 'lamp_file_for_identify': self.wavecal_lamp_lines_input.value,
            'file': self.wavecal_id_file_input,
            'wave_fit_degree_after_identify': self.wavecal_refit_degree_input,
            
            # Parameters from identify()
            'identify_thresh': self.wavecal_id_thresh_input, # Mapped from 'thresh'
            'sky': self.wavecal_id_sky_checkbox,
            # 'wav': self.wavecal_id_wav_input,
            'wref': self.wavecal_id_wref_input,
            'inter': self.wavecal_id_inter_checkbox,
            'orders': self.wavecal_id_orders_input,
            'verbose': self.wavecal_id_verbose_checkbox,
            'rad': self.wavecal_id_rad_input,
            'fit': self.wavecal_id_fit_checkbox,
            'maxshift': self.wavecal_id_maxshift_input,
            'sampling_value': self.wavecal_id_sample_input,
            'correcting_value': self.wavecal_id_re_sample_input,
            'arc_line_position': self.wavecal_id_arc_line_position_input,
            'weight_thresh': self.wavecal_id_weak_weight_input,
            'disp': self.wavecal_id_disp_input,
            'plot': self.wavecal_id_plot_checkbox,
            'pixplot': self.wavecal_id_pixplot_checkbox,
            'domain': self.wavecal_id_domain_checkbox,
            # 'plot_first_identify': True, # Mapped from 'plot' for the first run
            'plotinter': self.wavecal_id_plotinter_checkbox, # Mapped from 'plotinter'
            'xmin': self.wavecal_id_xmin_input,
            'xmax': self.wavecal_id_xmax_input,
            'lags_offset': self.wavecal_id_lags_input,
            'nskip': self.wavecal_id_nskip_input,
            'rows': self.wavecal_id_rows_input,
            
            # --- Trace() parameters ---
            'trace_file': self.extract2d_trace_file_input,
            'trace_spectrum': self.extract2d_spectrum_input,
            'trace_inst': self.extract2d_trace_inst_input,
            'trace_type': self.extract2d_trace_type_input,
            'trace_degree': self.extract2d_trace_degree_input,
            'trace_sigdegree': self.extract2d_trace_sigdegree_input,
            'trace_pix0': self.extract2d_trace_pix0_input,
            'trace_rad': self.extract2d_trace_rad_input,
            'trace_model': self.extract2d_trace_model_input,
            'trace_sc0': self.extract2d_trace_sc0_input,
            'trace_rows': self.extract2d_trace_rows_input,
            'trace_transpose': self.extract2d_trace_transpose_checkbox,
            'trace_lags': self.extract2d_trace_lags_input,
            'trace_channel': self.extract2d_trace_channel_input,
            'trace_hdu': self.extract2d_trace_hdu_input,
            
            # --- extract2d() parameters ---
            'extract2d_rows': self.extract2d_rows_input,
            'extract2d_buffer': self.extract2d_buffer_input,
            '2D flat apply': self._2d_flat_field_checkbox,
    
            # --- findpeak() parameters ---
            'findpeak_sc0': self.extract2d_findpeak_sc0_input,
            'findpeak_width': self.extract2d_findpeak_width_input,
            'findpeak_thresh': self.extract2d_findpeak_thresh_input,
            'findpeak_sort': self.extract2d_findpeak_sort_checkbox,
            'findpeak_back_percentile': self.extract2d_findpeak_backperc_input,
            'findpeak_method': self.extract2d_findpeak_method_input,
            'findpeak_smooth': self.extract2d_findpeak_smooth_input,
            'findpeak_diff': self.extract2d_findpeak_diff_input,
            'findpeak_bundle': self.extract2d_findpeak_bundle_input,
            'findpeak_verbose': self.extract2d_findpeak_verbose_checkbox,
            'findpeak_plot': self.extract2d_findpeak_plot_checkbox,
    
            # --- skyline() parameters ---
            'skyline_thresh': self.extract2d_skyline_thresh_input,
            'skyline_inter': self.extract2d_skyline_inter_checkbox,
            'skyline_linear': self.extract2d_skyline_linear_checkbox,
            'skyline_file': self.extract2d_skyline_file_input,
            'skyline_rows': self.extract2d_skyline_rows_input,
            'skyline_obj_rad': self.extract2d_skyline_obj_rad_input,
            'correcting_value': self.extract2d_correcting_value_input,
                    # --- Trace() parameters ---
            #'plot_spectra': self.extract1d_plot_spectra_checkbox.value,
            'trace_class_file': self.extract1d_trace_class_file_input,
            'trace_class_spectrum': self.extract1d_trace_class_spectrum_input,
            'trace_class_inst': self.extract1d_trace_class_inst_input,
            'trace_class_type': self.extract1d_trace_class_type_input,
            'trace_class_degree': self.extract1d_trace_degree_input,
            'trace_class_sigdegree': self.extract1d_trace_sigdegree_input,
            'trace_class_pix0': self.extract1d_trace_class_pix0_input,
            'trace_class_rad': self.extract1d_trace_class_rad_input,
            'trace_class_model': self.extract1d_trace_class_model_input,
            'trace_class_sc0': self.extract1d_trace_class_sc0_input,
            'trace_class_rows': self.extract1d_trace_class_rows_input,
            'trace_class_transpose': self.extract1d_trace_class_transpose_checkbox,
            'trace_class_lags': self.extract1d_trace_class_lags_input,
            'trace_class_channel': self.extract1d_trace_class_channel_input,
            'trace_class_hdu': self.extract1d_trace_class_hdu_input,


            # --- findpeak() parameters ---
            'findpeak_sc0': self.extract1d_findpeak_sc0_input,
            'findpeak_width': self.extract1d_findpeak_width_input,
            'findpeak_thresh': self.extract1d_findpeak_thresh_input,
            'findpeak_sort': self.extract1d_findpeak_sort_checkbox,
            'findpeak_back_percentile': self.extract2d_findpeak_backperc_input,
            'findpeak_method': self.extract1d_findpeak_method_input,
            'findpeak_smooth': self.extract1d_findpeak_smooth_input,
            'findpeak_diff': self.extract1d_findpeak_diff_input,
            'findpeak_bundle': self.extract1d_findpeak_bundle_input,
            'findpeak_verbose': self.extract1d_findpeak_verbose_checkbox,
            'findpeak_plot': self.extract1d_findpeak_plot_checkbox,
            
            # trace() method parameters
            'trace_method_srows': self.extract1d_trace_method_srows_input,
            'trace_method_sc0': self.extract1d_trace_method_sc0_input,
            'trace_method_rad': self.extract1d_trace_method_rad_input,
            'trace_method_thresh': self.extract1d_trace_method_thresh_input,
            'trace_method_index': self.extract1d_trace_method_index_input,
            'trace_method_skip': self.extract1d_trace_skip_input,
            'trace_method_gaussian': self.extract1d_trace_method_gaussian_checkbox,
            'trace_method_verbose': self.extract1d_trace_method_verbose_checkbox,
            
            # extract() parameters
            'extract_medfilt': self.extract1d_medfilt_input,
            # 'extract_back': self.extract1d_back_input,
            'extract_fit': self.extract1d_fit_checkbox,
            'extract_old': self.extract1d_old_checkbox,
            'extract_nout': self.extract1d_nout_input,
            'extract_threads': self.extract1d_threads_input,
            # 'sky_width_back': self.extract1d_sky_width_input,
            
            # --- skyline() parameters ---
            'skyline_thresh': self.extract1d_skyline_thresh_input,
            'skyline_inter': self.extract1d_skyline_inter_checkbox,
            'skyline_plot': self.extract1d_skyline_plot_checkbox,
            'skyline_linear': self.extract1d_skyline_linear_checkbox,
            'skyline_file': self.extract1d_skyline_file_input,
            'skyline_rows': self.extract1d_skyline_rows_input,
        
        }

        all_params = {}
        # ... (code to parse log_content and populate all_params remains the same) ...
        in_params_block = False
        json_str_buffer = ""
        for line in log_content.splitlines():
            if line.strip() == "PARAMETERS:":
                in_params_block = True
                json_str_buffer = ""
                continue
            if in_params_block:
                json_str_buffer += line
                try:
                    params = json.loads(json_str_buffer)
                    all_params.update(params)
                    in_params_block = False
                except json.JSONDecodeError:
                    continue
    
        applied_count = 0
        for key, value in all_params.items():
            if key not in self.widget_map:
                print(f"ℹ️ Log parameter '{key}' has no corresponding widget. Skipping.")
                continue
    
            widget_object = self.widget_map[key]
            
            # This check prevents crashes if the widget_map has bad entries (like None)
            if not hasattr(widget_object, 'value'):
                print(f"⚠️ Log parameter '{key}' points to an invalid object in widget_map. Skipping.")
                continue
                
            try:
                prepared_value = value
    
                # 1. Handle None values specifically for each widget type
                if prepared_value is None:
                    if isinstance(widget_object, (widgets.IntText, widgets.BoundedIntText)):
                        prepared_value = 0 # Assign a default, as None is not accepted
                    elif isinstance(widget_object, (widgets.FloatText, widgets.BoundedFloatText)):
                        prepared_value = 0.0 # Assign a default
                    elif isinstance(widget_object, widgets.Text):
                        prepared_value = '' # Use empty string for Text widgets
                    # For other types like Checkbox/Dropdown, None might be valid or we can skip
                    else:
                        widget_object.value = None
                        applied_count += 1
                        continue
                
                # 2. If value is not None, ensure it has the correct type
                if isinstance(widget_object, (widgets.IntText, widgets.BoundedIntText)):
                    prepared_value = int(float(value))
                elif isinstance(widget_object, (widgets.FloatText, widgets.BoundedFloatText)):
                    prepared_value = float(value)
                elif isinstance(widget_object, widgets.Text):
                    # Per your request, ensure any value for a Text widget is a string
                    prepared_value = str(value)
    
                # 3. Assign the final, prepared value
                widget_object.value = prepared_value
                applied_count += 1
    
            except Exception as e:
                print(f"⚠️ Could not set widget for '{key}' with value '{value}'. Error: {e}")
                
        print(f"Applied {applied_count} parameter(s) to the UI.")

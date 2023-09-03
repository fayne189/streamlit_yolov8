import os
import glob
import numpy as np
import streamlit as st

from utils import save_temp_file

def readme():
    # Open the README.md file and read all lines
    with open("README.md", 'r') as f:
        readme_line = f.readlines()
        # Create an empty buffer list to temporarily store the lines of the README.md file
        readme_buffer = []
        # Use the glob library to search for all files in the Resources directory and extract the file names
        resource_files = [os.path.basename(x) for x in glob.glob(f'Resources/*')]
        
    # Iterate over each line of the README.md file
    for line in readme_line :
        # Append the current line to the buffer list
        readme_buffer.append(line) 
        # Check if any images are present in the current line
        for image in resource_files:
            # If an image is found, display the buffer list up to the last line
            if image in line:
                st.markdown(''.join(readme_buffer[:-1])) 
                # Display the image from the Resources folder using the image name from the resource_files list
                st.image(f'Resources/{image}')
                # Clear the buffer list
                readme_buffer.clear()
                
    # Display any remaining lines in the buffer list using the st.markdown() function
    st.markdown(''.join(readme_buffer))

class MainUi(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.ui_cfg = cfg.get('ui_cfg')
        self.model_path = None
        self.use_tracker = None
        self.confidence_threshold = None
        self.video_options = {'demo.mp4':'resources/demo.mp4'}
        self.init_layout()
        self.init_components()
             
    def init_layout(self):
        # side bar layout
        self.sidebar_source = st.sidebar.container()
        self.sidebar_frame_selector = st.sidebar.container()
        self.sidebar_model = st.sidebar.container()
        self.sidebar_model_buttons = st.sidebar.container()
        # main layout
        self.main_layout = st.container()
        ## main page layout
        self.main_discription = self.main_layout.container()
        self.main_screen = self.main_layout.empty()

    def init_components(self):
        self.init_main()
        self.init_source_sidebar()
        self.init_model_sidebar()

    def init_main(self):
        # init online page
        with self.main_discription:
            with st.expander("README>>"):   # todo good readme
                readme()
        self.main_screen.image(np.zeros((480, 640, 3), np.uint8), channels='BGR')
 
    def init_source_sidebar(self):
        self.sidebar_source.markdown('---')
        source_video = self.sidebar_source.file_uploader(
            label="Choose a video...",
            type=['mp4']
        )
        if source_video:
            temp_path = save_temp_file(source_video)
            self.video_options.update({source_video.name:temp_path})
        selected_video = self.sidebar_source.selectbox(self.ui_cfg['sidebar_select_video'], self.video_options, index=len(self.video_options)-1 if source_video else 0)
        self.video_path = self.video_options.get(selected_video)
        print(self.video_options)

    def init_model_sidebar(self):
        self.sidebar_model.markdown('---')
        self.model_path = self.sidebar_model.selectbox(self.ui_cfg['selectbox_model_select'], self.ui_cfg['model_options'])
        if self.model_path is None or self.model_path == self.ui_cfg['model_options'][-1]:
            self.model_path = self.sidebar_model.text_input(self.ui_cfg['input_model_path'], value=self.cfg.get('weights'), placeholder='input yolov8 weight path')
        use_tracker = self.sidebar_model.selectbox(self.ui_cfg['selectbox_use_tracker'], self.ui_cfg['tracker_options'])
        confidence_threshold = self.sidebar_model.slider(self.ui_cfg['slider_confidence_threshold'], 0.0, 1.0, self.cfg.get('confidence', 0.5), 0.01)
        self.cfg.update({'use_tracker': use_tracker, 'confidence_threshold': confidence_threshold})
        self.use_tracker = use_tracker
        self.confidence_threshold = confidence_threshold
        with self.sidebar_model_buttons:
            button1, button2, button3 = st.columns(3)
            with button1:
                self.button_predict_one = st.button(self.ui_cfg['button_predict_one'])
            with button2:
                self.button_predict_all = st.button(self.ui_cfg['button_predict_all'])
            with button3:
                self.button_stop = st.button(self.ui_cfg['button_stop'])

    def frame_selector_sidebar(self, frames):
        min_elts, max_elts = self.sidebar_frame_selector.slider(self.ui_cfg['sidebar_select_frames'], 0, len(frames), [0, len(frames)])
        selected_frames = frames[min_elts:max_elts]
        selected_frame_index = self.sidebar_frame_selector.slider(self.ui_cfg['sidebar_choose_frame'], min_elts, max_elts, min_elts)
        if len(selected_frames) < 1:
            return None, None
        return selected_frames, selected_frame_index
  

    def show(self,frame):
        self.main_screen.image(frame, channels='BGR')
